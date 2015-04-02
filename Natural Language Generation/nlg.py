#!/usr/bin/env python
#coding: utf8

# Copyright (c) 2015, Andrey Kolchanov.  All rights reserved.

#This code creates a human-like report from a hockey log.

#filename for an input file
filename = 'Hockey_Log.xlsx'
#name of a sheet
sheetname = 'Avto-Neft'
#skeaker: jane or zahar
speaker='jane'
#private api key
key='' #https://tech.yandex.ru/speechkit/cloud/doc/dg/concepts/speechkit-dg-tts-docpage/


import openpyxl as px
import numpy as np

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import requests
from time import time
import os

# --- Classes defenition ---

# class player
class Player:
    number=None
    name=None
    position=None
    def __init__(self, number, name, position):
        self.number = number
        self.name = name
        self.position = position

# class play
class Play:
    period=None
    play=None
    min=None
    eventAction=None
    team=None
    actor=None
    fromLoc=None
    toLoc=None
    actor2=None
    actor3=None
    outcome=None
    def __init__(self, period, play, min, eventAction, team, actor, fromLoc, toLoc, actor2, actor3, outcome):
        self.period = period
        self.play = play
        self.min = min
        self.eventAction = eventAction
        self.team = team
        self.actor = actor
        self.fromLoc = fromLoc
        self.toLoc = toLoc
        self.actor2 = actor2
        self.actor3 = actor3
        self.outcome = outcome

# class game
class Game:
    date=None
    arena=None
    city=None
    attendance=None
    hometeam=None
    guestteam=None
    hometeamFinalScore=None
    guestteamFinalScore=None
    hometeamPlayers=[]
    guestteamPlayers=[]
    plays=[]
    def getPlayerName(self, team, number):
        if (team==self.hometeam):
            for x in self.hometeamPlayers:
                if (x.number == number):
                    return x.position+' '+ x.name
        elif (team==self.guestteam):
            for x in self.guestteamPlayers:
                if (x.number == number):
                    return x.position+' '+x.name
        return 'Unknown'
    def getPlaysbyPlayValue(self, playValue):
        result=[]
        for x in self.plays:
            if (x.play==playValue):
                result.append(x)
        return result

# --- Function defenition ---

