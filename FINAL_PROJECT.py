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

def getGolfLeaderBoard():
    '''
    resp = requests.get("https://golf-leaderboard-data.p.rapidapi.com/tour-rankings/2/2021")

    f = json.dumps(resp.text)

    #f = json.loads(resp)
    print(f)
    '''
    url = "https://golf-leaderboard-data.p.rapidapi.com/tour-rankings/2/2021"

    h = {
	    "X-RapidAPI-Host": "golf-leaderboard-data.p.rapidapi.com",
	    "X-RapidAPI-Key": "4489a2a0a6msh1f08319ed99a586p1aaacbjsn26fef02ad77b"
    }

    p = {"season" : 2022, "tour_id" : 2}

    response = requests.get(url, headers = h, params = p)

    #print(response.status_code)

    #f = json.dumps(response.text, )
    #print(response.json())
    f = response.json()

    for p in f["results"]["rankings"]:
        print(p["player_name"])
    
  

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


def getStrokesGainedPutting():


    pass



def main():
    dbname = "GolfingBrothers.db"
    cur, conn = setUpDatabase(dbname)

    #getGreensInRegPct(cur, conn)
    #getGolfLeaderBoard()
    #getStrokesGainedTeeToGreen(cur, conn)
    getScramblingPct(cur, conn)


    #getAvgDrivingDistance(cur, conn)





main()







