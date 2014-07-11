#encoding=utf-8

INPUT_FILE="/home/keg/lmy/data/hudong-article-category-11features-new.dat"
OUTPUT_FILE="/home/keg/lmy/data/hudong-article-category-11features-withoutpunc.dat"

with open(INPUT_FILE,'r') as fin:
    fout = open(OUTPUT_FILE,'w')
    out_lines = []
    remove_count = 0
    while True:
        line = fin.readline()
        if not line:
            break
        if '《' in line or '》' in line or '(' in line or ')' in line or '：' in line or ':' in line or '（' in line or '）' in line:
            remove_count+=1
            continue
        fout.write(line)
    print remove_count,"lines removed."
    fout.close()

