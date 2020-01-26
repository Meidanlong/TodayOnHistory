# -*- coding: utf-8 -*-
import scrapy

from urllib import parse
from scrapy.http import Request

from todayonhistory.items import TodayonhistoryItem


class TohSpider(scrapy.Spider):
    name = 'toh'
    allowed_domains = ['today.911cha.com/']
    # start_urls = ['http://today.911cha.com/']
    start_urls = []

    for year_index in range(366):
        year_url = 'http://today.911cha.com/history_'+str(year_index+1)+'.html'
        # print(year_url)
        start_urls.append(year_url)


    # host

    def parse(self, response):
        post_nodes = response.xpath('//*[@id="mainbox"]/div[1]/div[2]/div[2]/p/a')

        # title = response.css('#mainbox .f14 a').extract()
        for post_node in range(0,len(post_nodes),3):
            year_index = post_nodes[post_node]
            year = year_index.xpath('text()').extract_first('')

            day_index = post_nodes[post_node+1]
            day = day_index.xpath('text()').extract_first('')

            title_index = post_nodes[post_node+2]
            title = title_index.xpath('text()').extract_first('')
            title_herf = title_index.xpath('@href').extract_first('')

            # full_url = parse.urljoin(response.url,event_herf)
            full_url = 'http://today.911cha.com/'+title_herf

            # print(year+day+title+' -> '+full_url)
            # print(parse.urljoin(response.url,event_herf))

            meta = {
                       "year": year,
                       "day": day,
                       "title": title
                    }

            yield Request(url=parse.urljoin(response.url, title_herf), meta=meta,
                          callback=self.parse_detail,dont_filter=True)



    def parse_detail(self,response):
        # content = response.css('#mcon')
        contents = response.xpath('//*[@id="mainbox"]/div[1]/div[2]/div[2]/p/text()').extract()
        content = ''
        for index, c in enumerate(contents):
            if index > 0:
                content = content+'<br>'+c
            else:
                content = c
        # print(content)

        item = TodayonhistoryItem()
        item['year'] = str(response.meta.get('year','')).replace('年','')
        item['day'] = response.meta.get('day','')
        md = str(item['day']).replace('日','').split('月')
        month = int(md[0])
        day = int(md[1])
        item['weight'] = month*100+day
        item['title'] = response.meta.get('title','')
        item['content'] = content

        print(item['year'] +" "+ str(item['weight']) + item['title'] + ' ----> ' + item['content'])

        yield item



