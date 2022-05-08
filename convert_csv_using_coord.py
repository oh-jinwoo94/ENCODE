# JW OH - crispr jamboree (6/10/2020)

# use genome build coordinate conversion file to convert hg19 .csv to hg38 .csv
# only the first three columns are converted.


# only the hg19 coordinates that get successfully converted will be represented in the output file



# file format for conversion file 
# hg19_guideStart hg19_guideEnd   hg19_guideStrand        hg19_name       hg38_chr        hg38_guideStart hg38_guideEnd   hg38_guideStrand        hg38_nameguideSequence
#chr8    129113248       129113268       -       chr8:129113248-129113268:-      chr8    128101002       128101022       -       chr8:128101002-128101022:-       GATAAGGTCCAGGTGGAGTCA
#chrX    48654347        48654367        +       chrX:48654347-48654367:+        chrX    48795940        48795960        +       chrX:48795940-48795960:+GCCCAGCCCTCACACCCTGC

# if not mappeed
# hg38_chr .. will be "."

# cv file format
# assumes that there is a header name called "strandElement"

# chrX,48654347.0,48654367.0,chrX,48644962,48644962,chrX:48654347.0-48654367.0:+,.,+,+,K562,GATA1,ENSG00000102145.9,hg19,GCCCAGCCCTCACACCCTGC,SingleGuideCutting_4802,62,11.0,44.0,27.0,16.0,3.0,0.0,9.0,0.0,24.0,0.0,42.0,0.0,8.0,23.0,17.0,50.0,36.0,0.0,3.0,8.0,20.0,43.0,26.0,3.0,55.0,21.0,49.0,166.0,31.0,29.0,5.0,31.0,89.0,106.0,68.0,72.0,33.0,101.0,20.0,31.0,21.0,38.0,4.0,29.0,11.0,29.0,29.0,41.0

import sys



def main(argv = sys.argv):

    if(len(argv) != 3):
        print("Usage {0} {.csv in hg19} {hg19->hg38 conversion file}")
        sys.exit()

    icsv_file = open(argv[1], 'r')
    conv_file = open(argv[2], 'r')

    # first read in conv_file
    ori_to_new = dict() # old coordinate id to new coordinate info
    conv_file.readline() # header
    for line in conv_file:
        words = line.split()
        qid = words[4] 
        tchr, tbegin, tend, tstrand = words[5], words[6], words[7], words[8]
        ori_to_new[qid] = [tchr, tbegin, tend, tstrand]

    header = icsv_file.readline()
    print(header.rstrip())
    strand_index = (header.split(",")).index("strandElement")

    for line in icsv_file:
        words = (line.rstrip()).split(',')
        qchr, qbegin, qend, qstrand  = words[0], words[1], words[2], words[strand_index]
        if(qbegin != "." and len(qbegin) != 0):
            qbegin, qend = str(int(eval(qbegin))), str(int(eval(qend))) # in case given in float
            qid = qchr + ":" + qbegin + "-" + qend + ":" + qstrand
            try:
                new_coord = ori_to_new[qid]
                words[0], words[1], words[2], words[strand_index] = new_coord
                print(",".join(words))
            except:
                pass

    icsv_file.close()
    conv_file.close()
        
main()

