"""
H6 — Estimator 2 (HISP-Vec) trên ego-Facebook, hoàn tất bộ so sánh 3
cách (exact/est1/est2) mà cô Dung yêu cầu. Dùng lại C_exact đã lưu
từ lần chạy facebook_estimator1_fast.py trước (không cần upload nếu
đã có 2 file .npy đó trong Colab, nếu không sẽ tự tính lại).
"""
import numpy as np, scipy.sparse as sp, urllib.request, gzip, os, time
rng = np.random.default_rng(0)

def download(url):
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    return gzip.decompress(data).decode()

def edgelist_to_LT_matrix(text, directed_input=False):
    edges = []; nodes = set()
    for line in text.splitlines():
        if line.startswith('#') or not line.strip(): continue
        a, b = map(int, line.split()[:2])
        nodes.add(a); nodes.add(b); edges.append((a, b))
        if not directed_input: edges.append((b, a))
    id_map = {v: i for i, v in enumerate(sorted(nodes))}
    n = len(id_map)
    src = [id_map[a] for a, b in edges]; dst = [id_map[b] for a, b in edges]
    W = sp.csr_matrix((np.ones(len(edges)), (src, dst)), shape=(n, n))
    W.sum_duplicates()
    indeg = np.asarray(W.sum(axis=0)).ravel(); indeg[indeg == 0] = 1
    W = sp.csr_matrix(W.multiply(1.0 / indeg)); W.sort_indices()
    return W, n

def hisp_vec(W, q, T, rng):
    n = W.shape[0]; acc = np.zeros((n, q-1))
    for t in range(T):
        z = rng.choice([-1.0, 1.0], size=n); y = z.copy()
        for l in range(1, q+1):
            y = W @ y
            if l >= 2: acc[:, l-2] += z * y
    return acc / T

def exact_diag(W, q):
    cur = W.copy(); diags = []
    for r in range(2, q+1):
        cur = cur @ W; diags.append(cur.diagonal())
    return np.stack(diags, axis=-1)

print("Đang tải ego-Facebook...")
W_fb, n_fb = edgelist_to_LT_matrix(download("https://snap.stanford.edu/data/facebook_combined.txt.gz"), directed_input=False)
print(f"ego-Facebook: n={n_fb}, m={W_fb.nnz}, bậc TB={W_fb.nnz/n_fb:.1f}")

Q = 11

if os.path.exists("C_exact_facebook.npy"):
    print("Dùng lại C_exact_facebook.npy đã lưu trước đó.")
    C_exact = np.load("C_exact_facebook.npy")
else:
    print("Chưa có file lưu sẵn, tự tính exact...")
    t0 = time.perf_counter()
    C_exact = exact_diag(W_fb, Q)
    print(f"Thời gian exact: {time.perf_counter()-t0:.2f}s")
    np.save("C_exact_facebook.npy", C_exact)

print(f"\nChạy Estimator 2 (HISP-Vec), T=1000, toàn bộ {n_fb} node...")
t0 = time.perf_counter()
C_est2 = hisp_vec(W_fb, Q, 1000, rng)
t_est2 = time.perf_counter() - t0
print(f"Thời gian Estimator 2: {t_est2:.2f}s")

mask = C_exact > 0
rel2 = np.abs(C_est2[mask] - C_exact[mask]) / C_exact[mask]
print(f"Sai số trung vị: {100*np.median(rel2):.1f}%   p90: {100*np.percentile(rel2,90):.1f}%")

np.save("C_est2_facebook.npy", C_est2)

print("\n" + "="*70)
print("TỔNG KẾT H6 — ego-Facebook, thời gian tiền xử lý")
print("="*70)
if os.path.exists("facebook_est1_time.txt"):
    t_est1 = float(open("facebook_est1_time.txt").read())
else:
    t_est1 = 975.90  # số đã đo trước đó, ghi cứng nếu không có file lưu
t_exact = 13.94  # số đã đo trước đó
print(f"  MONSTOR+ (exact):     {t_exact:8.2f}s   (1.0x)")
print(f"  Estimator 1 (s=1000): {t_est1:8.2f}s   ({t_exact/t_est1:.3f}x so với exact)")
print(f"  Estimator 2 (T=1000): {t_est2:8.2f}s   ({t_exact/t_est2:.3f}x so với exact)")
