"""
Chan doan validation: so sanh tong anh huong DU DOAN cua model voi dap an THAT
tren vai do thi val, cho mot so checkpoint. Sao chep dung cach tinh trong khoi
validation cua train_LT.py.

Chay trong thu muc repo (can venv_hisp va LD_LIBRARY_PATH nhu khi train):
  python diag_val.py checkpoints/synth_all_4_3_32_0.3 exact synth-small-ba-005,synth-medium-ba-006
  python diag_val.py checkpoints/synth_est2_4_3_32_0.3 est2 synth-small-ba-005,synth-medium-ba-006

Hai do thi tren nam trong ca tap 8 do thi (MONSTOR+) lan tap 15 do thi (HISP).
"""
import sys
import numpy as np
import torch
import dgl
from utils import load_data
from models import MONSTOR

ckpt_dir, mode, graphs = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
epochs = [1, 2, 10, 50, 100]
stacks_to_print = (1, 2, 5, 20)
input_dim, hidden_dim, layer_num, batch_size, n_max_stacks = 4, 32, 3, 50, 20

kw = {'feature_mode': mode}
if mode == 'est1':
    kw['est_s'] = 1000
if mode == 'est2':
    kw['est_T'] = 1000

val_labels = [(g, 'val', 'LT') for g in graphs]
_, _, _, _, _, _g, _sX, _sy = load_data(train_labels=[], val_labels=val_labels,
                                        test_labels=[], **kw)

model = MONSTOR(in_feats=input_dim + 10, n_hidden=hidden_dim, n_layers=layer_num).cuda()

for vl in val_labels:
    lstr = '_'.join(vl)
    gt0 = np.array([torch.sum(_sy[lstr][i]).item() for i in range(batch_size)])
    print('=== {}: V={}, gt_mean={:.3f}, sqrt(sum gt^2) (loi cua bo du doan toan 0) = {:.3f}'.format(
        lstr, _g[lstr].number_of_nodes(), gt0.mean(), np.sqrt(np.sum(gt0 ** 2))))

for ep in epochs:
    model.load_state_dict(torch.load('{}/{}.pkt'.format(ckpt_dir, ep)))
    model.eval()
    for vl in val_labels:
        lstr = '_'.join(vl)
        V = _g[lstr].number_of_nodes()
        bg = dgl.batch([_g[lstr] for _ in range(batch_size)])
        with torch.no_grad():
            x = torch.zeros(bg.number_of_nodes(), input_dim + n_max_stacks).cuda()
            gt = np.array([torch.sum(_sy[lstr][i]).item() for i in range(batch_size)])
            seeds = _sX[lstr][0:batch_size]
            x[:, input_dim - 2] = x[:, input_dim - 1] = torch.t(seeds.view(-1).cuda())
            n_seeds = float(seeds.sum(dim=1).float().mean())
            for j in range(input_dim, input_dim + n_max_stacks):
                x[:, j] = model(bg, torch.cat((bg.ndata['idfeat'].detach(),
                                               x[:, j - input_dim:j]), dim=-1)).data
                x[:, j - 1] = x[:, j] - x[:, j - 1]
                s = j - input_dim + 1
                if s in stacks_to_print:
                    preds = np.array([torch.sum(x[:, j][i * V:(i + 1) * V]).item()
                                      for i in range(batch_size)])
                    node_p = x[:, j]
                    print('epoch {:3d} {} s={:2d}: pred_mean={:9.3f} gt_mean={:9.3f} '
                          '|S|_mean={:5.1f} MAE={:9.3f} | node_prob min={:.2e} max={:.2e} mean={:.2e}'.format(
                              ep, lstr, s, preds.mean(), gt.mean(), n_seeds,
                              np.abs(preds - gt).mean(),
                              float(node_p.min()), float(node_p.max()), float(node_p.mean())))
