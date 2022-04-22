'''
FINAL PROJECT:

Golfing Brothers

Harrison Barth
Kagan Shetterly

SI 206

April 26, 2022

Golf Leaderboard API:
https://rapidapi.com/sportcontentapi/api/golf-leaderboard-data

PGA Tour player statistics:
https://www.pgatour.com/stats.html

'''

import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
#from asyncore import write
#from xml.sax import parseString
from bs4 import BeautifulSoup
import requests
import csv
import unittest
import json

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getGolfLeaderboard(cur, conn):
    '''
    resp = requests.get("https://golf-leaderboard-data.p.rapidapi.com/tour-rankings/2/2021")

    f = json.dumps(resp.text)

    #f = json.loads(resp)
    print(f)
    
    url = "https://golf-leaderboard-data.p.rapidapi.com/tour-rankings/2/2021"


    p = {"season" : 2022, "tour_id" : 2}

    response = requests.get(url, params = p)

    #print(response.status_code)

    #f = json.dumps(response.text, )
    #print(response.json())
    f = response.json()

    for p in f["results"]["rankings"]:
        print(p["player_name"])
    '''


    #url = "https://sportsdata.io/developers/api-documentation/golf#/endpoint/leaderboard"

    my_headers = {"user" : "whdsports@gmail.com", "Ocp-Apim-Subscription-Key" : "{11e7472d48c5426395b330fc36795ae6}"}

    #response = requests.get("https://api.sportsdata.io/golf/v2/json/PlayerSeasonStats/2022", headers = my_headers)
    p = {"api_key" : "11e7472d48c5426395b330fc36795ae6"}

    #Ocp-Apim-Subscription-Key: {key}

    response = requests.get("https://feeds.datagolf.com/preds/get-dg-rankings?file_format=[ file_format ]&key=1e5bb95e483606573a01c8292f84")

    #print(response.text)

    text = json.loads(response.text)


    cur.execute('''
    DROP TABLE IF EXISTS Leaderboard
    ''')

    cur.execute('''
    CREATE TABLE Leaderboard (name TEXT, rank REAL)
    ''')

    for r in text["rankings"]:
        rank = int(r["owgr_rank"])
        name1 = r["player_name"]

        name2 = name1.split(",")

        real_name = name2[-1] + " " + name2[0]

        real_name1 = real_name.strip()

        #print(real_name)
        #print(rank)

        cur.execute('''
            INSERT INTO Leaderboard (name, rank)
            VALUES (?, ?)
            ''', (real_name1, rank))

    conn.commit()






def getAvgDrivingDistance(cur, conn):
    site = requests.get("https://www.pgatour.com/stats.html")

    f = site.text

    soup = BeautifulSoup(f, "html.parser")

    
    tableSeeAll = soup.find_all("a", class_ = "see-all")
    
    seeAllLink = tableSeeAll[3]["href"]

    link = "https://www.pgatour.com/" + str(seeAllLink)
    opened = requests.get(link)

    soup2 = BeautifulSoup(opened.text, "html.parser")

    drivingTable = soup2.find("table", class_ = "table-styled")

    rows = drivingTable.find_all("tr")   

    drivingDict = {}

    cur.execute('''
    DROP TABLE IF EXISTS Driving
    ''')

    cur.execute('''
    CREATE TABLE Driving (name TEXT, distance REAL)
    ''')



    for row in rows:
        
        player_name = row.find("td", class_ = "player-name")

        #playerName = player_name.find("a").string
        '''
        if (type(player_name) != None):
            playerName = player_name.find("a")

            print(playerName)
        '''
        name1 = ""
        drivingDistance = 0
   
        #print(player_name)
        if player_name != None:
            name = player_name.find("a")
            #print(name.string)
            name1 = str(name.string)
        

        driving_distance = row.find_all("td")

        if driving_distance != None:
            if len(driving_distance) > 5:
                #print(driving_distance[4].string)
                drivingDistance = float(driving_distance[4].string)
        

        
        if drivingDistance != 0 and name1 != "":
            
            cur.execute('''
            INSERT INTO Driving (name, distance)
            VALUES (?, ?)
            ''', (name1, drivingDistance))
            print(name1)
            print(drivingDistance)
    conn.commit()
            

