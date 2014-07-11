#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

ceations = ['equal','contain','contained','no relation','other']
numberType = ['singular','plural','unknown']

class CHSingleSent:
    
    def __init__(self,item):
        #try:
        self.string = item[0]
        self.typedDependency = item[2]
        self.taggedWords = item[1]
        self.taggedD = self.separateTaggedWordToDict(item[1])
        self.allWords = self.taggedD.keys()
        self.headword = self.findHeadword(self.separateTypedDependency(item[2])).split('\0')
        self.hwLen = len(self.headword)
        self.wordLen = len(self.string)
        self.unHeadword = [word for word in self.allWords if word not in self.headword]
        #except:
        #    print "Error"
        #    print item[0]

    def separateTypedDependency(self,tdstr):
        """
        Turn the typedDependency string to a dict(k:typed,v:word)
        str->dict
        """
    
        types = tdstr[1:-1].split('), ')
        ts = {}
        for t in types:
            if len(t) == 0:
                continue
            aa = t.split('(')
            ts[aa[0]]=[s[:s.rfind('-')] for s in aa[1].split(', ') ]
    
        return ts

    def isNoun(self,tag):
        """
        distinguish if the word is a noun
        """
        if tag.isalpha():
            return True if self.taggedD[tag.lower()] in ["NN","NNS","NNP","NNPS"] else False
        else:
            return True

    def findHeadword(self,typed):
        """
        dict(typed dict)->str(headwords, maybe more than one,separated by '\0')
        """
        centerword ="" 
        try:
            if not typed.has_key("root"):
                return self.string
            elif typed.has_key("dobj") and typed["dobj"] != typed["root"]:
                centerword = typed["dobj"][1]
            else:
                centerword = typed["root"][1]
            if typed.has_key("conj"):
                if typed["conj"][0] == centerword:
                    centerword = centerword+"\0"+ typed["conj"][1]
                elif typed["conj"][1] == centerword:
                    centerword = centerword+"\0"+ typed["conj"][0]
        except:
            centerword=self.string
        return centerword

    def separateTaggedWordToDict(self,twstr): #be attantion to the lowercase
        """
        Turn the tagged str to dict(k:word,v:tag)
        str->dict
        """
        ddict = {}
        lTaggedWords = twstr[1:-1].split(', ')
        for tag in lTaggedWords:
            word2tag = tag.split('/')
            key = word2tag[0].lower()
            ddict[key] = word2tag[1]
        return ddict

