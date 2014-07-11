import codecs

datafile = 'wiki-class-subclass.dat'
superfile = 'class-taggedword-typeddependency.dat'
subfile = 'subclass-taggedword-typeddependency.dat'
typed = ["root", "prep","nn", "dep", "amod", "conj", "det", "abbrev", "poss", "appos", 
"nsubj", "pobj", "dobj", "num","npadvmod", "aux", "advmod", "rcmod", "cop", "xcomp", 
"partmod","prt", "prepc"]

relations = ['equal','contain','contained','no relation','other']

centerWordD = {}

def appendToDict(ddict,key,value):
    if not ddict.has_key(key):
        ddict[key]= []
        ddict[key].append(value)
    elif value in ddict[key]:
        return
    elif value.lower() in [i.lower() for i in ddict[key]]:
        l = [i.lower() for i in ddict[key]]
        j = l.index(value.lower())
        if value < ddict[key][j]:
            ddict[key][j] = value
    else:
        ddict[key].append(value)
        
def readFromDataFile(ddict,filename,reverse = False): # if reverse=True,the second column becomes keys and the first column becomes values
    f = codecs.open(filename,'r','utf-8')
    count_list = []
    for line in f.readlines():
        count_list.append(line)
        eachLine = line.strip('\n').split('\t\t')#strip('\n') to remove line feed
        if reverse:
           # appendToDict(ddict,eachLine[1],eachLine[0])
           ddict[eachLine[1]].append(eachLine[0])
        else:
           # appendToDict(ddict,eachLine[0],eachLine[1])
           ddict[eachLine[0]].append(eachLine[1])
            
    print filename
    print len(ddict)
    print len(count_list)

    f.close()
    return ddict

def writeToNewFile(newFile,llist): # one to many
    fwrite = codecs.open(newFile,'w','utf-8')
    for item in llist:        
        fwrite.write('%s\n'%(item))
    fwrite.close()

def readTripleFromFile(filename):
    f = codecs.open(filename,'r','utf-8')
    llist = []
    count_list = []
    for line in f.readlines():
        count_list.append(line)
        eachLine = line.strip('\n').split('\t\t')#strip('\n') to remove line feed
        llist.append(eachLine)
            
    print filename
    print len(llist)
    print len(count_list)

    f.close()
    return llist

def writeTripleToFile(newFile,llist):
    fwrite = codecs.open(newFile,'w','utf-8')
    for item in llist:        
        fwrite.write('%s\t\t%s\t\t%s\n'%(item[0],item[1],item[2]))
    fwrite.close()

def separateTypedDependency(llist):
    newlist = []

    for item in llist:
        newitem = []
        newitem.append(item[0])
        types = item[2][1:-1].split('), ')
        ts = {}
        for t in types:
            if len(t) == 0:
                continue
            aa = t.split('(')
            ts[aa[0]]=[s[:s.rfind('-')] for s in aa[1].split(', ') ]
        newitem.append(ts)
        newlist.append(newitem)
    
    return newlist
    
def separateTaggedWordToDict(item): #be attantion to the lowercase
    ddict = {}
    lTaggedWords = item[1][1:-1].split(', ')
    for tag in lTaggedWords:
        word2tag = tag.split('/')
        key = word2tag[0].lower()
        ddict[key] = word2tag[1]
    return ddict

def getCenterWordType(cwdict,llist):
    dd = {}
    count = 0
    for item in llist:
        taggedDict = separateTaggedWordToDict(item)
        print count
        count = count+1
        centerW = cwdict[item[0]].split('\0')
        for i in centerW:
            dd[item[0]] = taggedDict[i.lower()]+'\0'
        dd[item[0]] = dd[item[0]][:-1]
    return dd

def findCenterword(item):
    typed = item[1]
    centerword = ""

    if not typed.has_key("root"):
        return "\t"
    if typed.has_key("prep_in"):
        centerword = typed["prep_in"][0]
    elif typed.has_key("prep_of"):
        centerword = typed["prep_of"][0]
    elif typed.has_key("prep_from"):
        centerword = typed["prep_from"][0]
    elif typed.has_key("amod"):
        if typed["root"][1] == typed["amod"][0]:
            centerword = typed["root"][1]
        elif (typed.has_key("dep") and typed["amod"][0] == typed["dep"][1]) or (typed.has_key("nn") and typed["amod"][0] == typed["nn"][0]):
                centerword = typed["amod"][0]
        else:
            centerword = typed["root"][1]
    else:
        centerword = typed["root"][1]

    if typed.has_key("conj_and"):
        if typed["conj_and"][0] == centerword:
            centerword = centerword+"\0"+ typed["conj_and"][1]
        elif typed["conj_and"][1] == centerword:
            centerword = centerword+"\0"+ typed["conj_and"][0]
    return centerword

def generateCenterWords(triplelist):

  
    ltyped = separateTypedDependency(triplelist)
    #ltagged = separateTaggedWord(l)

    #for item in ltyped[:10]:
    #    print "%s\t\t%s\n"%(item[0],item[1])

    for item in ltyped:
        cw = findCenterword(item)
        if cw == '\t':
            continue
        centerWordD[item[0]] = cw
 
    return centerWordD

def getRelationshipOfTwoLists(l1,l2):
    oldLen1 = len(set(l1))
    oldLen2 = len(set(l2))
    mergeLen = len(set(l1.extend(l2)))
    if oldLen == mergeLen and oldLen2 == mergeLen:
        return relationship[0]
    elif oldLen == mergeLen:
        return relationship[1]
    elif oldLen2 == mergeLen:
        return relationship[2]
    elif oldLen1+oldLen2 == mergeLen:
        return relationship[3]
    else:
        return relationship[4]

l = readTripleFromFile(superfile)
superCenterWordsD = generateCenterWords(l)
superCWTypeD = getCenterWordType(superCenterWordsD,l)

print superCWTypeD[:100] 

#subCenterWords = generateCenterWords(subfile,"subclass-centerword.dat")
