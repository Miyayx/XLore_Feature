#!/usr/bin/env python2.7
#encoding=utf-8
import codecs
from CHSingleSent import *
import FileIO
import threading

DATAFILE='/home/zigo/SemantifyWiki/etc/dataset/sample-5-title.dat'
SUPER_FILE='/home/lmy/data/parser/ha-title-taggedword-typeddependency.dat'
SUB_FILE='/home/lmy/data/parser/hc-title-taggedword-typeddependency.dat'

FEATURE9='/home/lmy/data/CLKB/sample-5-9features.dat'
FEATURE11='/home/lmy/data/CLKB/sample-5-11features.dat'

SUPER_HEADWORD_FILE = 'sample-5-headword-super.dat'
SUB_HEADWORD_FILE = 'sample-5-headword-sub.dat'

delimiter = '\t\t'

relations = ['equal','contain','contained','no relation','other']

def getStr2ObjectDict(filename):
    """
    str(filename) -> list of CHSingleSent
    """
    l = FileIO.readDataFromFile(filename)
    return dict([item[0],CHSingleSent(item)] for item in l )

def getRelationshipOfTwoSets(l1,l2):
    """
    get the relationship of two classes' headword collection
    two list of headwords -> int(relationshipID)
    relations = ['equal','contain','contained','no relation','other']
    """
    oldLen1 = len(set(l1))
    oldLen2 = len(set(l2))
    mergeList = l1
    mergeList.extend(l2)
    mergeLen = len(set(mergeList))
    if oldLen1 == mergeLen and oldLen2 == mergeLen:
        #return relations[0]
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
        return 4
        #return relations[4]

def getRalationshipOfTwoSets2(l1,l2):
    """
    get the relationship of two classes' headword and unheadword collection
    two list of headwords -> int(relationshipID)
    relations just include 'no relation' and 'other' 
    """
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

def recordInputtedFile(newfile):
    inputted_lines = []
    try:
       with codecs.open(newfile,'r','utf-8') as f:
           while True:
               line = f.readline()
               if not line:
                   break
               inputted_lines.append(line.strip('\n').split('\t\t')[0])
    except:
        pass
    return inputted_lines

def writeFeatureToFile(superD,subD,super_sub_freD,sub_super_freD,newfile,datafile):
    """
    (str,str) -> NoneType
    str is file name,first is feature-record file, second is class-subclass file

    Order of features:
    1. Relationship of super headword and subclass headword (look at the relation list )
    2. If sub(the whole string) starts with super(the whole string)
    3. If sub(the whole string) ends with super(the whole string)
    4. Length of superclass headword set
    5. Length of subclass headword set
    6. Length of superclass string
    7. Length of subclass string
    8. Relationship of superclass headwords set and subclass unheadword set
    9. Relationship of subclass headwords set and superclass unheadword set
    10.Frequency ratio a sub string's words appear to in the same super 
    11.Frequency ratio a super string's words appear to in the same sub 
    12.
    
    Output format:
    superclass\tsubclass\t\tf1,f2,f3....\n
    """
    recorded_items = recordInputtedFile(newfile)
    print "Have recorded",len(recorded_items),"items"
    fread = codecs.open(datafile,'r','utf-8')
    fwrite = codecs.open(newfile,'a','utf-8')
    for i in range(0,len(recorded_items)):
        line = fread.readline()
    while True:
        line = fread.readline()
        if not line:
            break
        item = line.strip('\n').split(delimiter)
        superStr = item[0]
        subStr = item[1]
        if len(subStr) == 0:
            print "subStr",subStr
            print "no sub"
            continue
        try:
            superS = superD[superStr]
            subS = subD[subStr]
        except:
            print superStr
            print subStr
            continue
        relation = getRelationshipOfTwoSets(superS.headword,subS.headword)
        relation8 = getRalationshipOfTwoSets2(superS.headword,subS.unHeadword)
        relation9 = getRalationshipOfTwoSets2(subS.headword,superS.unHeadword)
        print "write one line"
        fwrite.write('%s\t%s\t\t%d,%d,%d,%d,%d,%d,%d,%d,%d,%.3f,%.3f\n'%(
            superStr,subStr,relation,
            1 if subStr.startswith(superStr) else 0,
            1 if subStr.endswith(superStr) else 0,
            superS.hwLen,subS.hwLen,superS.wordLen,subS.wordLen,
            relation8,relation9,
            super_sub_freD[superStr][subStr],
            sub_super_freD[subStr][superStr]))
        fwrite.flush()
    fread.close()
    fwrite.close()

def calculateWordFrequency(d):
    """
    dict(k:str v:list of related string) -> dict(k:str v:dict of [k:str v:ratio])
    example:
    d['aaa'] = ['dwd','fgse','sdf']
    for key == 'aaa' in d:
    totalWord = 3+4+3 = 10
    freD = {'d':3,'w':1,'f':2,'g':1,'s':2,'e':1} 
    when key=='aaa', i =='dwd'
    fre = 3+1+3 = 7
    allFreD['aaa']['dwd']=7/10*3
    """
    #for k,v in d.items():
    #    print k,v
    allFreD = {}
    for key in d:    
        freD = {}
        totalWord = 0
        allFreD[key] = {}
        for i in d[key]:
            ss = list(i)
            for s in ss:
                totalWord = totalWord+1
                if freD.has_key(s):
                    freD[s] = freD[s]+1
                else: freD[s] = 1
        for i in d[key]:
            ss = list(i)
            fre = 0
            for s in ss:
                fre = fre+freD[s]
            #print key
            try:
                allFreD[key][i] =float(fre)/totalWord*len(d[unicode(key)])
            except:
                continue
    return allFreD

if __name__ == '__main__':
    superD = {}
    def fun_a():
        print "Calculating Object of super..."
        global superD
        superD = getStr2ObjectDict(SUPER_FILE)
        superHeadword = dict((k,v.headword) for k,v in superD.iteritems())
        FileIO.recordHeadword(SUPER_HEADWORD_FILE,superHeadword)
        superHeadword = {}

    subD = {}
    def fun_b():
        print "Calculating Object of sub..."
        global subD
        subD = getStr2ObjectDict(SUB_FILE)
        subHeadword = dict((k,v.headword) for k,v in subD.iteritems())
        FileIO.recordHeadword(SUB_HEADWORD_FILE,subHeadword)
        subHeadword = {}

    super_sub_freD = {}
    sub_super_freD = {}
    def fun_c():
        print "Calculating frequency..."
        global super_sub_freD,sub_super_freD
        ddict = FileIO.readTwoColumnsToDict(DATAFILE,delimiter='\t\t')
        super_sub_freD = calculateWordFrequency(ddict)
        dddict = FileIO.readTwoColumnsToDict(DATAFILE,True,delimiter='\t\t')
        sub_super_freD = calculateWordFrequency(dddict)
    
    threads = []
    threads.append(threading.Thread(target=fun_a))
    threads.append(threading.Thread(target=fun_b))
    threads.append(threading.Thread(target=fun_c))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    
    print "Writing to file..."
    writeFeatureToFile(superD,subD,super_sub_freD,sub_super_freD,FEATURE11,DATAFILE)

