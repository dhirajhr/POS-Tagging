import math
import json
import sys
def fileProcess():
    file_name=sys.argv[1]
    countTags=dict()#key value pair where value is a list with 0th element being total cnt and 1st being second last
    countEmissionNum=dict()
    countDoubleTags=dict()
    wordCount=dict()
    totalDistTags=dict()
    countTripleTags=dict()
    emissionProbabilities=dict()
    transProbabilities=dict()
    #fhand=open('en_train_tagged.txt',encoding='utf8')
    fhand=open(file_name,encoding='utf8')
    #fhand=open('filee.txt')
    totalTagCount=0;
    for line in fhand:
        words=line.split()
        for word in words:
            tempT=word.rsplit('/',1)
            #tempT[0]=tempT[0].lower()
            if not tempT[0] in wordCount:
                wordCount[tempT[0]]=1
            else:
                wordCount[tempT[0]]+=1
    #print 'word coount'
    #print wordCount
    rareWords=analyze101(wordCount)
    nonRare=analyze100(wordCount)
    #print nonRare
    fhand=open(file_name,encoding='utf8')
    #fhand=open('en_train_tagged.txt',encoding='utf8')
    cntrrr=0
    for line in fhand:
        line=line.rstrip()
        totalTagCount+=len(line.split())
        temp=tagify(line)
        cntr=0
        for tag in temp:
            cntr+=1
            #totalTagCount+=1
            if not tag in countTags:
                countTags[tag]=[1,0]
            else:
                countTags[tag][0]+=1
            if cntr<len(temp)-1:
                    countTags[tag][1]+=1
        words=line.split()
        for word in words:
            '''tempo=word.rsplit('/',1)
            delimeter='/'
            #tempo[0]=tempo[0].lower()
            if tempo[0] in rareWords:
                tempo[0]='_RARE_'
                cntrrr+=1
            word=delimeter.join(tempo)
                #print word'''
            if not word in countEmissionNum:
                countEmissionNum[word]=1
            else:
                countEmissionNum[word]+=1
    for observe in countEmissionNum:
        temp=observe.rsplit('/',1)
      #  print countTags[temp[1]]
        eProbab=float(countEmissionNum[observe])/float(countTags[temp[1]][0])
        emissionProbabilities[observe]=eProbab
    #print cntrrr
#double
    #fhand=open('filee.txt')
    #fhand=open('en_train_tagged.txt',encoding='utf8')
    fhand=open(file_name,encoding='utf8')
    for line in fhand:
        line=line.rstrip()
        temp=tagify(line)
        delimeter='@@'
        for index in range(len(temp)-1):
            doubleKey=delimeter.join(temp[index:index+2])
            if not doubleKey in countDoubleTags:
                countDoubleTags[doubleKey]=[1,0]
            else:
                countDoubleTags[doubleKey][0]+=1
        for index in range(len(temp)-3):
            doubleKey=delimeter.join(temp[index:index+2])
            countDoubleTags[doubleKey][1]+=1
#Triple
    #fhand=open('filee.txt')
    #fhand=open('en_train_tagged.txt',encoding='utf8')
    fhand=open(file_name,encoding='utf8')
    for line in fhand:
        temp=tagify(line)
        delimeter='@@'
        for index in range(len(temp)-2):
            tripleKey=delimeter.join(temp[index:index+3])
            if not tripleKey in countTripleTags:
                countTripleTags[tripleKey]=1
            else:
                countTripleTags[tripleKey]+=1

    #print wordCount
    #print len(countTags)
    #print len(countDoubleTags)
    #print len(countTripleTags)
    #lambdaValues=deletedInterpolation(countTags,countDoubleTags,countTripleTags,totalTagCount)
    transProbabilities=transCalculate(countTags,countDoubleTags,countTripleTags,totalTagCount)

    writeToFile(countTags,emissionProbabilities,transProbabilities,wordCount)


def analyze100(dictt):
    newDict=[]
    for i in dictt:
        if dictt[i]>3:
            newDict.append(i)
    return set(newDict)

def analyze101(dictt):
    newDict=[]
    for i in dictt:
        if dictt[i]<=3:
            newDict.append(i)
    return set(newDict)

def writeToFile(countTags,emission,transition,wordCount):
    fhand =open('hmmmodel.txt','w',encoding='utf8')
    c=json.loads("[{},{},{},{}]".format(json.dumps(countTags), json.dumps(emission), json.dumps(transition), json.dumps(wordCount)))
    fhand.write(json.dumps(c))




def taggedText(tags,tempLine):
    ll=tempLine.split()
    for i in range(len(ll)):
        ll[i]=ll[i]+'/'+tags[i]
    tempLine=' '.join(ll)
    return tempLine.rstrip()




#Viterbi
def tagify(line):
    listTags=[]
    listTags.append('<S>')
    #listTags.append('<S>')
    words=line.split()
    for word in words:
        temp=word.rsplit('/',1)
        listTags.append(temp[1])
    listTags.append('</S>')
    return listTags


def transCalculate(countTags,countDoubleTags,countTripleTags,totalCount):
    transProab=dict()
    V=len(countTags)
    Vtags=countTags.keys()
    for doubletag in countDoubleTags:
        delimeter='@@'
        temp=doubletag.split('@@')
        if float(countTags[temp[0]][1])!=0.0:
            transProab[temp[1]+'|'+temp[0]]=float(countDoubleTags[doubletag][0]+1.0)/float(countTags[temp[0]][1]+V**3)
    for i1 in Vtags:
        for i2 in Vtags:
            temp=i1+'|'+i2
            if temp not in transProab:
                transProab[temp]=1.0/(float(countTags[i2][1]+V**3))
    return transProab

fileProcess()
