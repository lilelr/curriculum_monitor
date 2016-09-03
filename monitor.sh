#!/bin/bash
i=1
while :
do
	echo "start"
        scrapy crawl monitor
        ((i++))
        # 每隔 n 秒运行一次
        sleep 300
done
