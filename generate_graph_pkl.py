"""
Sinh các file `datadir/{graph}_{split}_{prob}_graph.pkl.gz` mà `utils.py`
(hàm `_load_data_inner`) cần đọc, nhưng `processing.py` trong repo gốc
KHÔNG hề sinh ra (chỉ sinh các file `_random.pkl.gz`/`_degree.pkl.gz`).

Mỗi file `_graph.pkl.gz` là 1 scipy sparse matrix (định dạng CSR) —
xác nhận qua cách `load_data()` dùng nó: `dgl.from_scipy(data[0])`,
`data[0] @ data[0]` (nhân ma trận), `data[0].data` (lấy trọng số cạnh).

LƯU Ý QUAN TRỌNG — bẫy dễ sai âm thầm:
`graphs/` chỉ có 2 giai đoạn `train` và `test`, KHÔNG có `val` riêng.
Theo đúng mô tả trong paper MONSTOR+ gốc (mục 4.1): tập validation
dùng CHUNG mạng lưới ở giai đoạn train (cùng ma trận P/A), chỉ khác
seed set được chọn ra để tạo tuple. Vì vậy khi sinh file cho split
'val', phải đọc từ file `_train_` (không phải `_val_`, vì file đó
không tồn tại) rồi ghi ra tên `_val_..._graph.pkl.gz`.

Chạy 1 lần trước khi gọi bất kỳ script train/IM/IE/submodularity nào.
"""
import scipy.sparse as sp
import pickle
import gzip
import os


def load_edgelist_as_csr(path):
    """Đọc đúng format graphs/*.txt của MONSTOR+: dòng đầu 'n m',
    các dòng sau 'src dst prob', node 0-indexed."""
    with open(path) as f:
        n, m = map(int, f.readline().split())
        src, dst, w = [], [], []
        for line in f:
            a, b, p = line.split()
            src.append(int(a))
            dst.append(int(b))
            w.append(float(p))
    W = sp.csr_matrix((w, (src, dst)), shape=(n, n))
    W.sort_indices()
    return W


def generate_all(graphs_dir="graphs", out_dir="datadir",
                  graph_names=("Extended", "Celebrity", "WannaCry"),
                  prob_names=("BT", "JI", "LP", "LT")):
    os.makedirs(out_dir, exist_ok=True)
    n_written = 0
    n_skipped = 0

    for graph_name in graph_names:
        for prob in prob_names:
            for split_out in ("train", "val", "test"):
                # 'val' không có file riêng -> dùng chung ma trận với 'train'
                split_in = "train" if split_out in ("train", "val") else "test"
                in_path = f"{graphs_dir}/{graph_name}_{split_in}_{prob}.txt"
                out_path = f"{out_dir}/{graph_name}_{split_out}_{prob}_graph.pkl.gz"

                if not os.path.exists(in_path):
                    print(f"[BỎ QUA] không có {in_path}")
                    n_skipped += 1
                    continue

                W = load_edgelist_as_csr(in_path)
                with gzip.open(out_path, "wb") as f:
                    pickle.dump(W, f, protocol=4)
                print(f"[OK] {in_path} -> {out_path}  (n={W.shape[0]}, nnz={W.nnz})")
                n_written += 1

    print(f"\nHoàn tất: {n_written} file đã ghi, {n_skipped} bỏ qua (thiếu input).")


if __name__ == "__main__":
    generate_all()