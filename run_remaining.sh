#!/bin/bash
# H8 — Chay phan CON THIEU, dung binary moi (TEST_COUNT=1000).
# Tuan tu, khong chay song song, khong can ngoi canh.
#
# DA XONG (khong co trong file nay):
#   Extended_train_LT (4000), Extended_test_LT (4000) - tham so CU
#   Celebrity_test_LT (4000) - tham so CU
#   Celebrity_train_LT: da co random (2000) - tham so CU, CHi thieu degree
#   WannaCry_test_LT: da co random (2000) - tham so CU, CHi thieu degree
#
# LUU Y: 2 dong "lap phan thieu" ben duoi dung binary MOI (s=1000),
# trong khi phan random cung thu muc do da sinh bang tham so CU
# (s=100000). Khong gay loi gi - GNN van hoc binh thuong, chi la
# nhieu khong deu giua cac mau trong cung 1 thu muc.

cd ~/Documents/HISP/HISP

echo "===== BAT DAU — $(date) ====="

# --- Lap phan LT con thieu ---
echo "--- Celebrity/train/LT/degree (lap phan thieu) — $(date) ---"
./fast_monte_carlo_LT_degree graphs/Celebrity_train_LT.txt

echo "--- WannaCry/test/LT/degree (lap phan thieu) — $(date) ---"
./fast_monte_carlo_LT_degree graphs/WannaCry_test_LT.txt

echo "--- WannaCry/train/LT/random (sinh lai tu dau) — $(date) ---"
./fast_monte_carlo_LT_random graphs/WannaCry_train_LT.txt

echo "--- WannaCry/train/LT/degree (sinh lai tu dau) — $(date) ---"
./fast_monte_carlo_LT_degree graphs/WannaCry_train_LT.txt

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

echo "===== HOAN TAT TOAN BO — $(date) ====="