def getGreensInRegPct(cur, conn):
    site = requests.get("https://www.pgatour.com/stats.html")

    f = site.text

    soup = BeautifulSoup(f, "html.parser")

    
    tableSeeAll = soup.find_all("a", class_ = "see-all")
    
    seeAllLink = tableSeeAll[5]["href"]

    link = "https://www.pgatour.com/" + str(seeAllLink)
    opened = requests.get(link)

    soup2 = BeautifulSoup(opened.text, "html.parser")

    greensPctTable = soup2.find("table", class_ = "table-styled")
    #print(greeensPctTable)


    rows = greensPctTable.find_all("tr")   

    

    cur.execute('''
    DROP TABLE IF EXISTS GreensInReg
    ''')

    cur.execute('''
    CREATE TABLE GreensInReg (name TEXT, percentage REAL)
    ''')



    for row in rows:
        
        player_name = row.find("td", class_ = "player-name")

        #playerName = player_name.find("a").string
        '''
        if (type(player_name) != None):
            playerName = player_name.find("a")

            print(playerName)
        '''
        name1 = ""
        greensReg = 0
   
        #print(player_name)
        if player_name != None:
            name = player_name.find("a")
            #print(name.string)
            name1 = str(name.string)
            print(name1)

        greens_reg = row.find_all("td")

        if greens_reg != None:
            if len(greens_reg) > 5:
                #print(driving_distance[4].string)
                greensReg = float(greens_reg[4].string)
        

        
        if greensReg != 0 and name1 != "":
            
            cur.execute('''
            INSERT INTO GreensInReg (name, percentage)
            VALUES (?, ?)
            ''', (name1, greensReg))
            print(name1)
            print(greensReg)
    conn.commit()
 

def getStrokesGainedTeeToGreen(cur, conn):
    site = requests.get("https://www.pgatour.com/stats.html")

    f = site.text

    soup = BeautifulSoup(f, "html.parser")

    
    tableSeeAll = soup.find_all("a", class_ = "see-all")
    
    seeAllLink = tableSeeAll[6]["href"]

    link = "https://www.pgatour.com/" + str(seeAllLink)
    opened = requests.get(link)

    soup2 = BeautifulSoup(opened.text, "html.parser")

    greensPctTable = soup2.find("table", class_ = "table-styled")
    #print(greeensPctTable)


    rows = greensPctTable.find_all("tr")   

    

    cur.execute('''
    DROP TABLE IF EXISTS StrokesGainedTeeToGreen
    ''')

    cur.execute('''
    CREATE TABLE StrokesGainedTeeToGreen(name TEXT, strokes REAL)
    ''')


    for row in rows:
        
        player_name = row.find("td", class_ = "player-name")

        #playerName = player_name.find("a").string
        '''
        if (type(player_name) != None):
        playerName = player_name.find("a")

        print(playerName)
        '''
        name1 = ""
        greensReg = 0
   
        #print(player_name)
        if player_name != None:
            name = player_name.find("a")
            #print(name.string)
            name1 = str(name.string)
            print(name1)

        greens_reg = row.find_all("td")

        if greens_reg != None:
            if len(greens_reg) > 5:
                #print(driving_distance[4].string)
                greensReg = float(greens_reg[4].string)
        

        
        if greensReg != 0 and name1 != "":

            
            
            cur.execute('''
            INSERT INTO StrokesGainedTeeToGreen (name, strokes)
            VALUES (?, ?)
            ''', (name1, greensReg))
            print(name1)
            print(greensReg)
    conn.commit()

