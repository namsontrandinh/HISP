"""
Do anh huong THAT (Monte Carlo, 100.000 lan mo phong) cho 2 seed set
da lay tu IM.py (MONSTOR+ va HISP-Est1) tren Extended_test_LT.

test_LT.cpp tinh MOT LAN duy nhat ra ket qua cho MOI muc k=10..100
(buoc 10) - khong can chay rieng cho tung k=10/20/30/50.

Chay tren PC (can binary test_LT da build san tu H8):
    python3 measure_IM.py
"""
import subprocess, re

MONSTOR_SEEDS = [1449,3385,3814,2094,971,4284,5334,917,5201,3386,2,226,24,267,372,
    2624,334,4287,0,9,25,29,30,42,43,45,46,47,48,49,50,53,54,55,61,62,63,64,65,
    66,67,68,69,70,71,72,73,74,76,77,78,80,81,82,83,84,85,86,87,90,91,92,94,95,
    96,97,100,101,102,104,105,108,110,111,113,115,120,122,124,125,126,127,128,
    129,130,131,132,134,135,136,137,138,139,140,141,143,145,148,149,150]

EST1_SEEDS = [3385,1449,2094,4707,4328,3817,1225,3299,1804,4514,5334,4180,3866,
    126,3429,1000,1260,2342,503,4356,2078,5201,920,829,4055,1266,1337,3158,3054,
    3048,4109,0,1,3,6,8,10,13,17,19,20,21,22,23,25,26,29,30,33,34,35,37,38,40,
    41,42,43,45,46,47,48,49,50,53,54,55,59,64,69,74,80,84,91,97,102,112,118,123,
    128,131,134,137,141,145,148,151,154,159,162,167,169,171,174,178,181,185,193,
    199,201,204]

assert len(MONSTOR_SEEDS) == 100, f"MONSTOR+ can dung 100 seed, dang co {len(MONSTOR_SEEDS)}"
assert len(EST1_SEEDS) == 100, f"HISP-Est1 can dung 100 seed, dang co {len(EST1_SEEDS)}"

GRAPH_FILE = "graphs/Extended_test_LT.txt"
TEST_LT_BIN = "./test_LT"


def write_seed_file(seeds, path):
    with open(path, "w") as f:
        f.write("\n".join(map(str, seeds)))


def run_test_LT(seeds, tag):
    seed_file = f"seed_{tag}.txt"
    write_seed_file(seeds, seed_file)
    print(f"Dang chay test_LT cho {tag} (mat vai phut, 100.000 mo phong moi muc k)...")
    out = subprocess.run([TEST_LT_BIN, GRAPH_FILE, seed_file],
                          capture_output=True, text=True, timeout=1800)
    results = {}
    for line in out.stdout.splitlines():
        m = re.match(r"k=(\d+): average influence is ([\d.]+)", line)
        if m:
            results[int(m.group(1))] = float(m.group(2))
    if not results:
        print(f"  LOI: khong parse duoc ket qua nao. stdout={out.stdout[:300]} stderr={out.stderr[:300]}")
    return results


monstor_results = run_test_LT(MONSTOR_SEEDS, "monstor")
est1_results = run_test_LT(EST1_SEEDS, "est1")

print(f"\n{'='*60}")
print(f"{'k':<6}{'MONSTOR+ (that)':<20}{'HISP-Est1 (that)':<20}{'Chenh lech'}")
print(f"{'-'*60}")
for k in sorted(monstor_results):
    m_val = monstor_results.get(k, float('nan'))
    e_val = est1_results.get(k, float('nan'))
    diff_pct = 100 * (e_val - m_val) / m_val if m_val else float('nan')
    marker = "  <-- vung tin hieu that (theo phan tich seed set)" if k <= 20 else ""
    print(f"{k:<6}{m_val:<20.3f}{e_val:<20.3f}{diff_pct:+.2f}%{marker}")
