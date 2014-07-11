#!usr/bin/env python2.7
#encoding=utf-8

ID_TITLE1 = '/home/zigo/SemantifyWiki/etc/dataset/wc-id-title.dat'
ID_TITLE2 = '/home/zigo/SemantifyWiki/etc/dataset/wc-id-title.dat'
ID_ID = '/home/zigo/SemantifyWiki/etc/dataset/sample-2.dat'
TITLE_TITLE = '/home/zigo/SemantifyWiki/etc/dataset/sample-2-title.dat'
TITLE_FEATURE = '/home/lmy/data/CLKB/sample-2-title-11features.dat'
ID_FEATURE = '/home/lmy/data/CLKB/sample-2-11features.dat'

id_title = {}
title_id = {}
with open(ID_TITLE1) as f:
    line = f.readline()
    while line:
        s = line.strip().split('\t')
        if len(s) < 2:
            s.append('')
        id_title[s[0]] = s[1]
        title_id[s[1]] = s[0]
        line = f.readline()
if ID_TITLE1 != ID_TITLE2:
    with open(ID_TITLE2) as f:
        line = f.readline()
        while line:
            s = line.strip().split('\t')
            if len(s) < 2:
                s.append('')
            id_title[s[0]] = s[1]
            title_id[s[1]] = s[0]
            line = f.readline()

#with open(ID_ID) as f:
#    tf = open(TITLE_TITLE,'w')
#    line = f.readline()
#    while line:
#        s = line.strip().split(',')
#        tf.write(id_title[s[0]]+'\t\t'+id_title[s[1]]+'\n')
#        line = f.readline()
#    tf.close()

with open(TITLE_FEATURE) as f:
    tf = open(ID_FEATURE,'w')
    line = f.readline()
    while line:
        titles = line.strip().split('\t\t')[0]
        features = line.strip().split('\t\t')[1]
        t1 = titles.split('\t')[0]
        t2 = titles.split('\t')[1]
        tf.write(title_id[t1]+','+title_id[t2]+'\t'+features+'\n')
        line = f.readline()
    tf.close()
    
