'''
Purpose:
Input file has three columns for different types of log2fc. Choose one column and make bedgraph.


input file format:
name    PAM_ID  raw_log2FC      ztransformed_by_neg_control     ztransformed_by_all_guides
NA|chr10:107843620-107843639:+  chr10:107843639-107843642:+     0.2565649105042363      0.4333194638821953      0.4468597233627974
NA|chr10:107843650-107843669:+  chr10:107843669-107843672:+     -0.6303544035351705     -0.8859942777166191     -0.8147069889203993
NA|chr10:123598185-123598204:+  chr10:123598204-123598207:+     0.20059383105788678     0.3500611414206248      0.3672456597582073


output file format:
chr8    128391200       128391200       1.254248711277702
chr8    126891867       126891867       0.9836344730213816


For output pam coord, use first base pair (if - strand, last coord)
If there are mutliple pam with the same first bp (e.g. coming from pos and neg), average log2FC.
'''
import sys
import numpy as np

def main(argv = sys.argv):
    if(len(argv) != 4):
        print("Usage: {0} {log2FC summary} {col index for log2fc} {ofile name}")
        sys.exit()

    ifile = open(argv[1], 'r')
    cindex = int(argv[2])
    ofile = open(argv[3], 'w')

    log2FC_name = ifile.readline().split()[cindex]
    ploc_to_log2FC = dict()
    for line in ifile:
        words = line.split()
        pID, log2FC = words[1], eval(words[cindex])
        chrom, brange, strand = pID.split(":")
        start, end = brange.split("-")

        if(start == "."): # ignore non-coordinates 
            continue 
        if(strand == "+"):
            pcoord = start
        elif(strand == "-"):
            pcoord = str(int(end) - 1)
        else:
            continue
 
        ploc = chrom + "_" + pcoord
        try:
            ploc_to_log2FC[ploc].append(log2FC)
        except KeyError:
            ploc_to_log2FC[ploc] = [log2FC]


    for ploc in list(ploc_to_log2FC):
        log2FC = np.mean(ploc_to_log2FC[ploc])
        chrom, pcoord = ploc.split("_")
        ofile.write("\t".join([chrom, pcoord, pcoord, str(log2FC)]) + '\n')
    ifile.close()


main()
