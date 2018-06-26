# JB-HI-FI Web Crawler created by Joshua Cahill
# This web crawler navigates from the JB-HI-FI site map

import logging
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sys
import mysql.connector
# can get rid of this if mysql is working fine
import sqlite3

# SQL SETUP
conn = mysql.connector.connect(user='jbhifi', password='aR5vx?25', host='tupperware.dirtydns.com', database='tupperware_jbhifi')
c = conn.cursor()

# general variable setup
delayTime = 1
numPagesAnalysed = 0

# logging setup
logging.basicConfig(level=logging.DEBUG, filename = "/home/tupperware/JBHIFIWebCrawler/Debug/WebCrawler/pythonExecutionErrors.txt")

# setup the variable to store the bytes
totalBytes = 0
totalUnrecordedBytes = 0

# create the header for the URL request
requestHeaders = {
    'User-Agent': 'Project Web Crawler',
    'From': 'TupperwareC@hotmail.com'
}


def web_crawler():
    # setup text files
    global debug
    debug = open("/home/tupperware/JBHIFIWebCrawler/Debug/WebCrawler/debug.txt", "w")
    global newProducts
    newProducts = open("/home/tupperware/JBHIFIWebCrawler/Debug/WebCrawler/newProducts.txt", "a")

    # print dates and time to text files
    print(str(datetime.now()), file = debug)

    # get the site soup
    siteMapURL = 'https://www.jbhifi.com.au/General/Sitemap/'
    print("###Requesting site map access...", file = debug)
    siteMapSourceCode = requests.get(siteMapURL, headers=requestHeaders)
    siteMapPlainText = siteMapSourceCode.text
    siteMapSoup = BeautifulSoup(siteMapPlainText, "html.parser")
    print("###Site map accessed...", file = debug)

    # get the content screen
    contentScreen = siteMapSoup.find('div', {'class':'cms-content'})
    contentScreen = contentScreen.find('ul', recursive = False)
    print("#Content screen accessed...", file = debug)
    # for each section e.g. computers, cameras
    for categoryList in contentScreen.findAll('li', recursive = False):
        # get the title, e.g. computers, tv home entertainment
        global pageHeading
        pageHeading = categoryList.find('a').contents[0]
        pageHeading = comma_remove(pageHeading)
        print("###Page heading: " + pageHeading, file = debug)
        categoryList = categoryList.find('ul')

        # there is a list of different categories further broken down go to each of them
        for itemList in categoryList.findAll('li', recursive = False):

            for pageLinkURL in itemList.findAll('a'):
                pageTitle = pageLinkURL.contents[0]
                print("###Accessing page: " + pageTitle, file = debug)
                # we have reached the last product on the page terminate the program
                if(pageTitle == "JB HOME Stores"):
                    print("We have reached the end of scanning, ending program!", file = debug)
                    print(str(datetime.now()), file = debug)
                    sys.exit()
                pageLinkURL = pageLinkURL.get('href')
                pageLinkURL = fix_URL(pageLinkURL)
                
                isThereNextPage = 1
                while(isThereNextPage):
                    # now go to each page and look for individual items
                    pageOverViewSourceCode = requests.get(pageLinkURL,headers = requestHeaders)
                    pageOverViewPlainText = pageOverViewSourceCode.text
                    pageOverViewSoup = BeautifulSoup(pageOverViewPlainText, "html.parser")

                    # let the server rest
                    time.sleep(1)
                    
                    # check for the basic containers
                    for productContainer in pageOverViewSoup.findAll('div', {'class':'span03 product-tile'}):
                        individualProductURL = fix_URL((productContainer.find('a', {'class':'link'})).get('href'))
                        analyse_page(individualProductURL)
                    # check for the advertisement containers
                    for productContainer in pageOverViewSoup.findAll('div', {'class':'span09 product-tile feature-view'}):
                        individualProductURL = fix_URL((productContainer.find('a', {'class':'link'})).get('href'))
                        analyse_page(individualProductURL)
                    # check for compact advertisement containers
                    for productContainer in pageOverViewSoup.findAll('div', {'class':'span03 product-tile compact'}):
                        individualProductURL = fix_URL((productContainer.find('a', {'class':'link'})).get('href'))
                        analyse_page(individualProductURL)
                        
                    # check if there is another page and if there is change the url to that
                    isThereNextPage = 0
                    # if there is actually a page bar find it else move on
                    if(pageOverViewSoup.find('span',{'class':'currentPage'}) != None):                        
                        currentPage = (pageOverViewSoup.find('span',{'class':'currentPage'})).contents[0]
                        nextPage = int(currentPage) + 1
                        print("###Current Page is: " + currentPage, file = debug)
                        print('###Next Page is: ' + str(nextPage), file = debug)
                        pageNumbers = pageOverViewSoup.find('span',{'class':'pagNum'})
                        
                        # due to there being a page bar at the bottom of the page cycle through it till we find the correct link
                        for alternatePage in pageNumbers.findAll('a'):
                            if(int(alternatePage.contents[0]) == int(nextPage)):
                                isThereNextPage = 1
                                pageLinkURL = alternatePage.get('href')
                                print("###Next page URL is: " + pageLinkURL, file = debug)
                                break
                        print("###Is there next page: " + str(isThereNextPage), file = debug)
                        
    conn.commit()
    print("Total bytes analysed was: " + str(totalBytes), file = debug)            
    print("Total pages that couldn't be located with bytes: " + str(totalUnrecordedBytes), file = debug)
    print(str(datetime.now()), file = debug)

    # close text files and database
    debug.close()
    newProducts.close()
    conn.close()
            