# Parse an input xlsx file
def readGameReportFromExcelFile (filename, sheetname):
    game=Game()

    #open xlsx file
    W = px.load_workbook(filename, use_iterators = True)
    #get a required sheet
    p = W.get_sheet_by_name(name = sheetname)
    #for parsing
    i=0;
    j=0;


    GAME_DESCRIPTION_SECTION=0
    HOME_TEAM_SECTION=1
    GUEST_TEAM_SECTION=2
    FIRST_PERIOD_SECTION=3
    SECOND_PERIOD_SECTION=4
    THIRD_PERIOD_SECTION=5
    OVERTIME_SECTION=6
    SHOOTOUT_SECTION=7
    FINALSCORE_SECTION=8
    #the first section
    section = GAME_DESCRIPTION_SECTION


    #parse the file
    for row in p.iter_rows():
        for k in row:
            if (k.value=='home-team'):
                section = HOME_TEAM_SECTION
                continue
            if (k.value=='guest-team'):
                section = GUEST_TEAM_SECTION
                continue
            if (k.value=='Play'):
                section = FIRST_PERIOD_SECTION
                continue
            if (k.value=='End of first period'):
                section = SECOND_PERIOD_SECTION
                continue
            if (k.value=='End of second period'):
                section = THIRD_PERIOD_SECTION
                continue
            if (k.value=='End of third period'):
                section=OVERTIME_SECTION
                continue
            if (k.value=='End of overtime'):
                continue
            if (k.value=='Shootout'):
                section = SHOOTOUT_SECTION
                continue
            if (k.value=='Final score'):
                section = FINALSCORE_SECTION
                continue

            if (section==GAME_DESCRIPTION_SECTION):
                if ((i==1)and(j==0)):#date
                    game.date = k.value
                if ((i==1)and(j==1)):#arena
                    game.arena = k.value
                if ((i==1)and(j==2)):#city
                    game.city = k.value
                if ((i==1)and(j==3)):#Attendance
                    game.attendance = k.value
                if ((i==1)and(j==4)):#Home-team
                    game.hometeam = k.value
                if ((i==1)and(j==5)):#Guest-team
                    game.guestteam = k.value

            elif ((section == HOME_TEAM_SECTION)or(section == GUEST_TEAM_SECTION)):
                if (j==1):#a player's number
                    if (k.value==None):#an empty cell
                        isHometeamLineup = 0
                        break
                    elif (k.value!=None):
                        pnumber = k.value
                elif (j==2):#a player's name
                    if (k.value==None):#an empty cell
                        isHometeamLineup = 0
                        break
                    elif (k.value!=None):
                        pname = k.value
                elif (j==3):#a player's position
                    if (k.value==None):#an empty cell
                        isHometeamLineup = 0
                        break
                    elif (k.value!=None):
                        pposition = k.value
                        #we can create a player
                        p = Player(pnumber, pname, pposition)
                        if (section == HOME_TEAM_SECTION):
                            game.hometeamPlayers.append(p)
                        else:
                            game.guestteamPlayers.append(p)


            elif ((section==FIRST_PERIOD_SECTION)or(section==SECOND_PERIOD_SECTION)or(section==THIRD_PERIOD_SECTION)or(section==OVERTIME_SECTION)or(section==SHOOTOUT_SECTION)):
                if (j==0):
                    pplay = k.value
                    newPlay=1
                elif ((j==1)and(newPlay==1)):
                    pmin = k.value
                elif ((j==2)and(newPlay==1)):
                        peventAction = k.value
                elif ((j==3)and(newPlay==1)):
                    pteam = k.value
                elif ((j==4)and(newPlay==1)):
                    pactor = k.value
                elif ((j==5)and(newPlay==1)):
                    pfromLoc = k.value
                elif ((j==6)and(newPlay==1)):
                    ptoLoc = k.value
                elif ((j==7)and(newPlay==1)):
                    pactor2 = k.value
                elif ((j==8)and(newPlay==1)):
                    pactor3 = k.value
                elif ((j==9)and(newPlay==1)):
                    poutcome = k.value
                
                    p = Play(section-2, pplay, pmin, peventAction, pteam, pactor, pfromLoc, ptoLoc, pactor2, pactor3, poutcome)
                    game.plays.append(p)
                    newPlay=0

            elif (section==FINALSCORE_SECTION):
                if (j==0):
                    currentTeam=k.value
                elif (j==1):
                    if (currentTeam==game.hometeam):
                        game.hometeamFinalScore=k.value
                    elif (currentTeam==game.guestteam):
                        game.guestteamFinalScore=k.value


            j+=1;
        j=0;
        i+=1;
    return game

# download wav file of a required text
def textToSpeech(text, speaker, key):
    
    format= 'wav'
    lang = 'ru‑RU'

    user_agent ='Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'


    results = requests.get("https://tts.voicetech.yandex.net/generate",
                           params={'text': text, 'format': format, 'lang': lang, 'speaker': speaker, 'key': key},
                           headers={'User-Agent': user_agent})
   
    return results.content

# write an audio file to a disk
def textToSpeechFlush(file):
    fname=file
    #delete an old file
    try:
        os.remove(fname)
    except OSError:
        pass


    file = open(fname, 'wb')
    file.write(preparedAudio)
    file.close()

# write a text report to a disk
def textToFile(text, file):
    fname=file
    #delete an old file
    try:
        os.remove(fname)
    except OSError:
        pass
           
           
    file = open(fname, 'wt')
    file.write(text)
    file.close()

