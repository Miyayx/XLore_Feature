ceations = ['equal','contain','contained','no relation','other']
numberType = ['singular','plural','unknown']

class SingleSent:
    
    def __init__(self,item):
        self.string = item[0]
        self.typedDependency = item[2]
        self.taggedWords = item[1]
        self.taggedD = self.separateTaggedWordToDict(item[1])
        self.headword = self.findHeadword(self.separateTypedDependency(item[2])).split('\0')
        self.hwNumber = self.getHeadWordType(self.taggedD)
        self.hwLen = len(self.headword)
        self.wordLen = len(self.string.split(' '))
        self.unHeadword = []
        for s in self.headword:
            if s in self.string.split(' '):
                self.unHeadword = self.string.split(' ')
                self.unHeadword.remove(s)

        # Delete no use value for free memory
        self.typedDependency = None
        self.taggedWords = None
        self.taggedD = None

    def separateTypedDependency(self,tdstr):
    
        types = tdstr[1:-1].split('), ')
        ts = {}
        for t in types:
            if len(t) == 0:
                continue
            aa = t.split('(')
            ts[aa[0]]=[s[:s.rfind('-')] for s in aa[1].split(', ') ]
        return ts

    def isNoun(self,tag):
        if tag.isalpha():
            return True if self.taggedD[tag.lower()] in ["NN","NNS","NNP","NNPS"] else False
        else:
            return True

    def findHeadword(self,typed):
        centerword = ""

        if not typed.has_key("root"):
            return "\t"
        if typed.has_key("dobj"):
            centerword = typed["dobj"][1]
        elif typed.has_key("nsubj") and typed["nsubj"][1].isalpha() and not self.separateTaggedWordToDict(self.taggedWords)[typed["nsubj"][1].lower()] == "PRP":
            centerword = typed["nsubj"][1]
        elif typed.has_key("nsubj") and typed["nsubj"][0] == typed["root"][1]:
            centerword = typed["nsubj"][0]
        elif typed.has_key("prep_in"):
            centerword = typed["prep_in"][0]
        elif typed.has_key("prep_of"):
            centerword = typed["prep_of"][0]
        elif typed.has_key("prep_from"):
            centerword = typed["prep_from"][0]
        elif typed.has_key("prep_at"):
            centerword = typed["prep_at"][0]
        elif typed.has_key("dep"):
            if typed["dep"][1].isalpha() and self.isNoun(typed["dep"][1]) and typed["dep"][0].isalpha() and self.isNoun(typed["dep"][0]):
               centerword = typed["dep"][1]
            elif typed["dep"][0].isalpha() and self.isNoun(typed["dep"][0]):
               centerword = typed["dep"][0]
            elif typed["dep"][1].isalpha() and self.taggedD[typed["dep"][1].lower()] == "IN":
               centerword = typed["dep"][0]
            elif typed["dep"][1].isalpha() and self.isNoun(typed["dep"][1]):
               centerword = typed["dep"][1]
            else: centerword = typed["root"][1]
        elif typed.has_key("advmod"):
            centerword = typed["advmod"][1]
        elif typed.has_key("amod"):
            if typed["root"][1] == typed["amod"][0]:
                centerword = typed["root"][1]
            elif (typed.has_key("dep") and typed["amod"][0] == typed["dep"][1]) or (typed.has_key("nn") and typed["amod"][0] == typed["nn"][0]):
                 centerword = typed["amod"][0]
            else:
                centerword = typed["amod"][0]
        elif typed.has_key("nn"):
            centerword = typed["nn"][0]
        else:
            centerword = typed["root"][1]
        
        #centerword = centerword if self.isNoun(centerword) else typed["root"][1] if self.isNoun(typed["root"][1]) else centerword

        if typed.has_key("conj_and"):
            if typed["conj_and"][0] == centerword:
                centerword = centerword+"\0"+ typed["conj_and"][1]
            elif typed["conj_and"][1] == centerword:
                centerword = centerword+"\0"+ typed["conj_and"][0]
        return centerword

    def separateTaggedWordToDict(self,twstr): #be attantion to the lowercase
        ddict = {}
        lTaggedWords = twstr[1:-1].split(', ')
        for tag in lTaggedWords:
            try:
                word2tag = tag.split('/')
                key = word2tag[0].lower()
                ddict[key] = word2tag[1]
            except:
                print tag
        return ddict

    def getHeadWordType(self,taggedDict):
        dd = {}
        if self.headword == '\t':
            return
        headW = self.headword
        for i in headW:
            if taggedDict.has_key(i.lower()):
                if taggedDict[i.lower()] in ["NN","NNP"]:
                    t = "singular"
                elif taggedDict[i.lower()] in ["NNS","NNPS"]:
                    t = "plural"
                else:
                    t = "unknown"
                dd[i] = t       
        #return dd
        return 1 if 'plural' in dd.values() else 0 if 'singular' in dd.values() else 2 
     
