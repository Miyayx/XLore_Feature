
READ_FILE = "/home/lmy/data/origin/zhwiki-concept-sub-all.dat"
OUTPUT_FILE = READ_FILE.split(".")[0]+"-1v1.dat"

if __name__ == "__main__":
    one_to_one = [] 
    with open(READ_FILE) as f:
        for line in f.readlines():
            line = line.strip("\n")
            first = line.split("\t")[0]
            for second in line.split("\t")[1].split(";"):
                one_to_one.append([first,second])
    with open(OUTPUT_FILE,'w') as f:
        for first,second in one_to_one:
            f.write("%s\t\t%s\n"%(first,second))
