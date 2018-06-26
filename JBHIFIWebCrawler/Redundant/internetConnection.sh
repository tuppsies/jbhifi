#WE DO NOT NEED TO USE THIS PROGRAM JAMES AND CHRIS
#!/bin/bash
# This result pings the default gateway to check for an internet connection
# If we don't have an internet connection then we wait until we get one


result="$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)"

while [ $result = "error" ]
do
result="$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)"
echo result
done

if [ $result = "ok" ]; then
    echo We have an internet connection
    echo Beginning web crawler
    python3 /home/tupperware/JBHIFIWebCrawler/Programs/JBHIFIWebCrawler.py
    echo Beginning price analyser
    python3 /home/tupperware/JBHIFIWebCrawler/Programs/JBHIFIPriceAnalyser.py
fi
