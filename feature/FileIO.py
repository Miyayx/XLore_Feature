#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from CHSingleSent import *
import codecs

def readDataFromFile(filename):
    """
    str(filename) -> list of list(each list contain two items)
    the file has two columns with separated by '\t\t'
    """
    with codecs.open(filename,'r','utf-8') as f:
        return [line.strip('\n').split('\t') for line in f.readlines()]

def recordHeadword(filename,d):
    """
    (str,dict) -> NoneType
    For English, there maybe more than one headword, so there may be a headwordlist
    """
    with codecs.open(filename,'w','utf-8') as f:
        for k,v in d.items():
            if isinstance(v,list):
                f.write("%s\t"%k)
                for i in v:
                    try:
                        i = en.noun.singular(i)
                    except: pass
                    f.write("\t%s"%i)
                f.write("\n")
            else:
                f.write("%s\t\t%s\n"%(k,v))


def readTwoColumnsToDict(filename,reverse=False,delimiter='\t\t'):
    d = {}    
    f = codecs.open(filename,'r','utf-8')
    while True:
        line = f.readline()
        if not line:
            break
        eachLine = line.strip('\n').split(delimiter)
        if reverse:
            if not d.has_key(eachLine[1]):
                d[eachLine[1]] = []
            d[eachLine[1]].append(eachLine[0])
        else:
            if not d.has_key(eachLine[0]):
                d[eachLine[0]] = []
            d[eachLine[0]].append(eachLine[1])
    print len(d)
    f.close()
    return d
