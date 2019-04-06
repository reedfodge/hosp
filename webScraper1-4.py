import requests
import urllib
import time
import mysql.connector
import sys
from lxml.html import fromstring
from itertools import cycle
import traceback
from bs4 import BeautifulSoup
from torrequest import TorRequest

def printLogo():
    print(" ___  ___  ________  ________  ________        ________  ________  ________  ________  ________  _______   ________     ")
    print("|\  \|\  \|\   __  \|\   ____\|\   __  \      |\   ____\|\   ____\|\   __  \|\   __  \|\   __  \|\  ___ \ |\   __  \    ")
    print("\ \  \\\  \ \  \|\  \ \  \___|\ \  \|\  \     \ \  \___|\ \  \___|\ \  \|\  \ \  \|\  \ \  \|\  \ \   __/|\ \  \|\  \   ")
    print(" \ \   __  \ \  \\\  \ \_____  \ \   ____\     \ \_____  \ \  \    \ \   _  _\ \   __  \ \   ____\ \  \_|/_\ \   _  _\  ")
    print("  \ \  \ \  \ \  \\\  \|____|\  \ \  \___|      \|____|\  \ \  \____\ \  \\  \\ \  \ \  \ \  \___|\ \  \_|\ \ \  \\  \| ")
    print("   \ \__\ \__\ \_______\____\_\  \ \__\           ____\_\  \ \_______\ \__\\ _\\ \__\ \__\ \__\    \ \_______\ \__\\ _\ ")
    print("    \|__|\|__|\|_______|\_________\|__|          |\_________\|_______|\|__|\|__|\|__|\|__|\|__|     \|_______|\|__|\|__|")
    print("                       \|_________|              \|_________|                                                           ")
    print("                                                                                                                        ")
    print("                                                                                                                        ")
    print("                                                                                                                        ")
    print("                                                   Created By                                                           ")
    print("                                                   Reed Fodge                                                           ")
    print("                                                                                                                        ")
    print("========================================================================================================================")
    print("========================================================================================================================")
    print("                                                                                                                        ")
    print("                                                                                                                        ")


printLogo()

proxies = {"134.209.45.249:8080", "134.209.41.247:8080", "104.248.51.135:8080", "159.65.164.58:80", "134.209.41.247:3128", "134.209.123.111:3128", "134.209.66.166:8080"}
proxy_pool = cycle(proxies)

proxyA = {
  "http": "178.128.0.209:8080",
  "https": "178.128.0.209:8080"
}

#Connects to MySQL Database
mydb = mysql.connector.connect(
    host="hosp.ctt1wmriltj5.us-east-2.rds.amazonaws.com",
    user="rfodge",
    passwd="Yy6bxM-G",
    database="hosp"
)

tr = TorRequest(password='Yy6bxM-G')

#Fetches all of the websites from database
mycursor = mydb.cursor()
mycursor.execute("SELECT WEBSITE FROM hospitalList")
myresult = mycursor.fetchall()

websiteList = []

#Adds all the websites to a list
for x in myresult:
    websiteList.append(str(x))

#Formats the websites
websiteList = [e[3:len(e)-3] for e in websiteList]

#Header to reduce spam detection
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

suffix = {".pdf", ".xls", ".xslx", ".csv", ".xml"}

def findDocs(response):
    print("DOC LIST CALLED")
    documentList = []
    soup = BeautifulSoup(response.text, "html.parser")
    aTags = soup.findAll('a', href=True)
    for j in aTags:
        s = str(j)
        for x in suffix:
            if s.endsWith(x):
                documentList.append(j)
    return documentList

def getSubPages(response):
    print("SUB PAGES CALLED")
    subList = []
    soup = BeautifulSoup(response.text, "html.parser")
    aTags = soup.findAll('a', href=True)
    for x in aTags:
        try:
            st = str(x['href'])
        except UnicodeEncodeError:
            print("UnicodeEncodeError")
        if st[0:1] == "/":
            subList.append(st)
    return subList

APIRequests = 1

def checkRequests():
    if APIRequests > 998:
        sys.exit()

for i in websiteList:
    for o in range(0, 32):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
    printLogo()
    proxy = next(proxy_pool)
    response1 = requests.get(i)
    print("CONNECTED TO URL")
    checkRequests()
    APIRequests += 1
    dL = []
    sL = []
    sL1 = getSubPages(webPage)
    print("SubList 1 Complete")
    sL2 = []
    sL3 = []
    sL4 = []
    sL5 = []
    sL6 = []
    time.sleep(5)
    for a in sL1:
        proxy = next(proxy_pool)
        urlA = str(i) + str(a)
        try:
            checkRequests()
            responseA = requests.get(urlA, headers=headers, proxies=proxyA)
            APIRequests += 1
            time.sleep(2)
        except:
            print("Connection Error")
        sLA = getSubPages(responseA)
        sL2.extend(sLA)
    print("SubList 2 Complete")
    time.sleep(5)
    for b in sL2:
        proxy = next(proxy_pool)
        urlB = str(i) + str(b)
        try:
            checkRequests()
            responseB = requests.get(urlB, headers=headers, proxies=proxyA)
            APIRequests += 1
            time.sleep(2)
        except:
            print("Connection Error")
        sLB = getSubPages(responseB)
        sL3.extend(sLB)
    print("SubList 3 Complete")
    time.sleep(5)
    for c in sL3:
        proxy = next(proxy_pool)
        urlC = str(i) + str(c)
        try:
            checkRequests()
            responseC = requests.get(urlC, headers=headers, proxies=proxyA)
            APIRequests += 1
            time.sleep(2)
        except:
            print("Connection Error")
        sLA = getSubPages(responseC)
        sL4.extend(sLC)
    print("SubList 4 Complete")
    time.sleep(5)
    for d in sL4:
        proxy = next(proxy_pool)
        urlD = str(i) + str(d)
        try:
            checkRequests()
            responseD = requests.get(urlD, headers=headers, proxies=proxyA)
            APIRequests += 1
            time.sleep(2)
        except:
            print("Connection Error")
        sLD = getSubPages(responseD)
        sL5.extend(sLD)
    print("SubList 5 Complete")
    time.sleep(5)
    for e in sL5:
        proxy = next(proxy_pool)
        urlE = str(i) + str(e)
        try:
            checkRequests()
            responseE = requests.get(urlE, headers=headers, proxies=proxyA)
            APIRequests += 1
            time.sleep(2)
        except:
            print("Connection Error")
        sLE = getSubPages(responseE)
        sL6.extend(sLE)
    print("SubList 6 Complete")
    time.sleep(5)
    sL.extend(sL1)
    sL.extend(sL2)
    sL.extend(sL3)
    sL.extend(sL4)
    sL.extend(sL5)
    sL.extend(sL6)
    dL1 = findDocs(sL)
    dL.extend(dL1)
    for k in dL:
        print(k)
