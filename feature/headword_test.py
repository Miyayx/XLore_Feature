import codecs

def separateTypedDependency(tdstr):

    types = tdstr[1:-1].split('), ')
    ts = {}
    for t in types:
        if len(t) == 0:
            continue
        aa = t.split('(')
        ts[aa[0]]=[s[:s.rfind('-')] for s in aa[1].split(', ') ]

    return ts

def findHeadword(typed):
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

fread = codecs.open('class-subclass-features.dat','r','utf-8')
super_unknown = []
sub_unknown = []
for line in fread.readlines():
    words = line.strip('\n').split('\t\t')
   # print words
    if not  words[3].find('unknown') == -1:
   #     print line
        super_unknown.append(words[0])
    if not words[4].find('unknown') == -1:
    #    print line
        sub_unknown.append(words[1])
fread.close()

#print super_unknown
#print sub_unknown
super_unknown = list(set(super_unknown))
sub_unknown = list(set(sub_unknown))
print len(super_unknown)
print len(sub_unknown)

fread1=codecs.open('class-taggedword-typeddependency.dat','r','utf-8')
for line in fread1.readlines():
    for item in super_unknown:
        if item == line.strip('\n').split('\t\t')[0]:
           # print line
           pass
fread1.close()

fread2=codecs.open('subclass-taggedword-typeddependency.dat','r','utf-8')
for line in fread2.readlines():
    for item in sub_unknown:
        if item == line.strip('\n').split('\t\t')[0]:
           # print line
           pass
fread2.close()
super_unknown = []
sub_unknown = []
