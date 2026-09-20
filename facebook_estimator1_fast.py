"""
Bản tối ưu của Estimator 1 (path-sampling) cho H6 — dùng kỹ thuật
"prefix reuse" (paper HISP mục 5.4): đi 1 đường ngẫu nhiên dài q-1=10
bước, lấy kết quả tại MỌI điểm dừng dọc đường thay vì đi lại từ đầu
cho mỗi bậc r. Giảm ~10 lần khối lượng tính so với bản gốc.
"""
import numpy as np, scipy.sparse as sp, urllib.request, gzip, time
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

def path_sample_all_orders(W, dW, v, q, s, rng):
    """1 đường đi dài q-1 bước / mẫu, dùng chung cho mọi r=2..q.
    Trả về mảng (q-1,) là ước lượng c_2(v)..c_q(v)."""
    indptr, indices, data = W.indptr, W.indices, W.data
    acc = np.zeros(q - 1)  # tích luỹ cho r=2..q
    for j in range(s):
        x = v; prod = 1.0
        for step in range(1, q):  # step = r-1, đi tới q-1 bước
            lo, hi = indptr[x], indptr[x+1]
            if lo == hi:
                break  # chết giữa đường -> mọi r còn lại (chưa đi tới) vẫn là 0, bỏ qua
            prod *= dW[x]
            p = data[lo:hi] / dW[x]
            x = indices[lo:hi][rng.choice(hi-lo, p=p)]
            # kiểm tra cạnh quay về v ngay tại bước này -> đóng góp cho r = step+1
            lo2, hi2 = indptr[x], indptr[x+1]
            k = np.searchsorted(indices[lo2:hi2], v)
            back = data[lo2+k] if k < hi2-lo2 and indices[lo2+k] == v else 0.0
            acc[step - 1] += prod * back  # r = step+1 -> index r-2 = step-1
    return acc / s

def exact_diag(W, q):
    cur = W.copy(); diags = []
    for r in range(2, q+1):
        cur = cur @ W; diags.append(cur.diagonal())
    return np.stack(diags, axis=-1)

print("Đang tải ego-Facebook...")
W_fb, n_fb = edgelist_to_LT_matrix(download("https://snap.stanford.edu/data/facebook_combined.txt.gz"), directed_input=False)
print(f"ego-Facebook: n={n_fb}, m={W_fb.nnz}, bậc TB={W_fb.nnz/n_fb:.1f}")

Q = 11
dW = np.asarray(W_fb.sum(axis=1)).ravel()

print("\nTính exact để đối chiếu (đã biết mất ~14s)...")
t0 = time.perf_counter()
C_exact = exact_diag(W_fb, Q)
print(f"Thời gian exact: {time.perf_counter()-t0:.2f}s")

print(f"\nChạy Estimator 1 (bản prefix-reuse), s=1000, toàn bộ {n_fb} node...")
t0 = time.perf_counter()
C_est1 = np.zeros_like(C_exact)
for v in range(n_fb):
    C_est1[v, :] = path_sample_all_orders(W_fb, dW, v, Q, 1000, rng)
    if v % 500 == 0:
        print(f"  ...node {v}/{n_fb} ({time.perf_counter()-t0:.1f}s)")
t_est1 = time.perf_counter() - t0
print(f"\nThời gian Estimator 1 (prefix-reuse): {t_est1:.2f}s")

mask = C_exact > 0
rel1 = np.abs(C_est1[mask] - C_exact[mask]) / C_exact[mask]
print(f"Sai số trung vị: {100*np.median(rel1):.1f}%   p90: {100*np.percentile(rel1,90):.1f}%")

np.save("C_exact_facebook.npy", C_exact)
np.save("C_est1_facebook.npy", C_est1)
print("\nĐã lưu C_exact_facebook.npy, C_est1_facebook.npy — dùng lại cho bước estimator 2.")
