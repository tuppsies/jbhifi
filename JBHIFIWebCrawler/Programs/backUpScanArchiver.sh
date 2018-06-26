# This program was written by Joshua Cahill 20-03-2017
# This program takes all the results of the backUpScan and puts them into the archives

#!/bin/bash

# get the current date
currentDate=$(date +%d-%m-%Y)

# make the directories
mkdir /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/backUpScan
mkdir /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/backUpScan/$1
mkdir /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/backUpScan/$1/tmp

# move all the files from the prie analyser into the new directory
for FILE in /home/tupperware/JBHIFIWebCrawler/Debug/PriceAnalyser/*.txt
do
    mv $FILE /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/backUpScan/$1
done

# move the text files located in tmp into the debug folder
for FILE in /home/tupperware/JBHIFIWebCrawler/tmp/*.txt
do
    mv $FILE /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/backUpScan/$1/tmp
done
