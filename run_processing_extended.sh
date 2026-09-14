#!/bin/bash
# Chay processing.py cho Extended (dataset DUY NHAT da xong 100%).
# Moi lenh tu dong xu ly CA random lan degree ben trong (khong can
# goi rieng) - da xac nhan qua doc code processing.py that.
#
# train: doc idx 1-1600 (random), 1601-2000 (val random),
#        2001-3600 (degree), 3601-4000 (val degree) = du 4000 file
# test:  doc idx 1-2000 (random), 2001-4000 (degree) = du 4000 file

cd ~/Documents/HISP/HISP
source venv_hisp/bin/activate

check_disk() {
    avail=$(df --output=avail -k ~ | tail -1)
    avail_gb=$((avail / 1024 / 1024))
    echo "  [Dia con trong: ${avail_gb}GB]"
    if [ "$avail_gb" -lt 1 ]; then
        echo "  !!! DIA GAN HET (<1GB) - DUNG LAI, kiem tra ngay !!!"
        exit 1
    fi
}

echo "===== BAT DAU processing Extended — $(date) ====="

for combo in Extended_train_LT Extended_test_LT \
             Extended_train_BT Extended_test_BT \
             Extended_train_JI Extended_test_JI \
             Extended_train_LP Extended_test_LP; do
    echo "--- $combo — $(date) ---"
    check_disk
    python processing.py "$combo"
done

echo "===== HOAN TAT — $(date) ====="
ls -la datadir/ | grep Extended
