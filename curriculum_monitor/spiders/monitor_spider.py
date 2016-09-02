# -*- coding: utf-8 -*-

import time
import datetime
import pymongo

import scrapy
from scrapy.http import Request, FormRequest
import urllib
import json
import re

from curriculum_monitor.items import CurriculumMonitorItem


class MonitorSpider(scrapy.Spider):
    name = "monitor"
    allowed_domains = ["ucas.ac.cn"]
    start_urls = [
        "http://sep.ucas.ac.cn/appStore"
    ]

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数

    def start_requests(self):
        return [Request("http://sep.ucas.ac.cn/slogin", meta={'cookiejar': 1}, callback=self.post_login)]

        # FormRequeset出问题了

    def post_login(self, response):
        print 'Preparing login'

        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,  # "http://www.zhihu.com/login",
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.headers,  # 注意此处的headers
                                          formdata={

                                              'userName': 'lilelr@163.com',
                                              'pwd': '440921199306191617',
                                              'sb': 'sb'
                                          },
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]

    def after_login(self, response):
        print "after_login: " + response.url
        # for url in self.start_urls:
        #     yield self.make_requests_from_url(url)
        yield scrapy.Request("http://sep.ucas.ac.cn/portal/site/226/821",
                             cookies={"route": "7b8af2c81cb5eb409ef57d5bf81b68bd",
                                      "JSESSIONID": "8197A6EB451D8DA5A6D980B269E64B76",
                                      'sepuser': '"bWlkPWY3ZWZjMjcyLTlhNmYtNDIxYS1iMTcyLTVjZTcwZjExNmZlZQ==  "'},
                             headers=self.headers,
                             callback=self.curriculum_login,
                             dont_filter=True
                             )

    def curriculum_login(self, response):
        print "curriculum_login: " + response.url
        # print response.meta['cookiejar']
        yield scrapy.Request("http://jwxk.ucas.ac.cn/main",
                             cookies={"route": "7b8af2c81cb5eb409ef57d5bf81b68bd",
                                      "JSESSIONID": "8197A6EB451D8DA5A6D980B269E64B76",
                                      'sepuser': '"bWlkPWY3ZWZjMjcyLTlhNmYtNDIxYS1iMTcyLTVjZTcwZjExNmZlZQ==  "'},
                             # meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.curriculum_home,
                             dont_filter=True
                             )

    def curriculum_home(self, response):
        print "curriculum_home: " + response.url
        content = response.xpath('//div[@class="bn-info"]').extract()
        print content
        print "succeed"


    def parse(self, response):
        print "parse: " + response.url
        print "succeed"
        # for sel in response.xpath('//ul/li'):
        #     item = CurriculumMonitorItem()
        #     item['title'] = sel.xpath('a/text()').extract()
        #     item['link'] = sel.xpath('a/@href').extract()
        #     item['desc'] = sel.xpath('text()').extract()
        #     yield item