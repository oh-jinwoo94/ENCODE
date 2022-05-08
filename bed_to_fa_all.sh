#!/bin/sh
for file in *.bed
do
python3 ../script/bed_to_fa.py  /mnt/data0/joh27/genomes/hg19/ $file $(basename $file .bed)".fa"
done
