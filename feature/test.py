
TEST_FILE="hudong-category2-taggedword-typeddependency.dat"

with open(TEST_FILE,'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
    
        item = line.strip('\n').split('\t')
        tagged = item[1]
        typed = item[2]
        print tagged
        print typed
        tagList = eval(tagged)
        typedList = eval(typed)
        print len(tagList)
        print len(typedList)
        