# this function cleans the URL, because we may only get part of a URL (such as the end bit)
def fix_URL(urlExtension):
    jbURL = 'https://www.jbhifi.com.au'
    if urlExtension[:4] == "https": # accounts for if the url given is the complete url and already includes the jbURL
        url = urlExtension
    elif urlExtension == '/{{ hit.SKU }}': # accounts for a bug in the program
        url = 'NA'
    elif urlExtension[0] != '/': # accounts for if the url given doesn't start with a '/' but still needs to be added to the end of the jbURL
        url = jbURL + '/' + urlExtension
    else:
        url = jbURL + urlExtension

    print("###Fixed URL is: " + url, file = debug)
    return(url)


# this function removes all the commas in the input and then returns the new string
def comma_remove(sentence):
    newSentence = sentence.replace(",", "-")
    return newSentence



def analyse_page(url):
   

    global numPagesAnalysed
    numPagesAnalysed = numPagesAnalysed + 1
    print(" " + str(numPagesAnalysed) + " pages analysed...", end='\r')
   
    print("###Accessing URL: " + url, file = debug)

    if(url == 'NA'):
        print("###Invalid URL...", file = debug)
        return

    # check if the url is already in the database if it is return because we don't need to add it, otherwise get more information and add it to the database
    # by checking the url before actually accessing the product soup of the page we are reducing the cost on server and overall program time
    c.execute("select count(%s) from products where url = %s", (url, url))
    num = str(c.fetchone())
    num = num.split("(")[1]
    num = num.split(",")[0]
    num = int(num)
    # if there is already a record exit immediately otherwise continue
    if num >0:
        print("###There is already a matching url record...", file = debug)
        return

    # get the size of the webpage in bytes
    res = requests.head(url)
    res = res.headers
    res = str(res)
    #print(res, file = debug)
    if "'Content-Length': '" not in res:
        global totalUnrecordedBytes
        totalUnrecordedBytes += 1
        print("NO BYTES INFORMATION FOUND", file = debug)
    else:
        bytes = res.split("'Content-Length': '")[1]
        bytes = bytes.split("'")[0]   
        print("Bytes is " + str(bytes), file = debug)
        bytes = int(bytes)
        global totalBytes
        totalBytes += bytes
        print("Total bytes is " + str(totalBytes), file = debug)

    # let the server rest
    time.sleep(delayTime)        
        
    #print("###Accessing URL " + url)
    pageSourceCode = requests.get(url, headers=requestHeaders)
    pageText = pageSourceCode.text
    pageSoup = BeautifulSoup(pageText, "html.parser")

    # get the product ID
    productID = str((pageSoup.find('span', {'id':'prodID'})).contents[0])
    print("###ProductID is: " + productID, file = debug)

    # check if the productID of this URL is already in the database if it is return because we don't need to add it, otherwise get more information and add it to the database
    c.execute("select count(id) from products where id = %s", (productID,))
    numID = str(c.fetchone())
    numID = numID.split("(")[1]
    numID = numID.split(",")[0]
    numID = int(numID)
    # if there is already a record exit immediately otherwise continue
    if numID >0:
        print("###There is already a matching productID record...", file = debug)
        return
    
    
    # get the product title
    productTitle = (pageSoup.find('h1')).contents[0]
    productTitle = comma_remove(productTitle)
    # get the SKU
    productSKU = (pageSoup.find('meta', {'property':'sku'})).get('content')
    # get the release date
    productReleaseDate = (pageSoup.find('meta', {'property':'releaseDate'})).get('content')
    # get the brand
    productBrand = (pageSoup.find('meta', {'property':'brand'})).get('content')
    productBrand = comma_remove(productBrand)
    # get the model num
    productModelID = (pageSoup.find('meta', {'property':'model'})).get('content')

    # print the results to the new results file and console
    delimiter = ","
    print("New product: " + productID + delimiter + productSKU + delimiter + productModelID + delimiter + pageHeading + delimiter + productTitle + delimiter + productBrand + delimiter + productReleaseDate + delimiter + url, file = debug)
    print(str(datetime.now()) + delimiter + productID + delimiter + productSKU + delimiter + productModelID + delimiter + pageHeading + delimiter + productTitle + delimiter + productBrand + delimiter + productReleaseDate + delimiter + url, file = newProducts)

    # add the result to the database
    c.execute("INSERT INTO products VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (productID, productSKU, productModelID, pageHeading, productTitle, productBrand, productReleaseDate, url))
    conn.commit()
        
try:
    web_crawler()
except:
    logging.exception("ERROR")


    
    
    
    