def getScramblingPct(cur, conn):
    site = requests.get("https://www.pgatour.com/stats.html")

    f = site.text

    soup = BeautifulSoup(f, "html.parser")

    
    tableSeeAll = soup.find_all("a", class_ = "see-all")
    
    seeAllLink = tableSeeAll[9]["href"]

    link = "https://www.pgatour.com/" + str(seeAllLink)
    opened = requests.get(link)

    soup2 = BeautifulSoup(opened.text, "html.parser")

    greensPctTable = soup2.find("table", class_ = "table-styled")
    #print(greeensPctTable)


    rows = greensPctTable.find_all("tr")   

    

    cur.execute('''
    DROP TABLE IF EXISTS ScramblingPercentage
    ''')

    cur.execute('''
    CREATE TABLE ScramblingPercentage(name TEXT, percentage REAL)
    ''')


    for row in rows:
        
        player_name = row.find("td", class_ = "player-name")

        #playerName = player_name.find("a").string
        '''
        if (type(player_name) != None):
        playerName = player_name.find("a")

        print(playerName)
        '''
        name1 = ""
        greensReg = 0
   
        #print(player_name)
        if player_name != None:
            name = player_name.find("a")
            #print(name.string)
            name1 = str(name.string)
            print(name1)

        greens_reg = row.find_all("td")

        if greens_reg != None:
            if len(greens_reg) > 5:
                #print(driving_distance[4].string)
                greensReg = float(greens_reg[4].string)
        

        
        if greensReg != 0 and name1 != "":

            cur.execute('''
            INSERT INTO ScramblingPercentage (name, percentage)
            VALUES (?, ?)
            ''', (name1, greensReg))
            print(name1)
            print(greensReg)
    conn.commit()


def getStrokesGainedPutting(cur, conn):

    site = requests.get("https://www.pgatour.com/stats.html")

    f = site.text

    soup = BeautifulSoup(f, "html.parser")

    
    tableSeeAll = soup.find_all("a", class_ = "see-all")
    
    seeAllLink = tableSeeAll[8]["href"]

    link = "https://www.pgatour.com/" + str(seeAllLink)
    opened = requests.get(link)

    soup2 = BeautifulSoup(opened.text, "html.parser")

    greensPctTable = soup2.find("table", class_ = "table-styled")
    #print(greeensPctTable)


    rows = greensPctTable.find_all("tr")   

    

    cur.execute('''
    DROP TABLE IF EXISTS StrokesGainedPutting
    ''')

    cur.execute('''
    CREATE TABLE StrokesGainedPutting(name TEXT, strokes REAL)
    ''')


    for row in rows:
        
        player_name = row.find("td", class_ = "player-name")

        #playerName = player_name.find("a").string
        '''
        if (type(player_name) != None):
        playerName = player_name.find("a")

        print(playerName)
        '''
        name1 = ""
        greensReg = 0
   
        #print(player_name)
        if player_name != None:
            name = player_name.find("a")
            #print(name.string)
            name1 = str(name.string)
            print(name1)

        greens_reg = row.find_all("td")

        if greens_reg != None:
            if len(greens_reg) > 5:
                #print(driving_distance[4].string)
                greensReg = float(greens_reg[4].string)
        

        
        if greensReg != 0 and name1 != "":

            cur.execute('''
            INSERT INTO StrokesGainedPutting (name, strokes)
            VALUES (?, ?)
            ''', (name1, greensReg))
            print(name1)
            print(greensReg)
    conn.commit()

def drivingScatterPlot(cur, conn):

    drivingDict = {}

    cur.execute('''
    SELECT rank, distance
    FROM Leaderboard
    JOIN Driving
    ON Driving.name = Leaderboard.name
    ORDER BY Leaderboard.rank
    ''')
    

    for row in cur:
        print(row)




def main():
    dbname = "GolfingBrothers.db"
    cur, conn = setUpDatabase(dbname)

    #getGreensInRegPct(cur, conn)
    #getGolfLeaderBoard()
    #getStrokesGainedTeeToGreen(cur, conn)
    #getScramblingPct(cur, conn)
    #getStrokesGainedPutting(cur, conn)


    #getGolfLeaderboard(cur, conn)
    drivingScatterPlot(cur, conn)





main()







