import requests
import urllib
import time
import mysql.connector
from bs4 import BeautifulSoup

#Connect to MySQL Database
mydb = mysql.connector.connect(
    host="hosp.ctt1wmriltj5.us-east-2.rds.amazonaws.com",
    user="rfodge",
    passwd="Yy6bxM-G",
    database="hosp"
)

#Gets all websites from database
mycursor = mydb.cursor()
mycursor.execute("SELECT WEBSITE FROM hospitalList")
myresult = mycursor.fetchall()

websiteList = []

#Puts all the websites casted to a string in an array
for x in myresult:
    websiteList.append(str(x))

#Formats the websites
websiteList = [e[3:len(e)-3] for e in websiteList]

#Primary keyword check
def checkString(href):
    if "financ" in href:
        return True
    elif "bill" in href:
        return True
    elif "charge" in href:
        return True
    elif "pay" in href:
        return True
    elif "pric" in href:
        return True

#Secondary keyword check
def checkString2(href):
    if "pricing-transparency" in href:
        return True
    elif "pricing_transparency" in href:
        return True
    elif "chargemaster" in href:
        return True
    elif "charge-master" in href:
        return True
    elif "charge_master" in href:
        return True
    elif "price-list" in href:
        return True
    elif "price_list" in href:
        return True
    elif "billing-information" in href:
        return True
    elif "billing_information" in href:
        return True
    elif "pricing-information" in href:
        return True
    elif "pricing_information" in href:
        return True
    elif "estimat" in href:
        return True
    elif "pricing-faq" in href:
        return True
    elif "pricing_faq" in href:
        return True

#Headers for scraper to reduce bot detection
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

#Retrieves all <a> tags with an href in the HTML
def getTags(url):
    try:
        response = requests.get(url, headers=headers)
    except UnicodeEncodeError:
        print("FAILURE TO CONNECT TO URL")
    soup = BeautifulSoup(response.text, "html.parser")
    aTags = soup.findAll('a', href=True)
    time.sleep(1)
    return aTags

#Number of URLs containing keywords (For analytics)
numPrinted = 0;
#Total number of URLs parsed (For analytics)
numURLS = 0;

for y in websiteList:
    #Increases number of URLs parsed
    numURLS += 1
    #Intializes list of already printed hrefs to avoid repeated hrefs
    printedList = [0] * 10
    url = y
    #Retrieves all
    aTags = getTags(url)
    for z in aTags:
        try:
            st = str(z['href'])
        except UnicodeEncodeError:
            print("UNICODE ENCODE ERROR (FIX THIS AT SOME POINT)")
        if st[0:1] == '/' and checkString(st):
            if checkString2(st):
                if not st in printedList:
                    print(st)
                    numPrinted += 1
                    printedList.append(st)
            url2 = y + st
            aTags2 = getTags(url2)
            for a in aTags2:
                try:
                    st2 = str(a['href'])
                except UnicodeEncodeError:
                    print("UNICODE ENCODE ERROR (FIX THIS AT SOME POINT)")
                if st2[0:1] == '/' and checkString2(st2):
                    if not st2 in printedList:
                        numPrinted += 1
                        print(st2)
                        printedList.append(st2)
                    url3 = y + st2
                    aTags3 = getTags(url3)
                    for b in aTags3:
                        try:
                            st3 = str(b['href'])
                        except UnicodeEncodeError:
                            print("UNICODE ENCODE ERROR (FIX THIS AT SOME POINT)")
                        if st3[0:1] == '/':
                            print(st3)

    print("========== Printed: " + str(numPrinted) + " === Total: " + str(numURLS) + " === " + str((float(numPrinted)/float(numURLS))*100) + "% ==========")
