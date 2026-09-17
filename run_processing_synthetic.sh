#!/bin/bash
# processing.py cho 130 do thi tong hop - CHI can goi 1 lan/do thi
# (khong can train+test rieng nhu Extended, vi day la du lieu CHI
# dung de TRAIN theo chi dao cua co Dung - khong dung de test).
#
# Xu ly xong do thi nao, xoa .txt tho do thi do NGAY - tranh lap lai
# khung hoang het dia da gap voi Extended (hien chi con 48GB).

cd ~/Documents/HISP/HISP
source venv_hisp/bin/activate

check_disk() {
    avail=$(df --output=avail -k ~ | tail -1)
    avail_gb=$((avail / 1024 / 1024))
    if [ "$avail_gb" -lt 3 ]; then
        echo "!!! DIA CON DUOI 3GB (${avail_gb}GB) - DUNG LAI NGAY !!!"
        exit 1
    fi
}

count=0
total=$(ls graphs/synth-*_train_LT.txt 2>/dev/null | wc -l)

if [ "$total" -eq 0 ]; then
    echo "!!! KHONG TIM THAY graphs/synth-*_train_LT.txt - kiem tra lai buoc doi ten !!!"
    exit 1
fi

echo "===== BAT DAU processing $total do thi tong hop — $(date) ====="

for graph_file in graphs/synth-*_train_LT.txt; do
    combo=$(basename "$graph_file" .txt)   # vd: synth-small-ba-000_train_LT
    count=$((count + 1))
    echo "--- [$count/$total] $combo — $(date) ---"
    check_disk

    python processing.py "$combo"
    status=$?

    if [ $status -ne 0 ]; then
        echo "  !!! LOI xu ly $combo (exit $status) - DUNG LAI, KHONG xoa raw_data !!!"
        exit 1
    fi

    sample_file="datadir/${combo}_X_random.pkl.gz"
    if [ ! -s "$sample_file" ]; then
        echo "  !!! File output '$sample_file' RONG - DUNG LAI, KHONG xoa raw_data !!!"
        exit 1
    fi

    echo "  -> OK, xoa raw_data/$combo va graphs/${combo}.txt"
    rm -rf "raw_data/$combo"

    avail=$(df --output=avail -k ~ | tail -1)
    avail_gb=$((avail / 1024 / 1024))
    echo "  -> Dia con trong: ${avail_gb}GB"
done

echo ""
echo "===== HOAN TAT $total do thi — $(date) ====="
ls datadir/ | grep -c "^synth-"