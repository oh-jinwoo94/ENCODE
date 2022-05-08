#!/bin/sh

for file in  ../crispr_csv_files/*.csv
do
python ../script/convert_csv_using_coord.py  $file ../hg19_to_hg38/$(basename $file .csv).bowt.hg19_to_hg38 > ../crispr_csv_converted_to_hg38/$(basename $file .csv)_PerturbTarget_in_hg38.csv
done
