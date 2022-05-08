#!/bin/sh

for file in *.fa; 
do
echo $file	
/mnt/t/data0/joh27/tools/bowtie/bowtie /mnt/data0/mbeer/work/bowtie/bowtie_genomes/hg38  -f $file -n 0 --best >$file"_"bwt_n0_best
done
