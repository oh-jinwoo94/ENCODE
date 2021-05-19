# ENCODE FCC CRISPR subgroup

# scripts
## For checking file correctness
### check_guide_quant_format.py
input: guide_quant_format.txt (guideline for ENCODE standard) and ENCODE-formatted guide_quant files

NOTE: "guide_quant_format.txt" in this repository might not be up-to-date (last modified: 5/10/2021).

Purpose: Check whether input file has a proper format that matches with guide_quant_format guideline. 

sample command line:  python {format description file} {test file}

python check_guide_quant_format.py guide_quant_format.txt GATA_rep1_HS_ENCODE_guideQuant.bed
 
#### sample output

If successful: 

Test 1 passed

Test 2 passed

Test 3 passed

#### Example failure:

Test 1 passed

Test 2 failed. In line 4695, 15'th element must be either targeting or negative_control


### check_PAM.py
input:ENCODE-formatted guide_quant files, a reference genome fasta file. 
ref hg38 can be downloaded from: https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/

Purpose: If your file passes check_guide_quant_fomat.py, use this script to check whether your PAM coordinates are correctly extracted by checking NGG sequence. 

sample command line:  python {ifile: guide_quant} {reference fasta}

python check_PAM.py  MYC_rep1_LS_ENCODE_guideQuant.bed  /mnt/data0/joh27/genomes/hg38

#### Sample result 1 : 

NGG     50732.0

other   398.0

More than 80% of the PAMs are NGG. The coordinates are likely to be correct

#### Sample result 2: 

NGG     5433.0

other   4689.0

Less than 80% of the PAMs are NGG. The coordinates are likely to be incorrect



## For analysis (PAM coordinate -> log2FC) -- after passing the above two tests.
### gRNA_to_log2FC.py  

input: ENCODE-formatted guide_quant files

Purpose: compute log2FC in three different way: raw log2FC, log2FC z-transformed using negative control guides, log2FC z-tranformed using all guides

output: log2FC_summary files

sample command line (python  {gRNA quant 1 (e.g. T0)} {gRNA quant 2 (e.g. T14)} {ofile prefix})

python gRNA_to_log2FC.py  MYC_rep1_LS_ENCODE_guideQuant.bed  screens/MYC_rep1_HS_ENCODE_guideQuant.bed  Sabeti_HCRFlowFISH_MYC_R1


### summary_to_bedgraph.py 

input: log2FC_summary file

Purpose: select a type of log2FC in log2FC_summary, and use it to generate .bedgraph. Further, to ensure that the genome coordinates do not overlap (for compatibility with UCSC genome browser), output PAM coordinates will have width of 1 (coordinate of 'N'GG for (+)-strand and of CC'N' for (-)-strand).

output: .bedgraph

sample command line (format {log2FC summary} {col index for log2fc} {ofile name})

#### for raw log2fc

python summary_to_bedgraph.py  Sabeti_HCRFlowFISH_MYC_R1.log2FC_summary 2 Sabeti_HCRFlowFISH_MYC_R1_log2FC_0.bedgraph

####  for ztransformed_by_neg_control

python summary_to_bedgraph.py  Sabeti_HCRFlowFISH_MYC_R1.log2FC_summary 3 Sabeti_HCRFlowFISH_MYC_R1_log2FC_1.bedgraph

####  for ztransformed_by_all

python summary_to_bedgraph.py  Sabeti_HCRFlowFISH_MYC_R1.log2FC_summary 4 Sabeti_HCRFlowFISH_MYC_R1_log2FC_2.bedgraph



# sample file format

## ENCODE standard guide_quantification file

For more detail, check "guide_quant_format.txt"

chr12   54300767        54300770        GATA1|chr12:54300748-54300767:+ 366     +       chr12:54300748-54300767:+       chrX    48786590        48786591        +       GATA1   ENSG00000102145 GGATTCCAGTGAGATCCGAG    GGATTCCAGTGAGATCCGAG    targeting       NA

chr12   54300811        54300814        GATA1|chr12:54300792-54300811:+ 551     +       chr12:54300792-54300811:+       chrX    48786590        48786591        +       GATA1   ENSG00000102145 CTCCACCACAGGTGCCTGAA    GCTCCACCACAGGTGCCTGAA   targeting       NA

Only the first three, fifth, and sixth columns are relevant for these scripts.

First three: PAM coordinate

Fifth: total number gRNA sequences that are sequenced in a cell population

Sixth: strand location of the PAM

## .log2FC_summary
name    PAM_ID  raw_log2FC      ztransformed_by_neg_control     ztransformed_by_all_guides

GATA1|chr12:54300748-54300767:+ chr12:54300767-54300770:+       -0.6898171127857369     -1.3909202490331116     -1.1558450982161879

GATA1|chr12:54300792-54300811:+ chr12:54300811-54300814:+       0.14274017211608214     -0.3609625301812802     -0.3592771390999452

## .bedgraph
chrX    48476136        48476136        0.16272950003810832

chrX    48476137        48476137        0.14542752477380644


