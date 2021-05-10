# ENCODE

========== scripts ==============
-- gRNA_to_log2FC.py -- 
input: ENCODE-formatted guide_quant files
output: log2FC_summary files

sample command line (format {gRNA quant 1 (e.g. T0)} {gRNA quant 2 (e.g. T14)} {ofile prefix})
python gRNA_to_log2FC.py  ../screens/MYC_rep1_LS_ENCODE_guideQuant.bed  ../screens/MYC_rep1_HS_ENCODE_guideQuant.bed  Sabeti_HCRFlowFISH_MYC_R1


-- summary_to_bedgraph.py --
input: log2FC_summary file
output: .bedgraph

sample command line (format {log2FC summary} {col index for log2fc} {ofile name})
# for raw log2fc
python summary_to_bedgraph.py  Sabeti_HCRFlowFISH_MYC_R1.log2FC_summary 2 Sabeti_HCRFlowFISH_MYC_R1_log2FC_0.bedgraph
# for ztransformed_by_neg_control
python summary_to_bedgraph.py  Sabeti_HCRFlowFISH_MYC_R1.log2FC_summary 3 Sabeti_HCRFlowFISH_MYC_R1_log2FC_1.bedgraph
# for ztransformed_by_all
python summary_to_bedgraph.py  Sabeti_HCRFlowFISH_MYC_R1.log2FC_summary 4 Sabeti_HCRFlowFISH_MYC_R1_log2FC_2.bedgraph



============Note for file formats ===============

-- log2_FCsummary files --
contains gRNA coordinate, PAM coordinate, and log2FC values. 
negative controls are excluded.

