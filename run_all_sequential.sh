#!/bin/bash
# H8 — Chạy TUẦN TỰ, từng lệnh một, không song song.
# Không cần ngồi canh: chạy 1 lần "nohup bash run_all_sequential.sh &"
# rồi đi ngủ, sáng dậy xem log là biết chạy tới đâu.
#
# Đã BỎ Extended/train/LT/random vì đã chạy xong trước đó.

cd ~/Documents/HISP/HISP

echo "===== BẮT ĐẦU — $(date) ====="

# --- Extended / LT (3 lệnh còn lại, đã bỏ train/random) ---
echo "--- Extended/train/LT/degree — $(date) ---"
./fast_monte_carlo_LT_degree graphs/Extended_train_LT.txt

echo "--- Extended/test/LT/random — $(date) ---"
./fast_monte_carlo_LT_random graphs/Extended_test_LT.txt

echo "--- Extended/test/LT/degree — $(date) ---"
./fast_monte_carlo_LT_degree graphs/Extended_test_LT.txt

# --- Celebrity / LT ---
echo "--- Celebrity/train/LT/random — $(date) ---"
./fast_monte_carlo_LT_random graphs/Celebrity_train_LT.txt

echo "--- Celebrity/train/LT/degree — $(date) ---"
./fast_monte_carlo_LT_degree graphs/Celebrity_train_LT.txt

echo "--- Celebrity/test/LT/random — $(date) ---"
./fast_monte_carlo_LT_random graphs/Celebrity_test_LT.txt

echo "--- Celebrity/test/LT/degree — $(date) ---"
./fast_monte_carlo_LT_degree graphs/Celebrity_test_LT.txt

# --- WannaCry / LT ---
echo "--- WannaCry/train/LT/random — $(date) ---"
./fast_monte_carlo_LT_random graphs/WannaCry_train_LT.txt

echo "--- WannaCry/train/LT/degree — $(date) ---"
./fast_monte_carlo_LT_degree graphs/WannaCry_train_LT.txt

echo "--- WannaCry/test/LT/random — $(date) ---"
./fast_monte_carlo_LT_random graphs/WannaCry_test_LT.txt

echo "--- WannaCry/test/LT/degree — $(date) ---"
./fast_monte_carlo_LT_degree graphs/WannaCry_test_LT.txt

# --- Celebrity / IC (BT, JI, LP) ---
echo "--- Celebrity/train/BT/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Celebrity_train_BT.txt
echo "--- Celebrity/train/BT/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Celebrity_train_BT.txt
echo "--- Celebrity/test/BT/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Celebrity_test_BT.txt
echo "--- Celebrity/test/BT/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Celebrity_test_BT.txt

echo "--- Celebrity/train/JI/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Celebrity_train_JI.txt
echo "--- Celebrity/train/JI/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Celebrity_train_JI.txt
echo "--- Celebrity/test/JI/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Celebrity_test_JI.txt
echo "--- Celebrity/test/JI/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Celebrity_test_JI.txt

echo "--- Celebrity/train/LP/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Celebrity_train_LP.txt
echo "--- Celebrity/train/LP/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Celebrity_train_LP.txt
echo "--- Celebrity/test/LP/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Celebrity_test_LP.txt
echo "--- Celebrity/test/LP/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Celebrity_test_LP.txt

# --- Extended / IC (BT, JI, LP) ---
echo "--- Extended/train/BT/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Extended_train_BT.txt
echo "--- Extended/train/BT/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Extended_train_BT.txt
echo "--- Extended/test/BT/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Extended_test_BT.txt
echo "--- Extended/test/BT/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Extended_test_BT.txt

echo "--- Extended/train/JI/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Extended_train_JI.txt
echo "--- Extended/train/JI/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Extended_train_JI.txt
echo "--- Extended/test/JI/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Extended_test_JI.txt
echo "--- Extended/test/JI/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Extended_test_JI.txt

echo "--- Extended/train/LP/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Extended_train_LP.txt
echo "--- Extended/train/LP/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Extended_train_LP.txt
echo "--- Extended/test/LP/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/Extended_test_LP.txt
echo "--- Extended/test/LP/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/Extended_test_LP.txt

# --- WannaCry / IC (BT, JI, LP) ---
echo "--- WannaCry/train/BT/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/WannaCry_train_BT.txt
echo "--- WannaCry/train/BT/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/WannaCry_train_BT.txt
echo "--- WannaCry/test/BT/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/WannaCry_test_BT.txt
echo "--- WannaCry/test/BT/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/WannaCry_test_BT.txt

echo "--- WannaCry/train/JI/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/WannaCry_train_JI.txt
echo "--- WannaCry/train/JI/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/WannaCry_train_JI.txt
echo "--- WannaCry/test/JI/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/WannaCry_test_JI.txt
echo "--- WannaCry/test/JI/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/WannaCry_test_JI.txt

echo "--- WannaCry/train/LP/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/WannaCry_train_LP.txt
echo "--- WannaCry/train/LP/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/WannaCry_train_LP.txt
echo "--- WannaCry/test/LP/random — $(date) ---"
./fast_monte_carlo_IC_random graphs/WannaCry_test_LP.txt
echo "--- WannaCry/test/LP/degree — $(date) ---"
./fast_monte_carlo_IC_degree graphs/WannaCry_test_LP.txt

echo "===== HOÀN TẤT TOÀN BỘ — $(date) ====="
