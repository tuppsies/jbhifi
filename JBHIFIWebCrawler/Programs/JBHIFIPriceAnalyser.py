# This program written by Joshua Cahill is just testing some features in interacting with the mysql database using Python

import sys
import logging
import requests
from bs4 import BeautifulSoup
import time
import datetime
from datetime import datetime
import mysql.connector


homeDirectory = "/home/tupperware/JBHIFIWebCrawler/Debug/PriceAnalyser/"

# set up text files
error = open("/home/tupperware/JBHIFIWebCrawler/Debug/PriceAnalyser/errorLog.txt", "w")
debug = open("/home/tupperware/JBHIFIWebCrawler/Debug/PriceAnalyser/debug.txt", "w")
inActiveProducts = open("/home/tupperware/JBHIFIWebCrawler/Debug/PriceAnalyser/inActive.txt", "a")

# set up the text file we are going to be reading from
urlTxtFile = str((sys.argv)[1])
print("Our text file is: " + urlTxtFile, file = debug)
urlFile = open(urlTxtFile, "r")

# set up the logging of the execution errors
logLocation = str((sys.argv)[1])
logLocation = logLocation.split("tmp/")[1]
logLocation = logLocation.split("tmp")[0]
logLocation = homeDirectory + "executionError" + logLocation + ".txt"
logging.basicConfig(level=logging.DEBUG, filename = logLocation)
print("logLocation complete...", file = debug)

# create a unique string that consists of an integer to identify each instance of a process
# TO DO
uniqueString = str((sys.argv)[1])
uniqueString = uniqueString.split("tmp/")[1]
uniqueString = uniqueString.split("tmp")[0]
uniqueString = "process" + uniqueString + ":"

# create the header for the URL request
requestHeaders = {
    'User-Agent': 'Project Web Crawler',
    'From': 'TupperwareC@hotmail.com'
}

