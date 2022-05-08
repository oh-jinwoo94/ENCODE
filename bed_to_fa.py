# JW OH - crispr jamboree (6/10/2020)

# converts a bed file to a fasta file by fetching from genome


import sys

def main(argv = sys.argv):

    if(len(argv) != 4):
        print("Usage: {0} {genome build dir (containing single fastas)} {.bed} {ofile .fa}")
        sys.exit()
    gdir = argv[1]
    ifile = open(argv[2], 'r')
    ofile = open(argv[3], 'w')

    chr_to_seq = dict()
    for i, line in enumerate(ifile):
        if(len(line.rstrip())==0):
            continue
        if(i%1000==0):
            print(str(i) + " complete")
        words = line.split()
        chrom, begin, end = words[0], int(words[1]), int(words[2])
        qid = chrom + ":" + str(begin) + "-" + str(end)

        # read chromosome
        try:
            chrom_seq = chr_to_seq[chrom]
        except KeyError:
            with open(gdir + "/" + chrom + ".fa" , 'r') as fafile:
                fafile.readline()
                seq = "".join([line.rstrip() for line in fafile])
                chr_to_seq[chrom] = seq
                chrom_seq = chr_to_seq[chrom]
        ofile.write(">" + qid + "\n") 
        ofile.write(chrom_seq[begin:end+1] + "\n")


    ifile.close()
    ofile.close()
        



main()
