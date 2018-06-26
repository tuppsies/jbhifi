# This program takes in a large text file of URL's and splits it into lots of smaller ones
# This program was originally written on 2017-03-03
# this program requires a numeric arguement

import sys
import mysql.connector


# connect to the mysql database
conn = conn = mysql.connector.connect(user='jbhifi', password='aR5vx?25', host='tupperware.dirtydns.com', database='tupperware_jbhifi')
c = conn.cursor()


# get each URL in the database and put it into a list
c.execute("SELECT url FROM products")
URLSArray = []
for (url) in c:
    URLSArray.append(url)


# create the text files we are going to need
txtFiles = []
maxRange = int((sys.argv)[1])
for num in range (0, maxRange):
    # create the text file name and store it in the list
    txtFiles.append("/home/tupperware/JBHIFIWebCrawler/tmp/%stmp.txt" % str(num))



# now split the url's between the text files
# the following code does this by cycling through the list of urls whilst also cycling through the list of text files and adding each url to a text file
counter = 0
for url in URLSArray:
    currentFile = open(txtFiles[counter], "a")
    #newURL = fix(url)
    print(url, file = currentFile)
    currentFile.close
    if counter == (maxRange-1):
        counter = 0
        continue
    counter = counter+1




# commit and close the database
conn.commit()
conn.close()



