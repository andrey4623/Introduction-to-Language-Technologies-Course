#!/usr/bin/env python
#coding: utf8

# Copyright (c) 2015, Andrey Kolchanov.  All rights reserved.

import sys

keywords= ["plus", "times", "divided by", "how much is", "minus", "add", "and"]

#number words to integer on English
def englishText2int(textnum, numwords={}):
    if not numwords:
        units = [
                 "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                 "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                 "sixteen", "seventeen", "eighteen", "nineteen",
                 ]
            
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
                
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
                    
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            return None #raise Exception("Illegal word: " + word)
            
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
        
    return result + current

#number words to integer on Russian
def russianText2int(txtnum):
    trillion = ["","триллионов", "триллиона", "триллион"]
    billion = ["","миллиардов", "миллиарда", "миллиард"]
    millions = ["","миллионов", "миллиона", "миллион"]
    thousands = ["","тысяч", "тысяча", "тысячи"]

    hundreds = ["", "сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот"]
    tens = ["", "", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
    units = [
             "ноль", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь",
             "девять", "десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать",
             "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать",
             ]
             
    for word in txtnum.split():
        if (word not in trillion)and(word not in billion)and(word not in millions)and(word not in thousands)and(word not in hundreds)and(word not in tens)and(word not in units):    return None
    
    current = result = 0

    for i in range(len(trillion)-1,0,-1):
        if (txtnum.find(trillion[i])>-1):
            strOne =txtnum[:txtnum.find(trillion[i])]
            strTwo =txtnum[txtnum.find(trillion[i])+len(trillion[i])+1:]
            if ((strOne=="")and (strTwo=="")):
                return 1000000000000
            return  russianText2int(strOne)*1000000000000+ russianText2int(strTwo)


    for i in range(len(billion)-1,0,-1):
        
        if (txtnum.find(billion[i])>-1):
            
            strOne =txtnum[:txtnum.find(billion[i])]
            strTwo =txtnum[txtnum.find(billion[i])+len(billion[i])+1:]
            if ((strOne=="")and (strTwo=="")):
                return 1000000000
            else:   return  russianText2int(strOne)*1000000000+ russianText2int(strTwo)


    for i in range(len(millions)-1,0,-1):
        if (txtnum.find(millions[i])>-1):
            strOne =txtnum[:txtnum.find(millions[i])]
            strTwo =txtnum[txtnum.find(millions[i])+len(millions[i])+1:]
            if ((strOne=="")and (strTwo=="")):
                return 1000000
            return  russianText2int(strOne)*1000000+ russianText2int(strTwo)

    for i in range(len(thousands)-1,0,-1):
        if (txtnum.find(thousands[i])>-1):
            strOne =txtnum[:txtnum.find(thousands[i])]
            strTwo =txtnum[txtnum.find(thousands[i])+len(thousands[i])+1:]
            if ((strOne=="")and (strTwo=="")):
                return 1000
            return  russianText2int(strOne)*1000+ russianText2int(strTwo)

    for i in range(len(hundreds)-1,0,-1):
        if ((txtnum.find(hundreds[i])>-1)and(len(hundreds[i])>0)):
            result = i*100;
            txtnum = txtnum.replace(hundreds[i], '')
            break

    for i in range(0,len(tens)):
        if ((txtnum.find(tens[i])>-1)and(len(tens[i])>0)):
            result += i*10;
            txtnum = txtnum.replace(tens[i], '')
            break

    for i in range(len(units)-1,0,-1):
        if (txtnum.find(units[i])>-1):
            result += i;
            break

    return result

#number words to integer  - universal
def numberWordsToInteger(lang, text):
    if (lang=="en"):
        return englishText2int(text)
    elif (lang=="ru"):
        return russianText2int(text)


#load rules
fname='rules.txt'
rules = [line.strip() for line in open(fname)]


#get source language
if (len(sys.argv)<3):
    print "No enough arguments"
    sys.exit()

sourceLanguage = sys.argv[1]

#get source text
input=''
for arg in range(2,len(sys.argv)):
    input+=sys.argv[arg]+' '

#preprocessing
input = input.lower()
input = input.strip()

#if len is zero
if (len(input)==0):
    print "No input string"
    sys.exit()

#applying the rules
for rule in rules:
    command = rule[:rule.find(' ')]
    if (command=='replace'):
        rule = rule[rule.find('replace ')+9:]
        stringOne = rule[:rule.find('\'')]
        rule = rule[rule.find('\'')+2:]
        stringTwo = rule[1:-1]
        #apply replace rule
        input = input.replace(stringOne, stringTwo)


#parse
arr = []

while (len(input)>0):
    lowerWord=keywords[0]
    lowerValue=99999999
    for h in keywords:
        pos = input.find(h)
        if ((pos<lowerValue)and(pos>-1)):
            lowerValue=pos
            lowerWord = h
    if (lowerValue<99999999):
        if (lowerValue==0):
            s1 =input[:len(lowerWord)]
            arr.append(s1)
            input = input[len(lowerWord)+1:]
        else:
            s1 =input[:lowerValue-1]
            s2 =input[lowerValue:lowerValue+len(lowerWord)]
            arr.append(s1)
            arr.append(s2)
            input = input[lowerValue+len(lowerWord)+1:]
    elif (lowerValue==99999999):
        if (len(input)>0):
            arr.append(input)
            input=''


arr2=[]
for collocation in arr:

    if (collocation.find("point")>-1):
        #fractional number
        stringFirst=collocation[:collocation.find("point")-1]
        stringSecond=collocation[collocation.find("point")+6:]
        intFirst = numberWordsToInteger(sourceLanguage, stringFirst)
        if (intFirst==None):    intFirst=0
        intSecond = numberWordsToInteger(sourceLanguage, stringSecond)
        strTemp = str(intFirst)+'.'+str(intSecond)
        decimal =float(strTemp)
        
        arr2.append(decimal)
    else:
        res = numberWordsToInteger(sourceLanguage, collocation)
        if (res!=None):
            value=1.0*res
            arr2.append(value)
        else:
            if (collocation.isdigit()):
                #print "YES"
                arr2.append(1.0*int(collocation))
            else:
                arr2.append(collocation)

#calculation
for y in range(0,len(arr2)):
    stop=0
    while ((len(arr2)>=3)and(stop==0)):
        for x in range(0,len(arr2)):
            if (x+2<len(arr2)):
                if ((type(arr2[x]) is float)and(type(arr2[x+1]) is str)and(type(arr2[x+2]) is float)):
                    if (arr2[x+1]=="add"):
                        arr2[x] = arr2[x]+arr2[x+2]
                        arr2.remove(arr2[x+2])
                        arr2.remove(arr2[x+1])
                        break
                    elif (arr2[x+1]=="minus"):
                        arr2[x] = arr2[x]-arr2[x+2]
                        arr2.remove(arr2[x+2])
                        arr2.remove(arr2[x+1])
                    elif (arr2[x+1]=="times"):
                        arr2[x] = arr2[x]*arr2[x+2]
                        arr2.remove(arr2[x+2])
                        arr2.remove(arr2[x+1])
                    elif (arr2[x+1]=="divided by"):
                        arr2[x] = arr2[x]/arr2[x+2]
                        arr2.remove(arr2[x+2])
                        arr2.remove(arr2[x+1])
                    else:
                        stop=1
                else:
                    stop=1
            else:
                stop=1
            stop=1


#output
output=''
for d in arr2:
    output+=str(d)+' '

print output