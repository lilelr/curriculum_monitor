# -*- coding: utf-8 -*-

import time
import sys
import datetime
import pymongo

import scrapy
from scrapy.http import Request, FormRequest
import easygui
import urllib
import json
import re

from curriculum_monitor.items import CurriculumMonitorItem


def format_words(buf, param=0):
    # 去除字符串buf前后空白字符
    # 当param > 0时，还将去除字符串内部所有换行符
    buf = buf.strip()
    if param > 0:
        buf = buf.replace('\r', '').replace('\n', '')
    return buf


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

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数

    def start_requests(self):
        return [Request("http://sep.ucas.ac.cn/slogin", meta={'cookiejar': 1}, callback=self.post_login)]

        # FormRequeset

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
                             cookies={"route": "11d66bd81470cf8d05a0e237dde4c51e",
                                      "JSESSIONID": "D779C723FE5AC5E9D352F4A84CACE36C",
                                      'sepuser': '"bWlkPWM4MGYwMDliLWI2ODAtNDZkYi05ZTIzLWQ5N2NjZGE1N2NiMw==  "'},
                             # meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.curriculum_home,
                             dont_filter=True
                             )

    def curriculum_home(self, response):
        print "curriculum_home: " + response.url
        # content = response.xpath('//div[@class="bn-info"]').extract()
        # print content
        # print "succeed"
        # get 请求
        yield scrapy.Request("http://jwxk.ucas.ac.cn/courseManage/main",
                             cookies={"route": "11d66bd81470cf8d05a0e237dde4c51e",
                                      "JSESSIONID": "D779C723FE5AC5E9D352F4A84CACE36C",
                                      'sepuser': '"bWlkPWM4MGYwMDliLWI2ODAtNDZkYi05ZTIzLWQ5N2NjZGE1N2NiMw==  "'},
                             # meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.course_manage_main_request,
                             dont_filter=True
                             )

    def course_manage_main_request(self, response):
        print "course_manage_main_request: " + response.url
        return [
            FormRequest(url="http://jwxk.ucas.ac.cn/courseManage/selectCourse?s=6014582c-de59-45ca-9e01-7ca4e8696966",
                        headers=self.headers,  # 注意此处的headers
                        formdata={
                            'deptIds': '951',
                            'sb': '0'
                        },
                        callback=self.parse,
                        dont_filter=True
                        )]

    def parse(self, response):
        # print "parse: " + response.url
        # code = response.xpath("//span[@id='courseCode_125725']/text()").extract()[0]
        # print code
        # 课程代码
        curriculum_code = response.xpath(
            "//div[@class='mc-body']/form[@id='regfrm']//tr[6]/td[3]/a/span/text()").extract()[0]
        print "curriculum_code: " + curriculum_code
        # 课程名称
        curriculum_name = response.xpath("//div[@class='mc-body']/form[@id='regfrm']//tr[6]/td[4]/a/text()").extract()[
            0]
        print "curriculum_name: " + curriculum_name
        # 课程选课限制人数
        restrict = response.xpath("//div[@class='mc-body']/form[@id='regfrm']//tr[6]/td[7]/text()").extract()[0]

        print "restrict:  " + restrict
        # for each_item in restrict:
        #     print str("eachItem+" + each_item)
        #     each_item = format_words(each_item, 1)
        #     print str(each_item)
        # 目前课程已选人数
        students = response.xpath("//div[@class='mc-body']/form[@id='regfrm']//tr[6]/td[8]/text()").extract()[0]
        print "number: " + students
        # 开课老师
        teacher = response.xpath("//div[@class='mc-body']/form[@id='regfrm']//tr[6]/td[12]/a/text()").extract()[0]
        print teacher
        current_time = time.strftime(u'%Y年-%m月-%d日-%H时-%M分', time.localtime(time.time()))
        # print current_time

        content = current_time + "\n" \
                                 u"课程代码:" + curriculum_code + "\n" + u"课程名称:" + curriculum_name + "\n" \
                  + u"课程选课限制人数:" + restrict + "\n" + u"目前课程已选人数: " + students + "\n" \
                  + u"开课老师: " + teacher + "\n"

        restrict = int(restrict)
        students = int(students)

        if students < restrict:
            easygui.msgbox(u"算法课有空缺位置了,亲!" + "\n" + content, 'curriculum_monitor')
        else:
            easygui.msgbox(u"目前," + teacher + u"开的算法课选课人数已满." + "\n" + content, 'curriculum_monitor')


            # print "succeed"

            # for sel in response.xpath('//ul/li'):
            #     item = CurriculumMonitorItem()
            #     item['title'] = sel.xpath('a/text()').extract()
            #     item['link'] = sel.xpath('a/@href').extract()
            #     item['desc'] = sel.xpath('text()').extract()
            #     yield item
