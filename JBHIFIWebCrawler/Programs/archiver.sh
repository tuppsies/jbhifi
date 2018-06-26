# This program first written by Joshua Cahill 8-03-2017
# This program takes all the debug files from the most previous job and moves them to the archive folder
# This program may also delete and recreate the directories that the debug files are stored in to make sure that they are clear

#!/bin/bash

# get the current date
currentDate=$(date +%d-%m-%Y)

# make the new directories
mkdir /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate
mkdir /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/PriceAnalyser
mkdir /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/WebCrawler
mkdir /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/PriceAnalyser/tmp

# move the files from the price analyser into the new directory
for FILE in /home/tupperware/JBHIFIWebCrawler/Debug/PriceAnalyser/*.txt
do
    mv $FILE /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/PriceAnalyser
done

# move the files from the web crawler into the new directory
for FILE in /home/tupperware/JBHIFIWebCrawler/Debug/WebCrawler/*.txt
do
    mv $FILE /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/WebCrawler
done

# move the text files located in tmp into the debug folder
for FILE in /home/tupperware/JBHIFIWebCrawler/tmp/*.txt
do
    mv $FILE /home/tupperware/JBHIFIWebCrawler/Debug/Archives/$currentDate/PriceAnalyser/tmp
done

# delete both debug folders then recreate them??
