#!/bin/bash
# Doi ten 130 do thi tong hop de processing.py nhan dung nhanh 'train'.
#
# LY DO: processing.py tach ten bang split('_'), doi hoi dung 3 phan
# <graph>_<train|test>_<prob>. Ten cu "synth_small_ba_000_LT" co QUA
# NHIEU dau _ , bi tach thanh ['synth','small','ba','000','LT'] - vi
# tri [1]='small' KHONG khop 'train'/'test', code se bao loi ngay.
#
# SUA: doi dau _ giua cac phan mo ta (small/ba/000) thanh dau -, giu
# dung 3 phan cach boi _: <ten-mo-ta>_train_<prob>
#   VD: synth_small_ba_000_LT  ->  synth-small-ba-000_train_LT
#
# Doi CA graphs/*.txt LAN raw_data/*/ (thu muc da sinh Monte Carlo
# roi, KHONG can chay lai - chi doi ten, tiet kiem ~2.5 tieng da lam).

cd ~/Documents/HISP/HISP

count=0
for f in graphs/synth_*_LT.txt; do
    old_base=$(basename "$f" _LT.txt)          # vd: synth_small_ba_000
    new_base=$(echo "$old_base" | sed 's/_/-/g')  # vd: synth-small-ba-000

    old_graph_file="graphs/${old_base}_LT.txt"
    new_graph_file="graphs/${new_base}_train_LT.txt"
    old_raw_dir="raw_data/${old_base}_LT"
    new_raw_dir="raw_data/${new_base}_train_LT"

    if [ -f "$old_graph_file" ]; then
        mv "$old_graph_file" "$new_graph_file"
    fi
    if [ -d "$old_raw_dir" ]; then
        mv "$old_raw_dir" "$new_raw_dir"
    else
        echo "  !!! CANH BAO: khong thay $old_raw_dir - kiem tra lai !!!"
    fi
    count=$((count + 1))
done

echo "Da doi ten $count do thi."
echo "Kiem tra mau:"
ls graphs/synth-*_train_LT.txt | head -3
ls raw_data/ | grep "^synth-" | head -3