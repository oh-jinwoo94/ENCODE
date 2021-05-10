'''
Jin Woo Oh  -- for crispr group 

Using a format guide line file (example below), check whether an input file has the correct format.
Currently checks for:
    Test 1: The number of elements per line
    Test 2: Whether "guideType" is either "targeting" or "negative_control"
    Test 3: whether data types match (currently considers: uint, char[1], string, lstring)



table crispr_screen_guide_quantifications
"CRISPR guide_quantifications BED3+14 format"
(
string  chrom;          "Chromosome of the target of the perturbation (e.g., guideRNA, guideRNA pair). For guideRNA, use PAM."
...
uint    chromStart;             "Zero-based starting position of the target of the perturbation (e.g., guideRNA, guideRNA pair). As with BED format, the start position in each BEDPE feature is therefore interpreted to be 1 greater than the start position listed in the feature. For guideRNA, use PAM."
lstring Notes;          "Free text; 'NA' if no notes."
)

'''
import sys


# Test 1
def check_elem_per_line(dfile_name, ifile_name):
    n_elem = 0
    with open(dfile_name, 'r') as dfile:
        for line in dfile:
            if(';' in line):
                n_elem += 1

    with open(ifile_name, 'r') as ifile:
        for i, line in enumerate(ifile):
            if(len(line.rstrip()) != 0 and len(line.split()) != n_elem):
                print("Test 1 failed. line " + str(i+1) + " does not have " + str(n_elem) + " elements.")
                sys.exit(1)
    print("Test 1 passed")

# Test 2
def check_guide_type(dfile_name, ifile_name):
    col = 0 
    with open(dfile_name, 'r') as dfile:
        for line in dfile:
            if(';' in line):
                if("guideType" in line):
                    gt_col = col
                    break
                col += 1
    with open(ifile_name, 'r') as ifile:
        for i,line in enumerate(ifile):
            words = line.split()
            if(len(line.rstrip())>0 and words[col] != "targeting" and words[col] != "negative_control"):
                print("Test 2 failed. In line " + str(i+1) + ", " + str(col) + "'th element must be either targeting or negative_control")
                sys.exit(1)
    print("Test 2 passed")


# Test 3
def check_data_types(dfile_name, ifile_name):
    col_to_type = dict() # record data types for non-strings
    with open(dfile_name, 'r') as dfile:
        col = 0
        for line in dfile:
            if(';' in line):
                words = line.split()
                if("string" not in words[0]):
                    col_to_type[col] = words[0]
                col += 1
    #print(col_to_type)
    #{1: 'uint', 2: 'uint', 4: 'uint', 5: 'char[1]'}

    with open(ifile_name, 'r') as ifile:
        for i, line in enumerate(ifile):
            if("negative_control" in line):
                continue
            words = line.split()
            for col in list(col_to_type):
                if(col_to_type[col] == "uint"):
                    try:
                        x = int(words[col])
                        if(x<0):
                            raise error 
                    except:
                        print("Test 3 failed. In line " + str(i+1)  + ", " + words[col] + " is not unsigned integer")
                        sys.exit(1)
                if(col_to_type[col] == "char[1]"):
                    if(len(words[col]) != 1):
                        print("Test 3 failed. In line " + str(i+1)  + ", " + str(col) + "'th element must be a single-chacractor ('./-/+')")
                        sys.exit(1)
                # add more types if the file format changes. 
    print("Test 3 passed")


def main(argv = sys.argv):
    if(len(argv) != 3):
        print("{0} {format description file} {test file}")
        sys.exit()

    
    dfile_name = argv[1]; ifile_name = argv[2] 
    
    check_elem_per_line(dfile_name, ifile_name)
    check_guide_type(dfile_name, ifile_name)
    check_data_types(dfile_name, ifile_name) 
    print("All tests passed. Now use check_PAM.py to check for NGG pam sequences")

main()