def database_analyser():

    # set up the date
    # VERY IMPORTANT: date must be in this specific format as we use it to check for duplicates in the database
    date = str(time.strftime("%Y-%m-%d"))
    # print the date to the start of the file
    print(str(datetime.now()), file = debug)
    print(str(datetime.now()), file = error)
    print(str(datetime.now()), file = inActiveProducts)
    #print(str(datetime.now()), file = logLocation)
    
    # use this to store the total number of bytes of the webpages being analysed
    totalBytes = 0
    totalUnrecordedBytes = 0

    # get the total number of products that need to be analysed
    numPagesAnalysed = 0
    c.execute("SELECT COUNT(id) FROM products")
    numProducts = str(c.fetchone())
    numProducts = numProducts.split("(")[1]
    numProducts = numProducts.split(",")[0]
    numProducts = int(numProducts)

    # get each URL in the database and put it into a list
    c.execute("SELECT url FROM products")
    URLSArray = []
    for (url) in c:
        URLSArray.append(url)
    
    for url in urlFile:

        # prepare the url by parsing it nicely
        url = str(url)
        url = url.split("'")[1]
        url = url.split("'")[0]
        print(url, file = debug)

        # print the number of pages analysed
        # we do not do this at the moment since we run multiple processes
        #numPagesAnalysed = numPagesAnalysed + 1
        #print(" " + str(numPagesAnalysed) + " pages analysed, " + str(round(numPagesAnalysed/numProducts*100, 2)) + "% complete", end='\r')
       
        # attributes of the product
        isActive = 1
        numberReviews = 0
        overallRating = 0
        

        # make sure the record does not already exist
        c.execute("SELECT ID FROM products WHERE url = %s", (url,))
        checkProdID = str(c.fetchone())
        checkProdID = checkProdID.split("(")[1]
        checkProdID = checkProdID.split(",")[0]
        c.execute("SELECT COUNT(ID) FROM productPricing WHERE ID = %s AND date = %s", (checkProdID, date))
        num = str(c.fetchone())
        num = num.split("(")[1]
        num = num.split(",")[0]
        num = int(num)
        if num > 0:
            # an error has occured and we have double checked the price, log an error
            print("###Price is already in the table for today: " + url, file = debug)
            continue
        
        # get the size of the url in bytes
        res = requests.head(url)
        res = res.headers
        res = str(res)
        if "'Content-Length': '" not in res:
            totalUnrecordedBytes += 1
            print("NO BYTES INFORMATION FOUND", file = debug)      
        else:
            bytes = res.split("'Content-Length': '")[1]
            bytes = bytes.split("'")[0]
            print("Num bytes is " + str(bytes), file = debug)
            bytes = int(bytes)
            totalBytes += bytes
            print("Total bytes is now " + str(totalBytes), file = debug)        

        # prepare the page
        productSourceCode = requests.get(url, headers=requestHeaders)
        productPlainText = productSourceCode.text
        productSoup = BeautifulSoup(productPlainText, "html.parser")

        
        # give the server a rest
        time.sleep(0.1)

        
        # verify that the page is still active (e.g. that there is content on it)
        testProdID = productSoup.find('span', {'id':'prodID'})
        #testProdID = "2343"
        if(testProdID == None):
            # if we cannot locate a prodID then the page is no longer active and we put it in the database as non active
            c.execute("SELECT ID FROM products WHERE url = %s", (url,))
            testProdID = str(c.fetchone())
            testProdID = testProdID.split("(")[1]
            testProdID = testProdID.split(",")[0]
            price = 0
            isActive = 0
            c.execute("INSERT INTO productPricing VALUES(%s, %s, %s, %s, %s, %s)",(testProdID, date, price, overallRating, numberReviews, isActive))
            delimiter = ","
            print(date + delimiter + testProdID + delimiter + date + delimiter + url, file = inActiveProducts)
            print("inactive product: " + date + delimiter + testProdID + delimiter + date + delimiter + url, file = debug)
            continue



        # verify that we are on the correct product page checking the product id in the page against the product id in the database
        productPageID = (productSoup.find('span', {'id':'prodID'})).contents[0]
        c.execute("SELECT ID FROM products WHERE url = %s", (url,))
        productDatabaseID = str(c.fetchone())
        productDatabaseID = productDatabaseID.split("(")[1]
        productDatabaseID = productDatabaseID.split(",")[0]
        print("###productPageID: " + productPageID, file = debug)
        print("###productDatabaseID: " + productDatabaseID, file = debug)
        print(str(datetime.now()), file = debug)
        if(int(productPageID) != int(productDatabaseID)):
            # this is bad, log an error report and go to the next url
            print("###ID matching error...", file = debug)
            print("###ID's do not match on: " + url, file = error)
            print("productPageID is: " + productPageID)
            print("productDatabaseID is: " + productDatabaseID)
            continue   
        


        # get the price from the webpage
        price = (productSoup.find('meta', {'property':'price'})).get('content')
        price = float(price)


        # if it has a review get that as well
        ratingHTML = productSoup.find('span', {'class':'full-stars detail-page'})
        if(ratingHTML != None):
            overallRating = str(ratingHTML.get('style'))
            overallRating = overallRating.split(':')[1]
            overallRating = overallRating.split('%')[0]
            overallRating = float(overallRating)

            numberReviews = str(productSoup.find('span', {'class':'ratings-count detail-page'}))
            numberReviews = numberReviews.split('(')[1]
            numberReviews = numberReviews.split(')')[0]
            numberReviews = int(numberReviews)
            
            
        # print the data
        #delimiter = ","
        #print(productPageID + delimiter + date + delimiter + str(price) + delimiter + str(overallRating) + delimiter + str(numberReviews) + delimiter + str(isActive), file = debug)
        

        
        # insert into the database
        c.execute("INSERT INTO productPricing VALUES(%s, %s, %s, %s, %s, %s)",(str(productPageID), str(date), str(price), str(overallRating), str(numberReviews), str(isActive)))
        conn.commit()


    conn.commit()
    print("Total number of bytes analysed was " + str(totalBytes), file = debug)
    print("Total number of pages with no bytes information was " + str(totalUnrecordedBytes), file = debug)
    print(str(datetime.now()), file = debug)
    print(str(datetime.now()), file = error)
    print(str(datetime.now()), file = inActiveProducts)
    print("Program has completed", file = debug)
    
    # close the files and the database
    error.close()
    debug.close()
    inActiveProducts.close()
    


# connect to the mysql server
conn = mysql.connector.connect(user='jbhifi', password='aR5vx?25', host='tupperware.dirtydns.com', database='tupperware_jbhifi')
c = conn.cursor()

# try and run the program and if we get an error log it
try:
    database_analyser()
except:
    logging.exception("ERROR")    


# close the database connection
conn.close()
