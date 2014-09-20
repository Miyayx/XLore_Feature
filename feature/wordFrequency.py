import codecs
DATA_PATH = '/home/lmy/data/origin/'
FEATURE_PATH = '/home/lmy/data/feature/'

FILE_NAME=  'enwiki-instance-concept-1v1.dat'
FEATURE9 =  'enwiki-instance-concept-1v1-feature9.dat'
FEATURE11 = 'enwiki-instance-concept-1v1-feature11.dat'

def readTwoColumnsToDict(filename,reverse = False):
    d = {}    
    f = codecs.open(filename,'r','utf-8')
    for line in f.readlines():
        eachLine = line.strip('\n').split('\t\t')
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

def calculateWordFrequency(d):
    allFreD = {}
    for key in d:    
        freD = {}
        totalWord = 0
        allFreD[key] = {}
        for i in d[key]:
            ss = i.split(' ')
            for s in ss:
                totalWord = totalWord+1
                if freD.has_key(s):
                    freD[s] = freD[s]+1
                else: freD[s] = 1
        for i in d[key]:
            ss = i.split(' ')
            fre = 0
            for s in ss:
                fre = fre+freD[s]
            allFreD[key][i] =float(fre)/totalWord*len(d[key])
    return allFreD

ddict = readTwoColumnsToDict(DATA_PATH+FILE_NAME )
fD = calculateWordFrequency(ddict)
dddict = readTwoColumnsToDict(DATA_PATH+FILE_NAME ,True)
ffD = calculateWordFrequency(dddict)

rf = codecs.open(DATA_PATH+FILE_NAME,'r','utf8')
c = []
for line in rf.readlines():
    c.append(line.strip('\n'))
rf.close()

rf = codecs.open(FEATURE_PATH+FEATURE9,'r','utf-8')
wf = codecs.open(FEATURE_PATH+FEATURE11,'w','utf-8')
count = 0
for line in rf.readlines():
    classes = c[count].split('\t\t')
    count = count+1
    features = line.strip('\n').split('\t\t')[1]
    wf.write('%s\t%s\t\t%s,%.3f,%.3f\n'%(classes[0],classes[1],features,fD[classes[0]][classes[1]],ffD[classes[1]][classes[0]]))
rf.close()
wf.close() 
ddict = {}
fD = {}
c = []

print 'end'
