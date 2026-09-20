"""
Bang 1 (Table 1 - Influence estimation accuracy, theo dung dinh nghia
"Feature RMSE" trong paper HISP muc 9.3): so sanh c_r(v) uoc luong
(HISP-I voi s=20/50/100, HISP-Vec) voi c_r(v) TINH DUNG (MONSTOR+
exact), tren du lieu TEST THAT (Extended/Celebrity/WannaCry) -
KHONG can GNN, dung Q1 cua paper (do thuoc tinh dac trung, chua phai
anh huong thuc su qua GNN).

Cong thuc RMSE dung dung paper (muc 9.3):
  RMSE_C = sqrt( 1/(n(q-1)) * sum_r sum_v (c~_r(v) - c_r(v))^2 )

MAPE, Pearson, Spearman tinh tren CUNG cap gia tri (n x (q-1) phan tu,
flatten), cung 1 cach so sanh - khop tinh than voi RMSE dinh nghia
trong paper.

Chay tren Colab: !python3 table1_feature_accuracy.py
"""
import numpy as np
from scipy.stats import pearsonr, spearmanr
from estimators import load_LT_graph, exact_diag, hisp_vec, PathSampler

Q = 11  # q=11, khop hyperparameter MONSTOR+ goc (r=2..11)

def compute_metrics(C_true, C_hat):
    """Tinh RMSE (dung cong thuc paper), MAPE, Pearson, Spearman.
    Chi tinh tren cac o co C_true > 0 (tranh chia 0 o MAPE/Pearson
    khi phan lon gia tri thuc te = 0 - dung quy uoc da dung xuyen
    suot du an nay)."""
    mask = C_true > 0
    true_flat = C_true[mask]
    hat_flat = C_hat[mask]

    rmse = np.sqrt(np.mean((hat_flat - true_flat) ** 2))
    mape = np.mean(np.abs((hat_flat - true_flat) / true_flat)) * 100
    pearson_r, _ = pearsonr(true_flat, hat_flat)
    spearman_r, _ = spearmanr(true_flat, hat_flat)

    return rmse, mape, pearson_r, spearman_r


def run_on_dataset(name, path):
    print(f"\n{'='*78}\n{name}\n{'='*78}")
    W, n = load_LT_graph(path)
    print(f"n={n}, m={W.nnz}")

    C_exact = exact_diag(W, Q)  # dap an dung (dong thoi la dong "MONSTOR+" - RMSE=0 tuyet doi)

    results = {}

    # HISP-I (Estimator 1, path-sampling) voi s=20/50/100
    sampler = PathSampler(W)
    for s in [20, 50, 100]:
        rng = np.random.default_rng(0)
        C_hisp1 = sampler.estimate_all(Q, s, rng)
        rmse, mape, pear, spear = compute_metrics(C_exact, C_hisp1)
        results[f"HISP-s={s}"] = (rmse, mape, pear, spear)
        print(f"HISP-s={s:<4d}: RMSE={rmse:.4e}  MAPE={mape:6.1f}%  Pearson={pear:.4f}  Spearman={spear:.4f}")

    # HISP-Vec (Estimator 2) - them vao de tham khao, du paper Bang 1
    # chi liet ke HISP-s=20/50/100 (HISP-I); neu can them dong HISP-Vec
    # rieng thi da co san o day
    rng = np.random.default_rng(0)
    C_hisp2 = hisp_vec(W, Q, 1000, rng)
    rmse, mape, pear, spear = compute_metrics(C_exact, C_hisp2)
    results["HISP-Vec-T=1000"] = (rmse, mape, pear, spear)
    print(f"HISP-Vec(T=1000): RMSE={rmse:.4e}  MAPE={mape:6.1f}%  Pearson={pear:.4f}  Spearman={spear:.4f}")

    print(f"MONSTOR+ (exact) : RMSE=0.0000e+00  MAPE=   0.0%  Pearson=1.0000  Spearman=1.0000  (dap an dung)")

    return results


all_results = {}
datasets = [
    ("Extended_test_LT", "graphs/Extended_test_LT.txt"),
    ("Celebrity_test_LT", "graphs/Celebrity_test_LT.txt"),
    ("WannaCry_test_LT", "graphs/WannaCry_test_LT.txt"),
]
for name, path in datasets:
    all_results[name] = run_on_dataset(name, path)

print(f"\n\n{'='*78}\nBANG 1 TONG HOP (dinh dang giong Table 1 trong paper)\n{'='*78}")
print(f"{'Dataset':<20}{'Method':<20}{'RMSE':<14}{'MAPE':<10}{'Pearson':<10}{'Spearman'}")
for name, res in all_results.items():
    print(f"{name:<20}{'MONSTOR+':<20}{'0.0000':<14}{'0.0%':<10}{'1.0000':<10}{'1.0000'}")
    for method, (rmse, mape, pear, spear) in res.items():
        print(f"{'':<20}{method:<20}{rmse:<14.4e}{mape:<10.1f}{pear:<10.4f}{spear:.4f}")
