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

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getGolfLeaderBoard():
    pass

def getAvgDrivingDistance():
    
    pass

def getAvgGreensInReg():
    pass

def getStrokesGainedOffTee():
    pass

def getScrablingPct():
    pass

def getStrokesGainedPutting():
    pass














print("python")