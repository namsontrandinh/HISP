"""
Trien khai tau_d nhu co Dung huong dan: chia V thanh V_exact (bac <
tau_d, tinh chinh xac) va V_estimate (bac >= tau_d, uoc luong).
tau_d = bac trung binh cua do thi. Thu ca 2 lua chon "bac" (vao/ra,
vi do thi co huong) va do hoi tu de dua ra goi y.

Can co estimators.py cung thu muc.
Chay tren Colab bang: !python3 test_tau_d.py
"""
import numpy as np, time
from estimators import load_LT_graph, exact_diag, hisp_vec

def hybrid_estimate(W, q, tau_d, degree_type, T, rng):
    """Chia V theo tau_d, tinh V_exact chinh xac, V_estimate bang
    hisp_vec. Tra ve (ket qua gop, thoi gian, V_exact_size)."""
    n = W.shape[0]
    outd = np.asarray(W.sum(axis=1)).ravel()
    ind = np.asarray(W.sum(axis=0)).ravel()
    deg = outd if degree_type == "out" else ind

    is_exact = deg < tau_d
    n_exact = is_exact.sum()

    t0 = time.perf_counter()
    # V_exact: tinh chinh xac CHO TOAN BO do thi (don gian, dung
    # W day du), roi chi lay dong tuong ung V_exact
    C_full_exact = exact_diag(W, q)  # da toi uu (prune=True)
    # V_estimate: uoc luong bang hisp_vec cho toan bo, roi lay
    # dong tuong ung V_estimate
    C_full_est = hisp_vec(W, q, T, rng)
    t_total = time.perf_counter() - t0

    C_hybrid = np.where(is_exact[:, None], C_full_exact, C_full_est)
    return C_hybrid, t_total, n_exact


rng_base = np.random.default_rng(0)
Q = 11
T = 1000

for name in ["Extended_test_LT", "WannaCry_test_LT"]:
    W, n = load_LT_graph(f"/content/drive/MyDrive/orlab_hisp/MONSTOR-plus/graphs/{name}.txt")
    outd = np.asarray(W.sum(axis=1)).ravel()
    ind = np.asarray(W.sum(axis=0)).ravel()
    tau_out = outd.mean()
    tau_in = ind.mean()

    print(f"\n{'='*70}")
    print(f"{name}: n={n}")
    print(f"  bac ra trung binh (tau_out) = {tau_out:.3f}")
    print(f"  bac vao trung binh (tau_in) = {tau_in:.3f}")

    C_exact_true = exact_diag(W, Q)
    mask = C_exact_true > 0

    for degree_type, tau_d in [("out", tau_out), ("in", tau_in)]:
        rng = np.random.default_rng(0)
        C_hybrid, t_total, n_exact = hybrid_estimate(W, Q, tau_d, degree_type, T, rng)
        rel = np.abs(C_hybrid[mask] - C_exact_true[mask]) / C_exact_true[mask]
        err = 100 * np.median(rel)
        print(f"\n  --- tau_d = bac {degree_type} trung binh ({tau_d:.2f}) ---")
        print(f"    |V_exact| = {n_exact}/{n} ({100*n_exact/n:.1f}%)")
        print(f"    Thoi gian: {t_total:.2f}s")
        print(f"    Sai so trung vi (toan bo V, ca 2 nhom gop lai): {err:.1f}%")
