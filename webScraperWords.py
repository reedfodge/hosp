import requests
import urllib
import time
import mysql.connector
import sys
from bs4 import BeautifulSoup

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

#Connects to MySQL Database
mydb = mysql.connector.connect(
    host="hosp.ctt1wmriltj5.us-east-2.rds.amazonaws.com",
    user="rfodge",
    passwd="Yy6bxM-G",
    database="hosp"
)

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

#List of unique words
wordList = []
#List of unique words with their corresonding frequency
formattedWordList = []

#Possible bounds for words in a href
boundsList = ["/", "-", "_", "."]

#Creates an object that stores a word and a frequency
class wordWithIndex:
    def __init__(self, word):
        self.word = word
        self.frequency = 2

#Partition section of Quick Sort
def partition(low, high):
    i = (low-1)
    pivot = formattedWordList[high].frequency
    for j in range(low, high):
        if formattedWordList[j].frequency <= pivot:
            i = i+1
            formattedWordList[i],formattedWordList[j] = formattedWordList[j],formattedWordList[i]
    formattedWordList[i+1],formattedWordList[high] = formattedWordList[high],formattedWordList[i+1]
    return (i+1)

#Sorts formattedWordList with a Quick Sort
def sortFWL(low, high):
    if low < high:
        pi = partition(low, high)
        sortFWL(low, pi-1)
        sortFWL(pi+1, high)

#Analyzes the href
def analyzeWords(s, startBound):
    indexOfUpperBound = 10000000
    numBoundsChecked = 0
    for a in boundsList:
        #Checks to find the next index of every type of bound
        indexOfBound = s.find(a, startBound)
        #Breaks the loop if every bound has been checked for and
        #none were found, to tell the loop its reached the end
        if numBoundsChecked == 4:
            break
        elif indexOfBound != -1:
            numBoundsChecked += 1
            #If the specified type of bound is found and it is closer in
            #the href, it sets the upper bound of the word to the index
            #of that specified bound
            if indexOfBound < indexOfUpperBound:
                indexOfUpperBound = indexOfBound
            word = str(s[startBound:indexOfUpperBound])
            #Checks to see if the found word is unique
            if word not in wordList:
                wordList.append(word)
            else:
                #If the word is not unique, a new wWI object is created
                #with a frequency of 2 (the first appearence of the words
                #plus the current appearence) if it does not already exixt
                #in the formattedWordList. If it does, the frequency of
                #that word is incremented by 1
                formattedWord = wordWithIndex(word)
                inList = False;
                for x in formattedWordList:
                    if x.word == formattedWord.word:
                        x.frequency += 1
                        inList = True
                if inList == False:
                    formattedWordList.append(formattedWord)
        else:
            numBoundsChecked += 1
    if numBoundsChecked != 4:
        analyzeWords(s, indexOfUpperBound)

numURLSvisited = 0
numURLSrejected = 0

for i in websiteList:
    try:
        if numURLSrejected < 6:
            resposne = requests.get(i, headers=headers)
            numURLSvisited += 1
            soup = BeautifulSoup(response.text, "html.parser")
            aTags = soup.findAll('a', href=True)
            for j in aTags:
                try:
                    st = str(j['href'])
                except UnicodeEncodeError:
                    print("UNICODE ENCODE ERROR")
                if st[0:1] == "/":
                    analyzeWords(st, 1)
            numElements = len(formattedWordList)-1
            try:
                sortFWL(0, numElements)
            except RuntimeError:
                print("ERROR SORTING")
            for o in range(0, 32):
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
            printLogo()
            p = (float(numURLSvisited/len(websiteList))) * 100
            print("Percent Complete: " + str(p) + "% (" + str(numURLSvisited) + " / " + str(len(websiteList)) + ")")
            print("Unique Words: " + str(numElements+1))
            if len(formattedWordList) > 10:
                for x in range(numElements-10, numElements):
                    print(str(formattedWordList[x].word), ": " + str(formattedWordList[x].frequency))
            else:
                for a in formattedWordList:
                    print(str(a.word) + ": " + str(a.frequency))
            print("=====================")
        else:
            time.sleep(10)
            break
    except:
        print("CONNECTION ERROR")
        numURLSrejected += 1

for j in websiteList:
    try:
        if numURLS
