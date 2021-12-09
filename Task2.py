#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re


# In[2]:


def splitBySeparators(lineToSlit, reg):
    return re.sub(reg, ' ', lineToSlit).split()


# In[3]:


def addElemntToMap(mapOfWord, word, linecounter):
    if word in mapOfWord:
        mapOfWord[word].append(linecounter)
    else:
        mapOfWord[word] = [linecounter]
    return mapOfWord


# In[8]:


def analiseNotBaseCase(statOfWords, linecounter, wordToanalyse):
    word = None 
    for charIndex in range(len(wordToanalyse)):
        char = wordToanalyse[charIndex]
        if word ==None and char!='.':
            word = char
        elif char.isdigit():
            if word[-1].isdigit() or word[-1]=='.':
                word = word + char
            else:
                statOfWords = addElemntToMap(statOfWords,word,linecounter)
                word = char
        elif char.isdigit() and word[-1].isalpha():
            statOfWords = addElemntToMap(statOfWords,word,linecounter)
            word = char
        elif char.isalpha() and word[-1].isdigit():
            statOfWords = addElemntToMap(statOfWords,word,linecounter)
            word = char
        elif char.isalpha() and word[-1].isalpha():
            word = word+char
        elif char == '.' and word!=None:
            if wordToanalyse[charIndex-1].isdigit() and charIndex+1<len(wordToanalyse) and wordToanalyse[charIndex+1].isdigit() and not '.' in word:
                word= word+char
            elif word!=None:
                statOfWords = addElemntToMap(statOfWords,word,linecounter)
                word = None
    if word !=None:
        statOfWords = addElemntToMap(statOfWords,word,linecounter)
    return statOfWords


# In[9]:


def makeStats(filepath, encodingType):
    outPutMap = {} 
    separatorsForWords = "[\\\\!\"#$%&,\'()\*\+\-/:;\?\^_`{|}~]"
    numbersRegex = "^([0-9]+\d*([.]\d+)?)$|^(-?0[.]\d*[1-9]+)$|^0$|^0.0"
    try:
        with open(filepath,"r",encoding=encodingType) as file:
            linecounter=0
            for line in file:
                linecounter= linecounter+1
                words = splitBySeparators(line,separatorsForWords)
                for word in words:
                    if bool(re.match(numbersRegex, word)) or word.isalpha():
                        addElemntToMap(outPutMap,word,linecounter)
                    else:    
                        outPutMap = analiseNotBaseCase(outPutMap,linecounter,word)
    except FileNotFoundError:
        print('File not Found')
    return outPutMap


# In[13]:


#print(makeStats('task.txt','utf-8'))
