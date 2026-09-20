"""
So sanh Tinh chinh xac vs Estimator 2 tren WannaCry THAT (khong phai
tong hop) - du lieu Twitter, thua, nhung n lon nhat trong 3 dataset
Twitter (~19.000 node, lon hon Extended ~3.4 lan).

Muc tieu: xem Estimator 2 co giu duoc loi the toc do khi n lon hon,
DU cau truc van thua nhu Twitter (khong co tam giac nhu Facebook).

Chay tren Colab bang: !python3 wannacry_exact_vs_est2.py
(script nay chay nhu tien trinh con rieng, KHONG doc duoc bien
graphs_dir tu notebook - vi vay duong dan Drive duoc ghi thang
o day, sua lai neu ban dat ten thu muc khac.)
"""
import numpy as np, scipy.sparse as sp, time

repo_path = "/content/drive/MyDrive/orlab_hisp/MONSTOR-plus"
graphs_dir = f"{repo_path}/graphs"

def load_LT_graph(path):
    with open(path) as f:
        n, m = map(int, f.readline().split())
        src, dst, w = [], [], []
        for line in f:
            a, b, p = line.split()
            src.append(int(a)); dst.append(int(b)); w.append(float(p))
    W = sp.csr_matrix((w, (src, dst)), shape=(n, n))
    W.sort_indices()
    return W, n

def exact_diag(W, q):
    cur = W.copy(); diags = []
    for r in range(2, q+1):
        cur = cur @ W; diags.append(cur.diagonal())
    return np.stack(diags, axis=-1)

def hisp_vec(W, q, T, rng):
    n = W.shape[0]; acc = np.zeros((n, q-1))
    for t in range(T):
        z = rng.choice([-1.0, 1.0], size=n); y = z.copy()
        for l in range(1, q+1):
            y = W @ y
            if l >= 2: acc[:, l-2] += z * y
    return acc / T

rng = np.random.default_rng(0)
Q = 11
T = 1000

# So sanh ca 2 dataset Twitter da co de thay xu huong ro hon
for name in ["Extended_test_LT", "WannaCry_test_LT"]:
    W, n = load_LT_graph(f"{graphs_dir}/{name}.txt")
    print(f"\n{'='*60}\n{name}: n={n}, m={W.nnz}, bac TB={W.nnz/n:.1f}")

    t0 = time.perf_counter()
    C_exact = exact_diag(W, Q)
    t_exact = time.perf_counter() - t0
    print(f"  Tinh chinh xac: {t_exact:.2f}s")

    t0 = time.perf_counter()
    C_est2 = hisp_vec(W, Q, T, rng)
    t_est2 = time.perf_counter() - t0
    print(f"  Estimator 2 (T={T}): {t_est2:.2f}s")

    mask = C_exact > 0
    rel = np.abs(C_est2[mask] - C_exact[mask]) / C_exact[mask]
    print(f"  Sai so trung vi: {100*np.median(rel):.1f}%")

    faster = "Estimator 2" if t_est2 < t_exact else "Tinh chinh xac"
    ratio = t_exact / t_est2
    print(f"  => {faster} nhanh hon, ty le {ratio:.2f}x")
