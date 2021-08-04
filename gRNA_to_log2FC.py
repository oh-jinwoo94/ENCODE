'''
input file format:
chr10   107843639       107843642       NA|chr10:107843620-107843639:+  355     +       chr10:107843620-107843639:+     chr8    127736231       127736232       +       MYC     ENSG00000136997 GGAATGATCACAGTCTAAAC    GGAATGATCACAGTCTAAAC    negative_control        ST

output file format
name    PAM_ID  raw_log2FC      ztransformed_by_neg_control     ztransformed_by_all_guides
GATA1|chr12:54300748-54300767:+ chr12:54300767-54300770:+       -0.6898171127857369     -1.3909202490331116     -1.1558450982161879
GATA1|chr12:54300792-54300811:+ chr12:54300811-54300814:+       0.14274017211608214     -0.3609625301812802     -0.3592771390999452

'''
import sys
import numpy as np
def extract_PAM_ID(line):
    words = line.split()
    pam_id = words[0] + ":" + words[1] + "-" + words[2] + ":" + words[5]
    return pam_id
def main(argv = sys.argv):
    if(len(argv) != 4):
        print("Usage: {0} {gRNA quant 1 (e.g. T0)} {gRNa quant 2 (e.g. T14)} {ofile prefix}")
        sys.exit()
    ifile1 = open(argv[1], 'r')
    ifile2 = open(argv[2], 'r')

    prefix = argv[3]

    # Generate N x 3 matrix, N = #gRNA. : [[perturbation ID, type, count]]
    # [['MYC|chr12:54300748-54300767:+', chr12:54300767-54300770:+, 'targeting' 517] ..]
    pID_to_cnt_1 = np.array([[line.split()[3], extract_PAM_ID(line), line.split()[-2], int(line.split()[4])] for line in ifile1], dtype=object)
    pID_to_cnt_2 = np.array([[line.split()[3], extract_PAM_ID(line),  line.split()[-2], int(line.split()[4])] for line in ifile2], dtype=object)

    print(type(pID_to_cnt_1[:,0]))
    print(type(pID_to_cnt_2[:,0]))
    #if((pID_to_cnt_1[:,0] != pID_to_cnt_2[:,0]).all()):
    if(not np.array_equal(pID_to_cnt_1[:,0], pID_to_cnt_2[:,0])):
        print("gRNA order in file1 and and file2 don't match")
        sys.exit()

    
    # compute log2 (pre-normalization)
    print(pID_to_cnt_1[:,3])
    print(pID_to_cnt_2[:,3])
    log2FC = np.log2(((pID_to_cnt_1[:,3] + 1.0) / (pID_to_cnt_2[:,3] + 1.0)).astype('float64'))
    print(log2FC)

    # normalize using negative control. 
    neg_ctrl = (pID_to_cnt_1[:,2] == "negative_control")
    log2FC_neg = log2FC[neg_ctrl]
    mu, sig = log2FC_neg.mean(), log2FC_neg.std()
    log2FC_neg_norm = (log2FC - mu)/sig
    print(log2FC_neg_norm)

    # normalize using all
    mu, sig = log2FC.mean(), log2FC.std() 
    log2FC_all_norm = (log2FC - mu)/sig
    print(log2FC_all_norm) 

    # instead of z-transform, normalize by mean count 
    log2FC_mean_normed = np.log2(((pID_to_cnt_1[:,3]/(np.mean(pID_to_cnt_1[:,3])) + 1.0) / \
                                  (pID_to_cnt_2[:,3]/(np.mean(pID_to_cnt_2[:,3])) + 1.0)).astype('float64'))
    print(log2FC_mean_normed)

    # tot normed (suggested by josh)
    log2FC_tot_normed = np.log2((((pID_to_cnt_1[:,3]+1)/(np.sum(pID_to_cnt_1[:,3]))) / \
                                  ((pID_to_cnt_2[:,3]+1)/(np.sum(pID_to_cnt_2[:,3])))+1).astype('float64'))

    with open(prefix + ".log2FC_summary", 'w') as ofile:
        ofile.write("\t".join(["name", "PAM_ID","raw_log2FC", "ztransformed_by_neg_control", "ztransformed_by_all_guides", "normalized_by_mean_count", "normalized_by_tot_count"]) + '\n')
        for i in range(0, len(log2FC)):
            if("NA|.:.-." in pID_to_cnt_1[i,0]):
                    continue
            else:
                ofile.write("\t".join([pID_to_cnt_1[i,0], pID_to_cnt_1[i,1] \
                               ,str(log2FC[i]), str(log2FC_neg_norm[i]), str(log2FC_all_norm[i]), str(log2FC_mean_normed[i]), str(log2FC_tot_normed[i])]) + '\n')
            
            
    ifile1.close()
    ifile2.close()
    
    


main()
