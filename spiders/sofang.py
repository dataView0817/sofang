# -*- coding: utf-8 -*-
import time

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from houses.items import HousesItem
import re

class SofangSpider(scrapy.Spider):

    name = 'sofang'
    allowed_domains = ['sofang.com']
    base_urls = 'http://sz.sofang.com/'

    headers = {
        'Hosts': 'www.sofang.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Cookie': 'UM_distinctid=16de3d585824a1-0d115e2c8f0b96-1d3b6b55-f8100-16de3d585833fe; uniqueName=ec8c270a9b66dbc32732dcbe397f2009; CNZZDATA1262285598=1122613754-1571483714-%7C1572077987; XSRF-TOKEN=eyJpdiI6IkppdDc3eG1CTXBUZUtma3lUU0RLR0E9PSIsInZhbHVlIjoiMm1BODhOQ0ZIUWNrdnVFOG9cL05GdG0zbEJjOHN5XC9vekVORThESGFOQUh3eE83bDl1R0IwZkZLMVc3YW1wa0l2MjVwSVRsOFNcL0lSMWlRS1FBMWdBNEE9PSIsIm1hYyI6IjI4ZjRhMjhiZDE5NTViMTNkMzk5NzA0ZTlkZjVjYTRkMGE1YWY2ZjQ2YmE1NzUyMjc2YjFiYTliMTFlMzcyYmUifQ%3D%3D; www_sofang_session=eyJpdiI6IllzVFM3NWUxUnp0d1hwSklwbFVjUVE9PSIsInZhbHVlIjoiRFBtU3hONTlpdkhZM25aKzVRNERha3FJZ0JxcFlyRVllTUNORVRreW52V05OUE9ETmNlSWxRSXhvUG5kV0o2UjdxdVwvejdUY1hsM2lzMngraE5iclBnPT0iLCJtYWMiOiIwNmUxMTE3Njc0ZDc5ZTk4YTU5NWEzMGZkOGJkYmZhYjY2Njc2OTI4YTYxOGMxODMzYjZlZGQwYmYyMjFkNWQ1In0%3D; cityid=eyJpdiI6Ik9nYlwvd0VheG10elhBaVJrbFhCTjNRPT0iLCJ2YWx1ZSI6IldIREhGQWh5WCt5K0M2TXlcLzE5alVBPT0iLCJtYWMiOiI4MTE5YTIxNzNiODc5ODFlOTNkZDQ5YjU5NDAzZTg3NzNhNzJhM2Y3MDYxNjExNDNiYjljNjYwMTVmOWZiNzI0In0%3D; city=eyJpdiI6IlwvQUxuQ3JmV3F2eExOYkFueGZqSVdRPT0iLCJ2YWx1ZSI6IlRZNWEra1Z1K2lFUGpUSTE2UEwrS3RoZCtKeTZDZlFZYUxkXC84Rk9TdkVaNTVJWHMyMCtIcVwvd0JwdkVcL0M0VzloRFdLSENsUWxiUnc0YStSckhRTXNWVWkwUjd6bFZ5MEVWUER3RGlNbk9iN0lGeGtvdlFMUzlIb1ltU1NlVEd1YkY3RWZ0ZUVZSmVBZnpEU0J0eDJENjFSeHc3dW9NdEUwYytGQnVcL05oRms2ZHJ4VUlTQVhYd1NIUHppZ09ObzRDM0d2UFd5dGZxUmp6cDIrMWFnVHJaMGZudWpcL1ZjM01XaUxqV3NSeTdnSnpLUVFKdFFWT1UzNlpIVldaVStmaUwwbm9EQUJnWThiRGpiVzU5cXM2WXhzd05oRVFvQ0FnVG12M3g1VFdhdms9IiwibWFjIjoiYzA3NTgyM2ZkNDg0NTBiNDI3ZTM2MzE0MjkwZGNiMjFiMjljOTVhZTYzYzliMDM4N2ZiMGNlMTE0ODQzNWYwMyJ9; citypy=eyJpdiI6Inl2enhxZkZBckVwbE9aaUdSS0IwRHc9PSIsInZhbHVlIjoid29BMGtWYnNKUTJLdGJqVlhERFBoQT09IiwibWFjIjoiNTMwMzI5NjM2NGE5MmE3ZmNlMzMxODk4NjJiOTgxYjVjYmRkNmY4M2JlYjViZDRlMjFhMjE3NjM5MzQzM2ExMSJ9',
    }

    def start_requests(self):
        for i in range(20,100):
            yield Request(url=self.base_urls+'esfrent/area/bl'+str(i), headers = self.headers, callback=self.parse_index, errback=self.errback)

        # yield Request(url=self.base_urls + 'esfrent/', headers=self.headers, callback=self.parse_index,
        #           errback=self.errback)

    def errback(self, failure):
            self.logger.error(repr(failure))


    def parse_index(self, response):

            # soup = BeautifulSoup(text, 'lxml')

            for url in response.xpath('//a[re:test(@href, "\/housedetail\/.*?.html")]//@href'):
                detail_url = self.base_urls + url.extract()
                yield Request(detail_url, headers=self.headers, callback=self.parse_detail)

                # for house_msg in soup.find_all('dd', class_='house_msg'):
                #     # 名字
                #     print(house_msg.find('p', class_='name').a.string)
                #     # 地区
                #     area_clearfix = house_msg.find('p', class_='area clearfix')
                #     print(area_clearfix.a.string)
                #     print(area_clearfix.span.string)
                #
                #     # 类型
                #     house_type = house_msg.find('p', attrs={'class': 'type clearfix'})
                #     for child in house_type.children:
                #         print(child.string)


    def parse_detail(self, response):

        title = response.xpath('//div[@class="detail"]//p[@class="house_name"]/text()').extract_first()
        city = '广州'

        featureList = response.xpath('//p[@class="house_tge"]/span/text()').extract()
        feature = '、'.join(featureList)

        rent = response.xpath('//p[@class="total"]').css('span::text').extract_first()
        rentWay = response.xpath('//span[@class="sale_price margin_l"]/text()').extract_first()

        print(response.xpath('//div[@class="info"]/dl/dt/text()').extract())
        layouts = response.xpath('//div[@class="info"]/dl/dt/text()').extract()[0].strip()
        layout = layouts.replace('\r','').replace('\n','').replace(' ','')

        acreage = response.xpath('//div[@class="info"]/dl/dt/text()').extract()[1]
        toward = response.xpath('//div[@class="info"]/dl/dt/text()').extract()[2]
        print(toward)
        region = response.xpath('//ul[@class="msg"]/li/span/text()').extract_first().strip()
        address = response.xpath('//ul[@class="msg"]/li/span/text()').extract()[1].strip()

        introductions = response.xpath('//div[@class="box"]/div[@class="depict"]').css('*::text').extract()
        introduction = ''.join(introductions)

        picture = response.xpath('//div[@class="house_info"]').css('img')[1].attrib['src']

        houseItem = HousesItem()
        for field in houseItem.fields:
            try:
                houseItem[field] = eval(field)
            except NameError:
                print('Field is not defined', field)
        print(houseItem)

        yield houseItem
