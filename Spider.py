import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
import db_data
import re
from urllib.parse import urlparse

fiscaal_jaar = 2021
def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'https://{}'.format(url)
    return url

class WebSpider(scrapy.Spider):
    name = "webspider"

    DEPTH_LIMIT = 3

    def __init__(self):
        self.links = []
        self.allowed_domains = []
        for row in db_data.get_ondernemingen(fiscaal_jaar):
            self.allowed_domains.append(urlparse(row[1]).hostname)

    def start_requests(self):
        for row in db_data.get_ondernemingen(fiscaal_jaar):
            yield scrapy.Request(formaturl(row[1]),
                                 callback=self.parse, cb_kwargs={'comp': row[1]})

    # include_patterns = ['']
    exclude_patterns = ['.*\.(css|js|gif|jpg|jpeg|png|Store|Contact||.be/fr/|.be/en/|/be-fr/|/be-en/)']

    response_type_whitelist = ['text/html']

    def parse(self, response, comp):
        str1 = ""
        print("///////////////////////")
        print(response.url)
        print(comp)
        text = ''.join(response.selector.xpath("//body//text()").extract())
        print("///////////////////////")
        query = 'INSERT INTO dep."html_paginas"("naam","url", "text") VALUES(  %s,%s,%s ) '
        db_data.insert_query(query, comp, response.url, text)
        for url in LinkExtractor(allow_domains=self.allowed_domains).extract_links(response):
            if url:
                print(url)
                yield response.follow(url=url,
                                      callback=self.parse, cb_kwargs={'comp': comp})


process = CrawlerProcess()

process.crawl(WebSpider)
process.start()