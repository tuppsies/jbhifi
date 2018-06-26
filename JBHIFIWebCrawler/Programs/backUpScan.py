# This program is a back up and is designed to scan URL's that failed to scan in the main process
# This process will run a short time after the main process has completed

# TO DO add the time
# Also add an archiver at the conclusion of the program

import mysql.connector
import time
import sys
import os


# VERY IMPORTANT the date is in this format as it is what is used in the database
date = str(time.strftime("%Y-%m-%d"))

# set up text files
# must be in tmp directory
#productsToAnalyseFile = "/home/tupperware/JBHIFIWebCrawler/tmp/BackUpScantmp.txt"
#productsToAnalyse = open(productsToAnalyseFile, "w")

backUpUsage = open("/home/tupperware/JBHIFIWebCrawler/Debug/backUpUsage.txt", "a")
debugLocation = "/home/tupperware/JBHIFIWebCrawler/Debug/Archives/" + str(time.strftime("%d-%m-%Y")) + "/backUpScanDebug.txt"
debug = open(debugLocation, "w")
print(date, file = debug)



def main(cycle):

    # set up database connection
    conn = mysql.connector.connect(user='jbhifi', password='aR5vx?25', host='tupperware.dirtydns.com', database='tupperware_jbhifi')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(id) FROM products")
    productCount = str(c.fetchone())
    productCount = productCount.split("(")[1]
    productCount = productCount.split(",")[0]
    productCount = int(productCount)

    c.execute("SELECT COUNT(id) FROM productPricing WHERE date = %s", (date,))
    productPricingCount = str(c.fetchone())
    productPricingCount = productPricingCount.split("(")[1]
    productPricingCount = productPricingCount.split(",")[0]
    productPricingCount = int(productPricingCount)

    # close the database connection
    conn.commit()
    conn.close()

    if productCount == productPricingCount:
        # then backup scan has successfully completed
        # add some stats to the debug file
        print("We have the correct amount of products!", file = debug)
        print("products: " + str(productCount) + " productPricing: " + str(productPricingCount), file = debug)
        # add the final stats to the final file
        print(date + " products: " + str(productCount) + " productPricing: " + str(productPricingCount), file = backUpUsage)
        print(date, file = debug)
        sys.exit(0)
    else:
        print("We do not have the correct amount of products!", file = debug)
        print("products: " + str(productCount) + " productPricing: " + str(productPricingCount), file = debug)
        # we are going to try and scan the database again
        print("About to run WebCrawler again!", file = debug)
        os.system("cd /home/tupperware/JBHIFIWebCrawler/Programs; ./splitter.sh 15")
        # recursively call the function in case the latest run of the program didnt catch everything
        # we can only do one scan at the moment since they all run in the background
        # hack method is wait an estimated amount of time - in this case 3 hours
        time.sleep(10800)
        # run the archiver
        os.system("cd /home/tupperware/JBHIFIWebCrawler/Programs; ./backUpScanArchiver.sh %s" % str(cycle))
        # recursively call the function again
        main(cycle + 1)

main(0)








