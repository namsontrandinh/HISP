"""
Do tau_d cho HISP-I tren Extended (dataset dang dung cho phan IM).

Dua nguyen logic da kiem chung truoc do (test_tau_d.py), CHi doi phan
uoc luong tu hisp_vec() sang PathSampler (HISP-I) - moi phan khac giu
nguyen (cach chia V_exact/V_estimate theo bac ra, cach do sai so).

Chay tren Colab: !python3 tau_d_hisp1.py
(can estimators.py + graphs/Extended_test_LT.txt cung thu muc)
"""
import numpy as np, time
from estimators import load_LT_graph, exact_diag, PathSampler

def hybrid_estimate_hisp1(W, q, tau_d, s, rng):
    """Giong het ham hybrid_estimate() da dung cho HISP-Vec truoc do,
    chi doi buoc uoc luong sang PathSampler (HISP-I)."""
    n = W.shape[0]
    outd = np.asarray(W.sum(axis=1)).ravel()
    is_exact = outd < tau_d
    n_exact = is_exact.sum()

    t0 = time.perf_counter()
    C_full_exact = exact_diag(W, q)          # V_exact: tinh dung
    sampler = PathSampler(W)
    C_full_est = sampler.estimate_all(q, s, rng)   # V_estimate: HISP-I
    t_total = time.perf_counter() - t0

    C_hybrid = np.where(is_exact[:, None], C_full_exact, C_full_est)
    return C_hybrid, t_total, n_exact


Q = 11
S = 1000  # khop voi s da dung khi train checkpoint HISP-Est1

W, n = load_LT_graph("graphs/Extended_test_LT.txt")
outd = np.asarray(W.sum(axis=1)).ravel()
tau_out = outd.mean()

print(f"Extended_test_LT: n={n}")
print(f"tau_d (bac ra trung binh) = {tau_out:.4f}")

C_exact_true = exact_diag(W, Q)
mask = C_exact_true > 0

rng = np.random.default_rng(0)
C_hybrid, t_total, n_exact = hybrid_estimate_hisp1(W, Q, tau_out, S, rng)
rel = np.abs(C_hybrid[mask] - C_exact_true[mask]) / C_exact_true[mask]
err = 100 * np.median(rel)

print(f"\n=== KET QUA tau_d cho HISP-I tren Extended ===")
print(f"tau_d = {tau_out:.4f}")
print(f"|V_exact| = {n_exact}/{n} ({100*n_exact/n:.1f}%)")
print(f"Thoi gian: {t_total:.2f}s")
print(f"Sai so trung vi (toan bo V, ca 2 nhom gop lai): {err:.1f}%")

print(f"\n=== Doi chieu voi tau_d da co san cho HISP-Vec (do truoc do) ===")
print(f"tau_d (HISP-Vec, Extended) = 0.9210  (dung boi bac ra trung binh - cung cong thuc)")
print(f"=> Ca 2 estimator DUNG CHUNG 1 gia tri tau_d (vi tau_d chi phu thuoc")
print(f"   vao do thi, khong phu thuoc estimator nao duoc dung ben trong)")