# for reporting a play
def step(p):
    s=''
    if (p.actor!=None):
        if (p.actor!='defender'):
            s+=game.getPlayerName(p.team, p.actor).encode('utf-8')+' из команды '+p.team.encode('utf-8')
        else:
            s+='Защитник из команды '+p.team.encode('utf-8')
        
        if (p.outcome!=None):
            if (p.outcome=='yes'):
                s+=' успешно'
            elif (p.outcome=='no'):
                s+=' безрезультатно'
            elif (p.outcome=='no score'):
                s+=' незасчитанно'
            elif (p.outcome=='miss'):
                s+=' пропустив'
            elif (p.outcome=='hit-goalee'):
                s+=' hit-goalee'
            elif (p.outcome=='scored'):
                s+=' засчитано'
            elif (p.outcome=='blocked'):
                s+=' поставив блок'
            elif (p.outcome=='caught'):
                s+=' поймав'
        s+= ' выполнил '+p.eventAction.encode('utf-8')
    # there is no any actor
    elif (p.actor==None):
        s+='Команда '+p.team.encode('utf-8')
        if (p.outcome!=None):
            if (p.outcome=='yes'):
                s+=' успешно'
            elif (p.outcome=='no'):
                s+=' безрезультатно'
            elif (p.outcome=='no score'):
                s+=' незасчитанно'
            elif (p.outcome=='miss'):
                s+=' пропустив'
            elif (p.outcome=='hit-goalee'):
                s+=' hit-goalee'
            elif (p.outcome=='scored'):
                s+=' засчитано'
            elif (p.outcome=='blocked'):
                s+=' поставив блок'
            elif (p.outcome=='caught'):
                s+=' поймав'
        s+= ' выполнила '+p.eventAction.encode('utf-8')
    if (p.fromLoc!=None):
        s+=' с локации '+p.fromLoc.encode('utf-8')
    if (p.toLoc!=None):
        s+=' в локацию '+p.toLoc.encode('utf-8')
    if (p.actor2!=None):
        s+=' задействуя игрока '+game.getPlayerName(p.team, p.actor2).encode('utf-8')
    if (p.actor3!=None):
        s+=' задействуя игрока '+game.getPlayerName(p.team, p.actor3).encode('utf-8')
    s+='. '
        
    return s



# --- Begin our code ---
currentPeriod =0
preparedAudio=''
game=readGameReportFromExcelFile(filename, sheetname)

# introduction
outputSpeech='Всем привет! И сегодня мы расскажем вам о матче между '+game.hometeam.encode('utf-8')+' и '+game.guestteam.encode('utf-8')+', который прошел '+str(game.date)+' на стадионе '+game.arena.encode('utf-8')+' в городе '+game.city.encode('utf-8')+'. На этот матч пришло '+str(game.attendance)+' человек, что довольно круто. '
outputFile = outputSpeech+'\r\n'
outputSpeech+='Сразу скажем, что итоговой счет игры '+str(game.hometeamFinalScore)+ ' на '+str(game.guestteamFinalScore)+'. Игра состояла из 3 периодов, овертайма и shootout. И сейчас мы вам расскажем, как проходила игра. '
outputFile = outputSpeech+'\r\n'

# create the first audio part
preparedAudio+= textToSpeech(outputSpeech,speaker, key)
# clear audio text
outputSpeech=''

# preparation
count={}
for x in range(0, len(game.plays)):
    if (game.plays[x].play!=None):
        p = game.plays[x].play
        if p in count:
            count[p]+=1
        else:
            count[p]=1

# create a detailed report
for x in count:
    # get all plays with a required play id
    g = game.getPlaysbyPlayValue(x)
    s=''
    #check for new period
    if (g[0].period>currentPeriod):
        currentPeriod = g[0].period
        if (currentPeriod<4):
            s +='                   ПЕРИОД '+str(currentPeriod)+'.          '
        else:
            s +='                     ОВЕРТАЙМ                    '
    # overall data
    s+='На минуте '+str(g[0].min)+' произошло событий: '+str(count[x])+ '. '

    # this is the main part
    for p in g:
        s+=step(p)
    # end of the main part

    outputSpeech+=s
    outputFile+=s+' \r\n'
    if (len(outputSpeech)>2000):
        preparedAudio+= textToSpeech(outputSpeech,speaker, key)
        outputSpeech=''

s = 'Shootout. '
outputSpeech+=s
outputFile+=s+' \r\n'

for x in game.plays:
    if ((x.play==None)and(x.min==None)): # Shootout
        s=''
        s+=step(x)
        outputSpeech+=s
        outputFile+=s+' \r\n'

        if (len(outputSpeech)>2000):
            preparedAudio+= textToSpeech(outputSpeech,speaker, key)
            outputSpeech=''



# --- Saving ---

# save the audio file
textToSpeechFlush('output.wav')
# save the text file
textToFile(outputFile, 'output.txt')