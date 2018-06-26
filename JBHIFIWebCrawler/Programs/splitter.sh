#!/bin/bash

# Started by Joshua Cahill on 3/3/2017
# This program will split the database up easily to analyse it
# It takes a number as the first arguement which identifies how many text files and processes it will have

# remove the directories we are going to create in case they already exist
rm -r /home/tupperware/JBHIFIWebCrawler/tmp


# create a tmp directory to store the text files
mkdir /home/tupperware/JBHIFIWebCrawler/tmp

# First of all we take all the urls from the mysql database and split them into different text files
# call a python script to do this
python3 /home/tupperware/JBHIFIWebCrawler/Programs/splitter.py $1

#Check if we have an internet connection before we begin analysing the text files
wget -q --tries=10 --timeout=20 --spider http://google.com


# TO DO make this into a while loop
if [[ $? -eq 0 ]]; then
    # We have an internet connection
    # Then run analysis on all the text files at once and simulatenously
    for textFile in /home/tupperware/JBHIFIWebCrawler/tmp/*.txt
    do
        python3 /home/tupperware/JBHIFIWebCrawler/Programs/JBHIFIPriceAnalyser.py $textFile &
    done
else
        echo "Offline"
fi



