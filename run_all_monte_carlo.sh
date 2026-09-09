#!/bin/bash
# H8 — Chạy sinh dữ liệu Monte Carlo, từng lệnh liệt kê riêng (không vòng lặp)
# Chạy nền (nohup + &) để không mất khi AnyDesk rớt kết nối.
# Mỗi lệnh ghi log riêng, tên khớp file graph, dễ tra khi cần xem tiến độ.

cd ~/Documents/HISP/HISP

# ============================================================
# MODEL LT (dùng fast_monte_carlo_LT_random / fast_monte_carlo_LT_degree)
# ============================================================

# --- Celebrity ---
nohup ./fast_monte_carlo_LT_random graphs/Celebrity_train_LT.txt > log_Celebrity_train_LT_random.txt 2>&1 &
nohup ./fast_monte_carlo_LT_degree graphs/Celebrity_train_LT.txt > log_Celebrity_train_LT_degree.txt 2>&1 &
nohup ./fast_monte_carlo_LT_random graphs/Celebrity_test_LT.txt  > log_Celebrity_test_LT_random.txt  2>&1 &
nohup ./fast_monte_carlo_LT_degree graphs/Celebrity_test_LT.txt  > log_Celebrity_test_LT_degree.txt  2>&1 &

# --- Extended ---
nohup ./fast_monte_carlo_LT_random graphs/Extended_train_LT.txt > log_Extended_train_LT_random.txt 2>&1 &
nohup ./fast_monte_carlo_LT_degree graphs/Extended_train_LT.txt > log_Extended_train_LT_degree.txt 2>&1 &
nohup ./fast_monte_carlo_LT_random graphs/Extended_test_LT.txt  > log_Extended_test_LT_random.txt  2>&1 &
nohup ./fast_monte_carlo_LT_degree graphs/Extended_test_LT.txt  > log_Extended_test_LT_degree.txt  2>&1 &

# --- WannaCry ---
nohup ./fast_monte_carlo_LT_random graphs/WannaCry_train_LT.txt > log_WannaCry_train_LT_random.txt 2>&1 &
nohup ./fast_monte_carlo_LT_degree graphs/WannaCry_train_LT.txt > log_WannaCry_train_LT_degree.txt 2>&1 &
nohup ./fast_monte_carlo_LT_random graphs/WannaCry_test_LT.txt  > log_WannaCry_test_LT_random.txt  2>&1 &
nohup ./fast_monte_carlo_LT_degree graphs/WannaCry_test_LT.txt  > log_WannaCry_test_LT_degree.txt  2>&1 &

# ============================================================
# MODEL IC (dùng fast_monte_carlo_IC_random / fast_monte_carlo_IC_degree)
# 3 loại xác suất: BT, JI, LP — mỗi loại là 1 activation probability
# matrix khác nhau (đúng paper MONSTOR+ gốc mục 2.1)
# ============================================================

# --- Celebrity / BT ---
nohup ./fast_monte_carlo_IC_random graphs/Celebrity_train_BT.txt > log_Celebrity_train_BT_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Celebrity_train_BT.txt > log_Celebrity_train_BT_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/Celebrity_test_BT.txt  > log_Celebrity_test_BT_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Celebrity_test_BT.txt  > log_Celebrity_test_BT_degree.txt  2>&1 &

# --- Celebrity / JI ---
nohup ./fast_monte_carlo_IC_random graphs/Celebrity_train_JI.txt > log_Celebrity_train_JI_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Celebrity_train_JI.txt > log_Celebrity_train_JI_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/Celebrity_test_JI.txt  > log_Celebrity_test_JI_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Celebrity_test_JI.txt  > log_Celebrity_test_JI_degree.txt  2>&1 &

# --- Celebrity / LP ---
nohup ./fast_monte_carlo_IC_random graphs/Celebrity_train_LP.txt > log_Celebrity_train_LP_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Celebrity_train_LP.txt > log_Celebrity_train_LP_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/Celebrity_test_LP.txt  > log_Celebrity_test_LP_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Celebrity_test_LP.txt  > log_Celebrity_test_LP_degree.txt  2>&1 &

# --- Extended / BT ---
nohup ./fast_monte_carlo_IC_random graphs/Extended_train_BT.txt > log_Extended_train_BT_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Extended_train_BT.txt > log_Extended_train_BT_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/Extended_test_BT.txt  > log_Extended_test_BT_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Extended_test_BT.txt  > log_Extended_test_BT_degree.txt  2>&1 &

# --- Extended / JI ---
nohup ./fast_monte_carlo_IC_random graphs/Extended_train_JI.txt > log_Extended_train_JI_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Extended_train_JI.txt > log_Extended_train_JI_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/Extended_test_JI.txt  > log_Extended_test_JI_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Extended_test_JI.txt  > log_Extended_test_JI_degree.txt  2>&1 &

# --- Extended / LP ---
nohup ./fast_monte_carlo_IC_random graphs/Extended_train_LP.txt > log_Extended_train_LP_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Extended_train_LP.txt > log_Extended_train_LP_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/Extended_test_LP.txt  > log_Extended_test_LP_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/Extended_test_LP.txt  > log_Extended_test_LP_degree.txt  2>&1 &

# --- WannaCry / BT ---
nohup ./fast_monte_carlo_IC_random graphs/WannaCry_train_BT.txt > log_WannaCry_train_BT_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/WannaCry_train_BT.txt > log_WannaCry_train_BT_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/WannaCry_test_BT.txt  > log_WannaCry_test_BT_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/WannaCry_test_BT.txt  > log_WannaCry_test_BT_degree.txt  2>&1 &

# --- WannaCry / JI ---
nohup ./fast_monte_carlo_IC_random graphs/WannaCry_train_JI.txt > log_WannaCry_train_JI_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/WannaCry_train_JI.txt > log_WannaCry_train_JI_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/WannaCry_test_JI.txt  > log_WannaCry_test_JI_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/WannaCry_test_JI.txt  > log_WannaCry_test_JI_degree.txt  2>&1 &

# --- WannaCry / LP ---
nohup ./fast_monte_carlo_IC_random graphs/WannaCry_train_LP.txt > log_WannaCry_train_LP_random.txt 2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/WannaCry_train_LP.txt > log_WannaCry_train_LP_degree.txt 2>&1 &
nohup ./fast_monte_carlo_IC_random graphs/WannaCry_test_LP.txt  > log_WannaCry_test_LP_random.txt  2>&1 &
nohup ./fast_monte_carlo_IC_degree graphs/WannaCry_test_LP.txt  > log_WannaCry_test_LP_degree.txt  2>&1 &

echo "Đã khởi chạy nền toàn bộ 48 tiến trình. Xem: jobs -l  hoặc  ps aux | grep fast_monte_carlo"
