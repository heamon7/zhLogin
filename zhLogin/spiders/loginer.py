# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from scrapy.conf import settings
from scrapy import log
from scrapy.shell import inspect_response
from datetime import datetime


from datetime import datetime

from zhLogin.items import ZhloginItem

class LoginerSpider(scrapy.Spider):
    name = "loginer"
    allowed_domains = ["www.zhihu.com"]
    start_urls = (
        'http://www.www.zhihu.com/',
    )



    def __init__(self):
        pass

    def start_requests(self):
        #print "start_requests ing ......"
        return [Request("http://www.zhihu.com",callback = self.post_login)]

    def post_login(self,response):
       # print "post_login ing ......"
        xsrfvalue = response.xpath('/html/body/input[@name= "_xsrf"]/@value').extract()[0]
        return [FormRequest.from_response(response,
                                          #headers = self.headers,
                                          formdata={
                                              '_xsrf':xsrfvalue,
                                              'email':'heamon8@163.com',
                                              'password':'heamon8@()',
                                              'rememberme': 'y'
                                          },
                                          dont_filter = True,
                                          callback = self.after_login
                                        #  dont_filter = True
                                          )]

    def after_login(self,response):
        #print "after_login ing ....."
        #inspect_response(response,self)
        self.urls = ['http://www.zhihu.com/question/20767389']
        for url in self.urls:
            yield self.make_requests_from_url(url)


    def parse(self,response):

        item =  ZhloginItem()
        print  datetime.now()
        print response.xpath('//*[@id="zh-single-question-page"]//span[@class="time"]/text()').extract()[0]
        #inspect_response(response,self)
        return item
