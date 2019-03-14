from google import google
import mysql.connector

mydb = mysql.connector.connect(
    host="hosp.ctt1wmriltj5.us-east-2.rds.amazonaws.com",
    user="rfodge",
    passwd="Yy6bxM-G",
    database="hosp"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT WEBSITE FROM hospitalList")
myresult = mycursor.fetchall()

websiteList = []

for x in myresult:
    websiteList.append(str(x))

websiteList = [e[3:len(e)-3] for e in websiteList]
PDFresultsList = []
CSVresultsList = []
XLsresultsList = []
XLSXresultsList = []

for y in websiteList:
    PDFsearch_results = ("site:" + y + " filetype:pdf")
    CSVsearch_results = ("site:" + y + " filetype:csv")
    XLSsearch_results = ("site:" + y + " filetype:xls")
    XLSXsearch_results = ("site:" + y + " filetype:xlsx")
    for url in search(PDFsearch_results):
        PDFresultsList.append(url)
    for url in search(CSVsearch_results):
        CSVresultsList.append(url)
    for url in search(XLSsearch_results):
        XLsresultsList.append(url)
    for url in search(XLSXsearch_results):
        XLSXresultsList.append(url)

for z in PDFresultsList:
    print(z)
