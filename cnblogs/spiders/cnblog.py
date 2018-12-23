# -*- coding: utf-8 -*-
import scrapy
import re


class CnblogSpider(scrapy.Spider):
    name = 'cnblog'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://www.cnblogs.com/']

    def parse(self, response):
        total = response.xpath("//div[@class='post_item']")
        for info in total:
            item = dict()
            item['title'] = info.xpath("./div[2]/h3/a/text()").extract_first()
            item['href'] = info.xpath("./div[2]/h3/a/@href").extract_first()
            yield scrapy.Request(
                item['href'],
                callback=self.parse_info,
                meta={"item": item}
            )

        next_url = response.xpath("//a[contains(.,'Next >')]/@href").extract_first()
        next_url = "https://www.cnblogs.com" + next_url
        yield scrapy.Request(
            next_url,
            callback=self.parse,
        )

    def parse_info(self, response):
        item = response.meta['item']
        id = re.findall(r"/p/(.*?).html", item['href'])[0]
        yield scrapy.Request(
            "https://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId=" + str(id),
            callback=self.parse_num,
            meta={"item": item}
        )

    def parse_num(self, response):
        item = response.meta['item']
        item["read_num"] = response.body.decode()
        yield item
