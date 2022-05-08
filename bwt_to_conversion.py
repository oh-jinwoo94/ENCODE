# Jin Woo OH - crispr jamboree (6/10/2020)
# takes the initial crispr screen .csv file and bowtie output (mapping the perturb region) and output a file that gives the hg19 -> hg38 conversion result


# File format requirement for .csv file
# assumes that the first three columns are the ones used for coordinate change.
# assumes that there is a column named "strandElement" that is either + or -
# assumes that there is a column named "guideSequence"
# skips .csv lines that are non-targetting. (empty first three columns and/or empty strandElement)


# bowtie output format
# chrX:48554983-48555003  +       chrX    48696592        GCGCGGCGAGCACCCGCCTCC   IIIIIIIIIIIIIIIIIIIII   0
# chrX:49741561-49741581  +       chrX    49976950        GTACAGAAATGTTTCTTAAGC   IIIIIIIIIIIIIIIIIIIII   0


# output format
# 1 hg19 chr
# 2 hg19 guideStart
# 3 hg19 guideEnd
# 4 hg19 guideStrand
# 5 hg19 name (chr:start-end:strand)
# 6 hg38 chr
# 7 hg38 guideStart
# 8 hg38 guideEnd
# 9 hg38 guideStrand
# 10 hg38 name (chr:start-end:strand)
# 11 guideSequence

# NOTE
# hg19 name and hg38 name are regenerated using the coordinates
# guideSequence is given by the initial guidSequence in .csv.  

import sys



def main(argv = sys.argv):
    if(len(argv) != 3):
        print("{0} {initial csv file} {bowtie output}")
        sys.exit()

    csv_file = open(argv[1], 'r')
    bto_file = open(argv[2], 'r')

    qname_to_mapping = dict()
    for line in bto_file:  
        words = line.split()
        qname, tstrand, tchr, tbegin, tseq = words[0], words[1], words[2], int(words[3]), words[4]
        tend = tbegin + len(tseq)- 1
        qname_to_mapping[qname] = [tchr, str(tbegin), str(tend), tstrand]

    csv_header = ((csv_file.readline()).rstrip()).split(',')
    strand_index = csv_header.index("strandElement")
    #gseq_index = csv_header.index("guideSequence")
    gseq_index = csv_header.index("guideSpacerSeq") 
    #print("\t".join(  ["hg19_guideStart", "hg19_guideEnd", "hg19_guideStrand", "hg19_name", "hg38_chr", "hg38_guideStart", "hg38_guideEnd", "hg38_guideStrand", "hg38_name", "guideSequence"]  ))
    print("\t".join(  ["hg19_guideStart", "hg19_guideEnd", "hg19_guideStrand", "hg19_name", "hg38_chr", "hg38_guideStart", "hg38_guideEnd", "hg38_guideStrand", "hg38_name", "guideSpacerSeq"]  ))
    for line in csv_file:
        words = line.split(',')
        qchr, qbegin, qend = words[0:3]
        qstrand = words[strand_index]
        gseq = words[gseq_index]

        if((qchr != "." and qchr !="") and (qstrand == "+" or qstrand == "-")): # skip over the negative controls
            qname = qchr + ":" + qbegin + "-" + qend

            try:
               mapped = qname_to_mapping[qname]
            except KeyError: # not mapped by bowtie
                mapped = [".", ".", ".", "."]
          
            if(not(mapped[3] == "+" or mapped[3] == "-" or mapped[3] == ".")): #"." for not mapped
                print("strand must be either + or - or .")
                print(qstrand)
                print(tstrand)
                print(line)
                sys.exit()

            if(mapped[3] == "+"):
                if(qstrand == "+"):
                    tstrand = "+"
                else:
                    tstrand = "-"
            elif(mapped[3] == "-"):
                if(qstrand == "+"):
                    tstrand = "-"
                else:
                    tstrand = "+"
            else:
                tstrand = "."

            tname = mapped[0] + ":" + mapped[1] + "-" + mapped[2] + ":" + tstrand
 
            print("\t".join([qchr, qbegin, qend, qstrand, qname + ":" + qstrand, mapped[0], mapped[1], mapped[2], tstrand, tname, gseq]))
                


main()
