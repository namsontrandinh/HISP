#!/bin/bash
# H8 — Sinh dữ liệu Monte Carlo, chia theo cụm (dataset x mô hình xác suất).
# Mỗi cụm dùng vòng lặp (train/test x random/degree = 4 tiến trình chạy nền).
# Có "wait" cuối mỗi cụm -> cụm sau chỉ bắt đầu khi cụm trước xong hẳn,
# tránh chạy 48 tiến trình cùng lúc làm quá tải máy 16GB/1 GPU.
#
# RIÊNG Extended/LT: KHÔNG có trong file này. Bạn tự chạy tay từng dòng
# để bỏ qua dòng đang chạy dở, theo đúng ý đã thống nhất.

cd ~/Documents/HISP/HISP

run_cluster () {
    local graph=$1 prob=$2 binprefix=$3
    echo "===== Cụm: ${graph} / ${prob} ====="
    for split in train test; do
        for kind in random degree; do
            nohup ./${binprefix}_${kind} graphs/${graph}_${split}_${prob}.txt \
                > log_${graph}_${split}_${prob}_${kind}.txt 2>&1 &
        done
    done
    wait   # đợi cả 4 tiến trình của cụm này xong mới sang cụm sau
    echo "===== Xong cụm: ${graph} / ${prob} ====="
}

# ============================================================
# MODEL LT — chỉ Celebrity, WannaCry (Extended/LT bạn tự chạy tay)
# ============================================================
run_cluster Celebrity LT fast_monte_carlo_LT
run_cluster WannaCry  LT fast_monte_carlo_LT

# ============================================================
# MODEL IC — Celebrity / Extended / WannaCry, mỗi cái x BT/JI/LP
# ============================================================
run_cluster Celebrity BT fast_monte_carlo_IC
run_cluster Celebrity JI fast_monte_carlo_IC
run_cluster Celebrity LP fast_monte_carlo_IC

run_cluster Extended  BT fast_monte_carlo_IC
run_cluster Extended  JI fast_monte_carlo_IC
run_cluster Extended  LP fast_monte_carlo_IC

run_cluster WannaCry  BT fast_monte_carlo_IC
run_cluster WannaCry  JI fast_monte_carlo_IC
run_cluster WannaCry  LP fast_monte_carlo_IC

echo "HOÀN TẤT toàn bộ các cụm (trừ Extended/LT bạn tự chạy tay)."
