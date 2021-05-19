'''
Jin Woo Oh  -- for crispr group 
Get PAM sequences using column (0,1,2,5)

input file format
chrX    48746031        48746034        NA|chrX:48746031-48746034:+     103     +       chrX:48746012-48746031:+        NA      NA      NA      NA       NA      NA      CCTTGGTCTCCCGAAGATC     GCCTTGGTCTCCCGAAGATC    targeting       NA
'''

import sys


# reverse complement a sequence
rv = {'A': 'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
def revcomp(seq):
    rvcmp_seq = [rv[seq[i]] for i in range(len(seq) - 1, -1, -1)]
    return "".join(rvcmp_seq)

def main(argv = sys.argv):
    if(len(argv) != 3):
        print("Usage {0} {ifile} {ref_genome.fasta}")
        sys.exit()

    print(argv[1])
    ifile = open(argv[1], 'r')

    chrom_to_seq = dict()
    ngg = 0; other = 0;
    for line in ifile:

        # if empty line, skip
        if(len(line.rstrip()) == 0):
            continue

        words = line.split()
        ###### read whole chromosome sequences  #######
        try: # for properly formatted genomic coordinates. allows float as well 
            chrom, begin, end, strand = words[0], int(eval(words[1])), int(eval(words[2])), words[5]
        except (SyntaxError, NameError) as error:
            continue # nontargetting controls  e.g. NA or . 
        # also just skip negative controls
        if(words[-2] == "negative_control"):
            continue
        try: # if chromosome already loaded, use it
            cseq = chrom_to_seq[chrom]
        except KeyError: # else, load chromosome
            with open(argv[2], 'r') as ref_file:
                while(ref_file.readline().split()[0] != (">" + chrom)):
                    pass
                cseq = []
                for line in ref_file:
                    if(">" not in line):
                        cseq.append(line.rstrip())
                    else:
                        break
                cseq = "".join(cseq)
                chrom_to_seq[chrom] = cseq


        ######  fetch PAM sequence using PAM coordinates   ######
        if(strand == "+"):
            pam = cseq[begin:end].upper()
        else: # neg strand --> rev comp
            pam = revcomp(cseq[begin:end].upper())

        ### histogram of pams ###
        if(pam[1:] == "GG"):
            ngg += 1.0
        else: 
            other += 1.0




    print("\t".join(["NGG", str(ngg)]))
    print("\t".join(["other", str(other)]))

    if(ngg / (ngg+other) > 0.8):
        print("More than 80% of the PAMs are NGG. The coordinates are likely to be correct")
    else:
        print("Less than 80% of the PAMs are NGG. The coordinates are likely to be incorrect")
    ifile.close()
main()
