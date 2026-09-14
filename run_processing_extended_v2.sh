#!/bin/bash
# Ban AN TOAN: chay TUNG LENH MOT, dung lai VA BAO CAO sau moi lenh de
# ban tu quyet dinh co chay tiep khong - khong tin vao uoc tinh, kiem
# tra dung luong THAT sau moi buoc (uoc tinh truoc chi ~20.2GB, RAT SIT
# SAO so voi 21GB dang co, sai so du nho cung co the lam day dia lai).

cd ~/Documents/HISP/HISP
source venv_hisp/bin/activate

run_one() {
    combo=$1
    echo "===== $combo — $(date) ====="
    python processing.py "$combo"
    avail=$(df --output=avail -k ~ | tail -1)
    avail_gb=$((avail / 1024 / 1024))
    used_datadir=$(du -sh datadir/ 2>/dev/null | cut -f1)
    echo "  -> Dia con trong: ${avail_gb}GB | datadir/ hien chiem: $used_datadir"
    if [ "$avail_gb" -lt 2 ]; then
        echo "  !!! CANH BAO: dia con duoi 2GB - DUNG LAI NGAY, khong chay lenh tiep theo !!!"
        exit 1
    fi
}

# Chi chay 1 combo dau tien lam thu - XEM KET QUA TRUOC KHI CHAY TIEP
run_one Extended_test_LT
echo ""
echo ">>> Da xong 1/8 combo. Kiem tra dong tren, neu on hay tu chay tiep 7 combo con lai."
