#!/bin/bash
i=1
while :
do
	echo "start"
        scrapy crawl monitor
        ((i++))
        sleep 300
done
