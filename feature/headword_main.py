from SingleSent import *
import codecs

#datafile = '/home/zigo/SemantifyWiki/etc/dataset/sample-4-title.dat'
datafile = '/home/keg/lmy/CLKB/sample-4-title.dat'
#superfile = '/home/lmy/data/parser/new-wa-title-taggedword-typeddependency.dat'
superfile = '/home/keg/lmy/data/parser/new-wa-title-taggedword-typeddependency.dat'
#subfile = '/home/lmy/data/parser/new-wc-title-taggedword-typeddependency.dat'
subfile = '/home/keg/lmy/data/parser/new-wc-title-taggedword-typeddependency.dat'
featurefile = '/home/keg/lmy/data/CLKB/sample-4-9features.dat'
specialfile= 'special-taggedword-typeddependency.dat'
typed = ["root", "prep","nn", "dep", "amod", "conj", "det", "abbrev", "poss", "appos", 
"nsubj", "pobj", "dobj", "num","npadvmod", "aux", "advmod", "rcmod", "cop", "xcomp", 
"partmod","prt", "prepc"]

relations = ['equal','contain','contained','no relation','other']
numberType = ['singular','plural','unknown']

def readDataFromFile(filename):
    f = codecs.open(filename,'r','utf-8')
    llist = []
    for line in f.readlines():
        eachLine = line.strip('\n').split('\t')#strip('\n') to remove line feed
        llist.append(eachLine)
            
    print filename
    print len(llist)

    f.close()
    return llist

def getRelationshipOfTwoSets(l1,l2):
    oldLen1 = len(set(l1))
    oldLen2 = len(set(l2))
    mergeList = l1
    mergeList.extend(l2)
    mergeLen = len(set(mergeList))
    if oldLen1 == mergeLen and oldLen2 == mergeLen:
#        return relations[0]
        return 0
    elif oldLen1 == mergeLen:
        #return relations[1]
        return 1
    elif oldLen2 == mergeLen:
        #return relations[2]
        return 2
    elif oldLen1+oldLen2 == mergeLen:
        #return relations[3]
        return 3
    else:
        #return relations[4]
        return 4
    
def getRalationshipOfTwoSets2(l1,l2):
    if len(l1) == 0 or len(l2) == 0:
        #return relations[3]
        return 0
    oldLen1 = len(set(l1))
    oldLen2 = len(set(l2))
    mergeList = l1
    mergeList.extend(l2)
    mergeLen = len(set(mergeList))
    if oldLen1+oldLen2 == mergeLen:
        #return relations[3]
        return 0
    else:
        #return relations[4]
        return 1
    
def writeToFile(newFile,llist):
    fwrite = codecs.open(newFile,'w','utf-8')
    for item in llist:
        superS = superD[item[0]]
        subS = subD[item[1]]
        relation = getRelationshipOfTwoSets(superS.headword.split('\0'),subS.headword.split('\0'))
        fwrite.write('%s\t\t%s\t\t%s\t%s\t%s\t%d\t%d\t%d\t%d\n'%(
            item[0],item[1],relation,superS.hwNumber,subS.hwNumber,superS.hwLen,subS.hwLen,superS.wordLen,subS.wordLen))
    fwrite.close()

def recordHeadword(filename,d):
    with codecs.open(filename,'w','utf-8') as f:
        for k,v in d.items():
            f.write("%s\t"%k)
            for i in v:
                #print i
                try:
                    i = en.noun.singular(i) 
                except:
                    pass
                #print i
                f.write("\t%s"%i)
            f.write("\n")

#specialD = {}
#speciall = readDataFromFile(specialfile)
#for item in speciall:
#    if len(item[2]) <= 0:
#        continue
#    specialD[item[0]] = SingleSent(item)
#print 'finish specialD'
#speciall = []

superl = []
superD = {}
superl = readDataFromFile(superfile)
for item in superl:
    if len(item[2]) <= 0:
        continue
    try:
        superD[item[0]] = SingleSent(item)
    except Exception,e:
        print e
        print item
