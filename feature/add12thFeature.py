#!/usr/bin/env python2.7
#encoding=utf-8

"""
This program add the 12th feature to file.
Read the previous 11 features, Read class from class-subclass.dat so that sequence can be reserved. Then write 12th with them.
"""

import codecs

DATAFILE = 'wiki-class-subclass.dat'
FEATURE12th = 'wiki-class-subclass-ishyper.dat'
FEATURE11_FILE = '../data/wiki-class-subclass-11features.dat'
FEATURE12_FILE = '../data/wiki-class-subclass-12features.dat'

c = []
with codecs.open(DATAFILE,'r','utf-8') as f:
    c = [line.strip('\n') for line in f.readlines()]

#read the 12th feature to memory
d = {}
with codecs.open(FEATURE12th,'r','utf-8') as f:
    for line in f.readlines():
        items = line.strip('\n').split('\t\t')
        if len(items) == 3:
            d[items[0]+'\t\t'+items[1]] = eval(items[2])
        elif len(items) < 3:
            d[items[0]] = eval(items[1])

rf = codecs.open(FEATURE11_FILE,'r','utf-8')
wf = codecs.open(FEATURE12_FILE,'w','utf-8')
count = 0
for line in rf.readlines():
    classStr = c[count]
    classes = c[count].split('\t\t')
    count = count+1
    features = line.strip('\n').split('\t\t')[1]
    wf.write('%s\t%s\t\t%s,%d\n'%(classes[0],classes[1],features,d[classStr]))
rf.close()

