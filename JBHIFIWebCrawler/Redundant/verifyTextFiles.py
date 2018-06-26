# This program will verify how many lines are in all the text files that we created.
# Just a debugging tool
# Written by Joshua Cahill 6/3/2017

import sys
import os


def verifyTextFiles():

    directory = "/home/tupperware/JBHIFIWebCrawler/tmp/"
    # assuming that all files in the directory are just the text files
    totalCount = 0;
    for file in os.listdir(directory):
        file = directory + file
        openFile = open(file, "r")
        localCount = 0
        for line in openFile:
            localCount += 1
        totalCount += localCount
        print(file + "\t" + str(localCount) + " lines")
    
    print("Total number of lines is: " + str(totalCount))


verifyTextFiles()
