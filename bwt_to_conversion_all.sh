#!/bin/sh

for file in ../crispr_csv_files/*.csv
do

python ../script/bwt_to_conversion.py  $file $(basename $file .csv)_perturb_site.fa_bwt_n0_best > ../hg19_to_hg38/$(basename $file .csv).bowt.hg19_to_hg38

#check correctness
python ../script/check_conversion_correctness.py  ../hg19_to_hg38/$(basename $file .csv).bowt.hg19_to_hg38  hg19 hg38 /mnt/t/data0/joh27/genomes/
done