print 'finish superD'
superl = []

superHeadword = dict((k,v.headword) for k,v in superD.iteritems())
recordHeadword('super_headword.dat',superHeadword)

subD = {}
subl = readDataFromFile(subfile)
for item in subl:
    if len(item[2]) <= 0:
        continue
    subD[item[0]] = SingleSent(item)
print 'finish subD'
subl = []

subHeadword = dict((k,v.headword) for k,v in subD.iteritems())
recordHeadword('sub_headword.dat',subHeadword)

#classl = readDataFromFile(datafile)
#writeToFile("class-subclass-features.dat",classl)

#fread = codecs.open(datafile,'r','utf-8')
#fwrite = codecs.open('class-subclass-features.dat','w','UTF--8')
#for line in fread.readlines():
#    item = line.strip('\n').split('\t\t')#strip('\n') to remove line feed
#    superS = superD[item[0]]
#    subS = subD[item[1]]
#    relation = getRelationshipOfTwoSets(superS.headword,subS.headword)
#    relation8 = getRalationshipOfTwoSets2(superS.headword,subS.unHeadword)
#    relation9 = getRalationshipOfTwoSets2(subS.headword,superS.unHeadword)
#    fwrite.write('%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%d\t\t%d\t\t%d\t\t%d\t\t%s\t\t%s\n'%(
#        item[0],item[1],relation,superS.hwNumber,subS.hwNumber,superS.hwLen,
#        subS.hwLen,superS.wordLen,subS.wordLen,relation8,relation9))
#fread.close()
#fwrite.close()

fread = codecs.open(datafile,'r','utf-8')
fwrite = codecs.open(featurefile,'w','UTF--8')
for line in fread.readlines():
    item = line.strip('\n').split('\t\t')#strip('\n') to remove line feed
    try:
        superS = superD[item[0]]
        subS = subD[item[1]]
    except Exception,e:
        print e
        print line
    relation = getRelationshipOfTwoSets(superS.headword,subS.headword)
    relation8 = getRalationshipOfTwoSets2(superS.headword,subS.unHeadword)
    relation9 = getRalationshipOfTwoSets2(subS.headword,superS.unHeadword)
    fwrite.write('%s\t%s\t\t%d,%d,%d,%d,%d,%d,%d,%d,%d\n'%(
        item[0],item[1],relation,superS.hwNumber,subS.hwNumber,superS.hwLen,
        subS.hwLen,superS.wordLen,subS.wordLen,relation8,relation9))
fread.close()

#fread = codecs.open(datafile,'r','utf-8')
#funknown = codecs.open('unknown.dat','w','UTF-8')
#unknownL = []
#for line in fread.readlines():
#    item = line.strip('\n').split('\t\t')#strip('\n') to remove line feed
#    superS = superD[item[0]]
#    subS = subD[item[1]]
#    #print superS.hwNumber.values()
#    if not superS.wordLen == 1 and 'unknown' in superS.hwNumber.values() and not superS.headword[0] == 'Geography': 
#        unknownL.append(superS)
#       # funknown.write('%s\t\t%s\t\t%s\t\t%s\n'%(item[0],superS.headword,superS.taggedWords,superS.typedDependency))
#    if not subS.wordLen == 1 and 'unknown' in subS.hwNumber.values() and not subS.headword[0] == 'Geography': 
#        unknownL.append(subS) 
#       # funknown.write('%s\t\t%s\t\t%s\t\t%s\n'%(item[1],subS.headword,subS.taggedWords,subS.typedDependency))
#unknownL = list(set(unknownL))
#for item in unknownL:
#        funknown.write('%s\t\t%s\t\t%s\t\t%s\n'%(item.string,item.headword,item.taggedWords,item.typedDependency))
#print len(unknownL)
#unknownL = []    
#fread.close()
#funknown.close()
#for item in specialD.values():
#    print '%s\t\t%s\t\t%s\t\t%s\n'%(item.string,item.headword,item.taggedWords,item.typedDependency)
print 'end'
