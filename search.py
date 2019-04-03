from googlesearch import search
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
XLSresultsList = []
XLSXresultsList = []
XMLresultsList = []

for y in websiteList:
    print('------')
    PDFquery = "site:" + y + " filetype:pdf"
    CSVquery = "site:" + y + " filetype:csv"
    XLSquery = "site:" + y + " filetype:xls"
    XLSXquery = "site:" + y + " filetype:xlsx"
    XMLquery = "site:" + y + " filetype:xml"
    for a in search(PDFquery, tld="co.in", num=10, stop=1, pause=2) :
        print(a)
    for b in search(CSVquery, tld="co.in", num=10, stop=1, pause=2) :
        print(b)
    for c in search(XLSquery, tld="co.in", num=10, stop=1, pause=2) :
        print(c)
    for d in search(XLSXquery, tld="co.in", num=10, stop=1, pause=2) :
        print(d)
    for e in search(XMLquery, tld="co.in", num=10, stop=1, pause=2) :
        print(e)
