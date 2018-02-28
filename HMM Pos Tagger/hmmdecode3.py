import math
import json
import sys


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

def viterbiUtil():
    fhand=open('hmmmodel.txt',encoding='utf8')
    fhand1=open('hmmoutput.txt','w',encoding='utf8')
    bigDict=json.load(fhand)
    countTags=bigDict[0]
    emissionProbab=bigDict[1]
    transProbab=bigDict[2]
    wordCount=bigDict[3]
    nonRare=analyze100(wordCount)
    lenC=list(countTags.keys())
    file_name=sys.argv[1]
    fhand=open(file_name,encoding='utf8')
    badaAnswer=''

    for line in fhand:
        words=line.split()
        tempLine=''
        for word in words:
            #word=word.lower().rstrip()
            if not word in wordCount:
                for indi in lenC:
                    emissionProbab[word+'/'+indi]=1.0

            else:
                tempLine+=word
            tempLine+=' '
        finalList=viterbi(countTags,emissionProbab,transProbab,line.rstrip())
        badaAnswer+=taggedText(finalList,line)
        badaAnswer+='\n'
    badaAnswer=badaAnswer.rstrip()
    fhand1.write(badaAnswer)
    #print('Done')


def taggedText(tags,tempLine):
    ll=tempLine.split()
    for i in range(len(ll)):
        ll[i]=ll[i]+'/'+tags[i]
    tempLine=' '.join(ll)
    return tempLine.rstrip()


def viterbi(countTags,emissionProbab,transProbab,line):
    #Read From File
    #print(line)
    #print countTags
    #print transProbab
    #print emissionProbab
    countTagsKeys=list(countTags.keys())
    #print 'hi'
    #print countTagsKeys
    countTagsKeys.remove('<S>')
    countTagsKeys.remove('</S>')
    countTagsKeys.insert(0,'<S>')
    countTagsKeys.insert(len(countTagsKeys),'</S>')
    words=line.split()
    #print len(words)
    vMatrix = [[0 for x in range(len(words))] for y in range(len(countTags))] #state x observations
    backpointer = [[0 for x in range(len(words))] for y in range(len(countTags))]
    for index in range(1,len(countTagsKeys)-1):
        yo=countTagsKeys[index]+'|'+'<S>'
        yo1=words[0]+'/'+countTagsKeys[index]
        if yo in transProbab and yo1 in emissionProbab:
            vMatrix[index][0]=transProbab[countTagsKeys[index]+'|'+'<S>']*emissionProbab[words[0]+'/'+countTagsKeys[index]]
            #vMatrix[index][0]=(-math.log(transProbab[countTagsKeys[index]+'|'+'<S>']))+(-math.log(emissionProbab[words[0]+'/'+countTagsKeys[index]]))
            backpointer[index][0]='<S>'

    for index in range(1,len(words)):
        for states in range(1,len(countTagsKeys)-1):
            maxx=0.0
            for states1 in range(1,len(countTagsKeys)-1):
                yo=countTagsKeys[states]+'|'+countTagsKeys[states1]
                yo1=words[index]+'/'+countTagsKeys[states]

                if yo in transProbab and yo1 in emissionProbab:


                    temp=vMatrix[states1][index-1]*transProbab[countTagsKeys[states]+'|'+countTagsKeys[states1]]*emissionProbab[words[index]+'/'+countTagsKeys[states]]
                    #temp=vMatrix[states1][index-1]+(-math.log(transProbab[countTagsKeys[states]+'|'+countTagsKeys[states1]]))+(-math.log(emissionProbab[words[index]+'/'+countTagsKeys[states]]))
                    if temp>maxx:
                        maxx=temp
                        backpointer[states][index]=countTagsKeys[states1]

            vMatrix[states][index]=maxx

    maxx=0.0
    xx=0

    for state in range(1, len(countTagsKeys)-1):
        yo='</S>'+'|'+countTagsKeys[state]
        temp=vMatrix[state][len(words)-1]*transProbab['</S>'+'|'+countTagsKeys[state]]
        #temp=vMatrix[state][len(words)-1]+(-math.log(transProbab['</S>'+'|'+countTagsKeys[state]]))
        #print temp
        if temp>maxx and temp != 0:
            #print('bfns')
           # print(state)
            maxx=temp
            xx=1
           # print maxx
            backpointer[len(countTagsKeys)-1][0]=countTagsKeys[state]
            #print 'hh'
            #print backpointer[len(countTagsKeys)-1][0]


    vMatrix[len(countTagsKeys)-1][0]=maxx
    tempTag=backpointer[len(countTagsKeys)-1][0]
    index=countTagsKeys.index(tempTag)
    #print tempTag
    #print 'fuck'
    #print index
    #print(backpointer)
    ii=len(words)
    finalAnswer=[]
    finalAnswer.append(tempTag)
    while ii>0:
        #print 'hii'
        #print countTagsKeys[index]
        ii-=1
        #print('gdjdj')

        tempTag=backpointer[index][ii]
        #print tempTag
        finalAnswer.append(tempTag)
        index=countTagsKeys.index(tempTag)
        #print(tempTag)
        #print(ii)
    finalAnswer=finalAnswer[::-1]
    finalAnswer.pop(0)
    #print(len(line.split()))
    #print (len(finalAnswer))
    return finalAnswer



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



viterbiUtil()
