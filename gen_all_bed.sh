#!/bin/sh

for file in ../crispr_csv_files/*.csv
do
    python ../script/extract_bed_from_csv.py $file > $(basename $file .csv)_perturb_site".bed"
done
