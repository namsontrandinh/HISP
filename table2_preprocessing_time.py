"""
Bang 2 (Table 2 - Preprocessing time comparison): so thoi gian + bo
nho + speedup giua 3 cach tinh c_r(v):
  1. Exact matrix-power features - tinh THANG, khong toi uu (dung
     cong thuc nguyen ban MONSTOR+, KHONG dung phep luoc node da toi
     uu rieng cho HISP - vi day la moc so sanh "truoc khi co HISP")
  2. Block-based MONSTOR+ features - dung dung ky thuat paper
     MONSTOR+ GOC mo ta (cong thuc 5, muc 3.3.1): chia cot thanh
     block, giam bo nho tu O(|V|^2) xuong O(|V|*d), KHONG doi do
     phuc tap thoi gian
  3. HISP (ca HISP-I va HISP-Vec, tach rieng 2 dong theo dung "chay
     ca 2, ghi ca 2" da thong nhat)

Do bo nho bang tracemalloc (do THAT, khong uoc luong).

Chay tren Colab: !python3 table2_preprocessing_time.py
"""
import time, tracemalloc
import numpy as np
import scipy.sparse as sp
from estimators import load_LT_graph, exact_diag, hisp_vec, PathSampler

Q = 11


def exact_matrix_power_naive(W, q):
    """Cach tinh THANG, khong toi uu gi (khong luoc node) - dung lam
    moc 1.0x cho speedup, dung dinh nghia goc paper MONSTOR+."""
    cur = W.copy()
    diags = []
    for _ in range(2, q + 1):
        cur = cur @ W
        diags.append(cur.diagonal())
    return np.stack(diags, axis=-1)


def block_based_diag(W, q, block_size=2000):
    """Ky thuat 'block-based' dung paper MONSTOR+ goc mo ta (cong
    thuc 5, muc 3.3.1): thay vi giu ca Diag(W^r) mot luc, chia cot
    thanh tung block kich thuoc d, tinh rieng tung block. Giam bo nho
    dinh (peak memory) xuong O(|V|*d) thay vi O(|V|^2), khong doi
    tong so phep tinh (paper: 'khong tang do phuc tap thoi gian tiem
    can vuot qua O(r|V|^3)')."""
    n = W.shape[0]
    out = np.zeros((n, q - 1))
    for i in range(0, n, block_size):
        d = min(block_size, n - i)
        cur_block = W[:, i:i + d]  # W[:, i:i+d], (n, d)
        for r_idx, r in enumerate(range(2, q + 1)):
            cur_block = W @ cur_block  # nhan lien tiep, (n, d)
            # lay duong cheo tuong ung: hang (i+j) cot j cua block
            for j in range(d):
                out[i + j, r_idx] = cur_block[i + j, j]
    return out


def measure(fn, *args, **kwargs):
    tracemalloc.start()
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, elapsed, peak / 1e6  # peak tinh bang MB


def run_on_dataset(name, path):
    print(f"\n{'='*78}\n{name}\n{'='*78}")
    W, n = load_LT_graph(path)
    print(f"n={n}, m={W.nnz}")

    C_exact, t_exact, mem_exact = measure(exact_matrix_power_naive, W, Q)
    print(f"Exact matrix-power (khong toi uu): {t_exact:8.2f}s   {mem_exact:8.1f}MB   1.00x")

    C_block, t_block, mem_block = measure(block_based_diag, W, Q, block_size=2000)
    match = np.allclose(C_exact, C_block)
    print(f"Block-based MONSTOR+ features    : {t_block:8.2f}s   {mem_block:8.1f}MB   "
          f"{t_exact/t_block:6.2f}x   (ket qua giong het exact: {match})")

    rng = np.random.default_rng(0)
    sampler = PathSampler(W)
    _, t_hisp1, mem_hisp1 = measure(sampler.estimate_all, Q, 1000, rng)
    print(f"HISP-I (s=1000)                  : {t_hisp1:8.2f}s   {mem_hisp1:8.1f}MB   {t_exact/t_hisp1:6.2f}x")

    rng = np.random.default_rng(0)
    _, t_hisp2, mem_hisp2 = measure(hisp_vec, W, Q, 1000, rng)
    print(f"HISP-Vec (T=1000)                : {t_hisp2:8.2f}s   {mem_hisp2:8.1f}MB   {t_exact/t_hisp2:6.2f}x")

    return {
        "Exact matrix-power features": (t_exact, mem_exact, 1.0),
        "Block-based MONSTOR+ features": (t_block, mem_block, t_exact/t_block),
        "HISP-I": (t_hisp1, mem_hisp1, t_exact/t_hisp1),
        "HISP-Vec": (t_hisp2, mem_hisp2, t_exact/t_hisp2),
    }


all_results = {}
datasets = [
    ("Extended_test_LT", "graphs/Extended_test_LT.txt"),
    ("Celebrity_test_LT", "graphs/Celebrity_test_LT.txt"),
    ("WannaCry_test_LT", "graphs/WannaCry_test_LT.txt"),
]
for name, path in datasets:
    all_results[name] = run_on_dataset(name, path)

print(f"\n\n{'='*78}\nBANG 2 TONG HOP (dinh dang giong Table 2 trong paper)\n{'='*78}")
print(f"{'Dataset':<20}{'Method':<32}{'Time (s)':<12}{'Memory (MB)':<14}{'Speedup'}")
for name, res in all_results.items():
    for method, (t, mem, speedup) in res.items():
        print(f"{name:<20}{method:<32}{t:<12.2f}{mem:<14.1f}{speedup:.2f}x")
