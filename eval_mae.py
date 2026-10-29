"""
Danh gia do chinh xac uoc luong anh huong cua mot checkpoint tren do thi kiem thu:
MAE, RMSE, MAPE, Pearson, Spearman cua TONG anh huong du doan so voi tong anh huong
Monte Carlo, kem moc so sanh "khong lan truyen" (tong anh huong du doan = so seed).

Viet moi (khong sua IE.py): khong import cupy, nhan --feature-mode nhu IM.py, va co the
chay tren CPU khi CUDA loi.

Chay thu nhanh (4 lo, vai chuc giay) de kiem tra script:
  python eval_mae.py --checkpoint-path checkpoints/synth_all_4_3_32_0.3/1.pkt \
      --feature-mode exact --device cpu --max-sets 200
Chay day du:
  python eval_mae.py --checkpoint-path checkpoints/synth_all_4_3_32_0.3/1.pkt --feature-mode exact --device cpu
  python eval_mae.py --checkpoint-path checkpoints/synth_est1_4_3_32_0.3/1.pkt --feature-mode est1 --est-s 1000 --device cpu
  python eval_mae.py --checkpoint-path checkpoints/synth_est2_4_3_32_0.3/1.pkt --feature-mode est2 --est-T 1000 --device cpu
"""
import argparse
import os
import time

import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--checkpoint-path", required=True)
ap.add_argument("--feature-mode", default="exact", help="exact | est1 | est2")
ap.add_argument("--est-s", type=int, default=1000)
ap.add_argument("--est-T", type=int, default=1000)
ap.add_argument("--graph", default="Extended")
ap.add_argument("--prob", default="LT")
ap.add_argument("--n-stacks", type=int, default=1)
ap.add_argument("--input-dim", type=int, default=4)
ap.add_argument("--hidden-dim", type=int, default=32)
ap.add_argument("--layer-num", type=int, default=3)
ap.add_argument("--batch-size", type=int, default=50)
ap.add_argument("--max-sets", type=int, default=0, help="chi danh gia N seed set dau (0 = tat ca)")
ap.add_argument("--device", default="cuda", help="cuda | cpu")
args = ap.parse_args()

use_cuda = args.device == "cuda"
torch.set_num_threads(4)
if not use_cuda:
    # utils.load_data co dinh .cuda() va .to('cuda:0'); vo hieu hoa de chay tren CPU
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    torch.Tensor.cuda = lambda self, *a, **k: self
    import dgl as _dgl
    type(_dgl.graph(([0], [1]))).to = lambda self, *a, **k: self   # lay lop do thi tu mot do thi mau

import dgl  # noqa: E402
from utils import load_data  # noqa: E402
from models import MONSTOR  # noqa: E402

dev = torch.device("cuda" if use_cuda else "cpu")
test_labels = [(args.graph, "test", args.prob)]
lstr = "_".join(test_labels[0])

t0 = time.time()
g, sX, sy, X, y, _g, _sX, _sy = load_data(train_labels=[], val_labels=[], test_labels=test_labels,
                                          feature_mode=args.feature_mode,
                                          est_s=args.est_s, est_T=args.est_T)
print("nap du lieu va tinh feature xong sau {:.1f}s".format(time.time() - t0), flush=True)

model = MONSTOR(in_feats=args.input_dim + 10, n_hidden=args.hidden_dim, n_layers=args.layer_num).to(dev)
model.load_state_dict(torch.load(args.checkpoint_path, map_location=dev))
model.eval()

bs = args.batch_size
graph = _g[lstr]
V = graph.number_of_nodes()
bg = dgl.batch([graph for _ in range(bs)])
n_f, s = args.input_dim, args.n_stacks
N = _sX[lstr].shape[0]
if args.max_sets > 0:
    N = min(N, args.max_sets)
N = (N // bs) * bs

gt, preds, n_seeds = [], [], []
x = torch.zeros(bg.number_of_nodes(), n_f + s, requires_grad=False).to(dev)
t0 = time.time()
with torch.no_grad():
    for k, idx in enumerate(range(0, N, bs)):
        seeds = _sX[lstr][idx:idx + bs]
        gt += [torch.sum(_sy[lstr][idx + i]).item() for i in range(bs)]
        n_seeds += [float(torch.sum(seeds[i])) for i in range(bs)]
        x[:, n_f - 2] = x[:, n_f - 1] = torch.t(seeds.reshape(-1).to(dev))
        for j in range(n_f, n_f + s):
            x[:, j] = model(bg, torch.cat((bg.ndata["idfeat"].detach(), x[:, j - n_f:j]), dim=-1)).data
            x[:, j - 1] = x[:, j] - x[:, j - 1]
        preds += [torch.sum(x[:, n_f + s - 1][i * V:(i + 1) * V]).item() for i in range(bs)]
        if k % 10 == 0:
            print("  lo {}/{}  ({:.0f}s)".format(k + 1, N // bs, time.time() - t0), flush=True)

gt, preds, n_seeds = np.array(gt), np.array(preds), np.array(n_seeds)


def report(name, sl):
    g_, p_, s_ = gt[sl], preds[sl], n_seeds[sl]
    mae = np.mean(np.abs(p_ - g_))
    rmse = np.sqrt(np.mean((p_ - g_) ** 2))
    mape = np.mean(np.abs(p_ - g_) / g_)
    base = np.mean(np.abs(s_ - g_))
    from scipy.stats import pearsonr, spearmanr
    if np.std(p_) > 0:
        pc, sc = pearsonr(g_, p_)[0], spearmanr(g_, p_)[0]
    else:
        pc = sc = float("nan")
    if np.std(s_) > 0:
        bpc, bsc = pearsonr(g_, s_)[0], spearmanr(g_, s_)[0]
    else:
        bpc = bsc = float("nan")
    print("{:<16} n={:<5} MAE={:9.3f} RMSE={:9.3f} MAPE={:6.3f} Pearson={:6.3f} Spearman={:6.3f} | "
          "TB that={:8.2f} TB du doan={:8.2f} TB |S|={:6.2f} | MAE neu khong lan truyen={:9.3f} | "
          "Pearson/Spearman chi voi |S|={:6.3f}/{:6.3f}".format(
              name, len(g_), mae, rmse, mape, pc, sc, g_.mean(), p_.mean(), s_.mean(), base, bpc, bsc))


print("\n=== {} | {} | feature-mode={} | s={} ===".format(args.checkpoint_path, lstr, args.feature_mode, s))
report("toan bo", slice(0, len(gt)))
if len(gt) >= 2 * bs:
    h = (len(gt) // 2 // bs) * bs
    report("nua dau", slice(0, h))
    report("nua sau", slice(h, len(gt)))