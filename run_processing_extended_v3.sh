#!/bin/bash
# Ban v3: xu ly TUNG combo, XOA raw_data/.txt THO NGAY sau khi
# processing.py ghi file .pkl.gz thanh cong - giai phong dia lien tuc,
# khong doi tich luy het 8 combo moi xoa 1 lan (da hoc tu su co dia day).

cd ~/Documents/HISP/HISP
source venv_hisp/bin/activate

run_one() {
    combo=$1
    echo "===== $combo — $(date) ====="
    python processing.py "$combo"
    status=$?

    if [ $status -ne 0 ]; then
        echo "  !!! LOI khi xu ly $combo (exit code $status) - DUNG LAI, KHONG xoa raw_data !!!"
        exit 1
    fi

    # Kiem tra file output thuc su co noi dung (khong phai 0 byte)
    sample_file="datadir/${combo}_X_random.pkl.gz"
    if [ ! -s "$sample_file" ]; then
        echo "  !!! File output '$sample_file' RONG hoac khong ton tai - DUNG LAI, KHONG xoa raw_data !!!"
        exit 1
    fi

    echo "  -> OK, xoa raw_data/$combo (da xu ly xong, khong con can .txt tho)"
    rm -rf "raw_data/$combo"

    avail=$(df --output=avail -k ~ | tail -1)
    avail_gb=$((avail / 1024 / 1024))
    used_datadir=$(du -sh datadir/ 2>/dev/null | cut -f1)
    echo "  -> Dia con trong: ${avail_gb}GB | datadir/ hien chiem: $used_datadir"

    if [ "$avail_gb" -lt 2 ]; then
        echo "  !!! CANH BAO: dia con duoi 2GB - DUNG LAI NGAY !!!"
        exit 1
    fi
}

# Extended_test_LT DA XONG roi (chay o buoc truoc) - bo qua, chi xoa raw_data neu con
if [ -d "raw_data/Extended_test_LT" ]; then
    echo "Don raw_data/Extended_test_LT (da processing xong tu buoc truoc)"
    rm -rf raw_data/Extended_test_LT
fi

run_one Extended_train_LT
run_one Extended_train_BT
run_one Extended_test_BT
run_one Extended_train_JI
run_one Extended_test_JI
run_one Extended_train_LP
run_one Extended_test_LP

echo ""
echo "===== HOAN TAT TOAN BO 8 COMBO — $(date) ====="
ls -la datadir/ | grep Extended
