#!/bin/bash
# Sinh Monte Carlo cho 130 do thi tong hop (graphs/synth_*_LT.txt).
#
# DA SUA 2 LOI PHAT HIEN KHI TU KIEM CHUNG (khong doan, da chay binary
# that de bat loi):
#   1. File .txt PHAI nam trong graphs/ (khong phai thu muc rieng) -
#      code C++ hardcode gia dinh tien to "graphs/" dai 7 ky tu de
#      cat chuoi tinh ten thu muc output; thu muc khac ten se lam
#      tinh sai ten, gay Segmentation fault am tham.
#   2. PHAI tu tao truoc raw_data/<ten>/ cho TUNG do thi - code C++
#      khong tu mkdir (da biet tu vu WannaCry/Celebrity truoc day,
#      nhung ban dau quen ap dung lai o day, da tu bat loi va sua).

cd ~/Documents/HISP/HISP

check_disk() {
    avail=$(df --output=avail -k ~ | tail -1)
    avail_gb=$((avail / 1024 / 1024))
    if [ "$avail_gb" -lt 3 ]; then
        echo "!!! DIA CON DUOI 3GB (${avail_gb}GB) - DUNG LAI NGAY !!!"
        exit 1
    fi
}

mkdir -p raw_data
count=0
total=$(ls graphs/synth_*_LT.txt 2>/dev/null | wc -l)

if [ "$total" -eq 0 ]; then
    echo "!!! KHONG TIM THAY file graphs/synth_*_LT.txt - kiem tra da giai nen dung cho chua !!!"
    exit 1
fi

echo "===== BAT DAU sinh Monte Carlo cho $total do thi tong hop — $(date) ====="

for graph_file in graphs/synth_*_LT.txt; do
    name=$(basename "$graph_file" .txt)
    count=$((count + 1))
    echo "--- [$count/$total] $name — $(date) ---"
    check_disk
    mkdir -p "raw_data/$name"     # BAT BUOC - code C++ khong tu tao
    ./fast_monte_carlo_LT_random "$graph_file"
    ./fast_monte_carlo_LT_degree "$graph_file"
done

echo "===== HOAN TAT $total do thi — $(date) ====="
echo "Kiem tra nhanh so thu muc da sinh:"
ls raw_data/ | grep -c "^synth_"
