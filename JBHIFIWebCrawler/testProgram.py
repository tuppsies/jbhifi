from bs4 import BeautifulSoup
import sys
import logging
import requests
import time
import datetime
from datetime import datetime
import mysql.connector


def main():
        url = "https://www.jbhifi.com.au/tv-home-entertainment/hd-televisions/lg/lg-43uj654t-43-uhd-smart-led-lcd-tv/399600/"
        print("beginning main")
        productSourceCode = requests.get(url)
        productPlainText = productSourceCode.text
        productSoup = BeautifulSoup(productPlainText, "html.parser")
        print(productSoup)
        testProdID = productSoup.find('span', {'class':'hiddenCode'})
        if(testProdID == None):
            print("no testProdID")
        print("ending  main")



main()
