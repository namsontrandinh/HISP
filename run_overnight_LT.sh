#!/bin/bash
# H8 — Chạy qua đêm: 2 cụm NẶNG NHẤT (Celebrity/LT, WannaCry/LT).
# Extended/LT bạn tự chạy tay (đã làm riêng train/random).
# Các cụm IC (BT/JI/LP, nhẹ hơn nhiều) để dành chạy tay ban ngày sau.

cd ~/Documents/HISP/HISP

run_cluster () {
    local graph=$1 prob=$2 binprefix=$3
    echo "===== Bắt đầu cụm: ${graph} / ${prob} — $(date) ====="
    for split in train test; do
        for kind in random degree; do
            nohup ./${binprefix}_${kind} graphs/${graph}_${split}_${prob}.txt \
                > log_${graph}_${split}_${prob}_${kind}.txt 2>&1 &
        done
    done
    wait
    echo "===== Xong cụm: ${graph} / ${prob} — $(date) ====="
}

run_cluster Celebrity LT fast_monte_carlo_LT
run_cluster WannaCry  LT fast_monte_carlo_LT

echo "===== HOÀN TẤT toàn bộ chạy qua đêm — $(date) ====="
