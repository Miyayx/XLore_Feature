from SingleSent import *
import codecs

DATA_DELIMITER = "\t\t"
FEATURE_ITEM_DELIMITER = "\t"

typed = ["root", "prep","nn", "dep", "amod", "conj", "det", "abbrev", "poss", "appos", 
"nsubj", "pobj", "dobj", "num","npadvmod", "aux", "advmod", "rcmod", "cop", "xcomp", 
"partmod","prt", "prepc"] 
relations = ['equal','contain','contained','no relation','other']
numberType = ['singular','plural','unknown']

def readDataFromFile(filename):
    print filename
    llist = []
    for line in codecs.open(filename,'r','utf-8'):
        eachLine = line.strip('\n').split(DATA_DELIMITER)#strip('\n') to remove line feed
        llist.append(eachLine)
            
    print len(llist)

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
        fwrite.flush()
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

DATA_PATH = "/home/lmy/data/new_data/"
PARSER_PATH = "/home/lmy/data/parser/"
FEATURE_PATH = "/home/lmy/data/feature/"
HEADWORD_PATH = "./headword/"

if __name__=="__main__":
    
    #FILE_NAME = "enwiki-instance-concept-1v1.dat"
    FILE_NAME = "enwiki-concept-sub-all-1v1.dat"
    datafile = DATA_PATH+FILE_NAME
    superfile = PARSER_PATH+FILE_NAME.split(".")[0]+"-0column.dat"
    subfile = PARSER_PATH+FILE_NAME.split(".")[0]+"-1column.dat"
    featurefile = FEATURE_PATH+FILE_NAME.split(".")[0]+"-feature9.dat"
    super_headword_file = HEADWORD_PATH+FILE_NAME.split(".")[0]+"-superheadword.dat"
    sub_headword_file = HEADWORD_PATH+FILE_NAME.split(".")[0]+"-subheadword.dat"

    finished = []
    import os
    if os.path.isfile(featurefile):
        for line in codecs.open(featurefile,'r','utf-8'):
            finished.append(line.split(DATA_DELIMITER)[0])
    all_ = []
    for line in codecs.open(datafile,'r','utf-8'):
        all_.append(line.strip("\n").replace(DATA_DELIMITER,FEATURE_ITEM_DELIMITER))

    unfinished = list(set(all_) - set(finished))

    print "ALL:",len(all_)
    print "Finished",len(finished)
    print "Unfinished",len(unfinished)

    del finished
    del all_

    super_items = set([i.split(FEATURE_ITEM_DELIMITER)[0] for i in unfinished])
    sub_items = set([i.split(FEATURE_ITEM_DELIMITER)[1] for i in unfinished])
    
    superl = []
    superD = {}
    superl = readDataFromFile(superfile)
    for item in superl:
        if len(item[2]) <= 0:
            continue
        if item[0] in super_items:
            try:
                superD[item[0]] = SingleSent(item)
            except Exception,e:
                print e
                print item
    print 'finish superD'
    del superl
    
    #superHeadword = dict((k,v.headword) for k,v in superD.iteritems())
    #recordHeadword(HEADWORD_PATH+'super_headword.dat',superHeadword)
    #del superHeadword
    
    subD = {}
    subl = readDataFromFile(subfile)
    for item in subl:
        if len(item[2]) <= 0:
            continue
        if item[0] in sub_items:
            try:
                subD[item[0]] = SingleSent(item)
            except Exception,e:
                print e
                print item
    print 'finish subD'
    del subl
    
    #subHeadword = dict((k,v.headword) for k,v in subD.iteritems())
    #recordHeadword(HEADWORD_PATH+'sub_headword.dat',subHeadword)
    #del subHeadword

    fwrite = codecs.open(featurefile,'a','UTF-8')
    for line in unfinished:
        item = line.strip('\n').split(FEATURE_ITEM_DELIMITER)#strip('\n') to remove line feed
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
        fwrite.flush()
    fwrite.close()
    print 'end'
