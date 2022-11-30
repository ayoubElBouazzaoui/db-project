import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from db_data import get_onderneming, insert_query
from urllib.parse import urlparse
from threading import Lock
from urllib.parse import urlparse

from scrapy.exceptions import IgnoreRequest, NotConfigured
import re
def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'https://{}'.format(url)
    return url
class WebSpider(scrapy.Spider):
    
    name = "webspider"
   
    DEPTH_LIMIT = 2
    
   
     

    def __init__(self):
        self.links=[]
        self.allowed_domains = []

        for row in get_onderneming():
            
          if row[7] is not None :
           
            self.allowed_domains.append(str(urlparse(row[7]).hostname))
       


    def  start_requests(self):
        print("hello")

        for row in get_onderneming():
          if row[7] is not None:
            print(formaturl(row[7]))
            
            yield  scrapy.Request(formaturl(row[7]) ,
                callback =  self.parse , cb_kwargs={'comp':row[1],'id':row[0], 'count' : 0})
            
            
    
        
    # include_patterns = ['']
    exclude_patterns = ['.*\.(css|js|gif|jpg|jpeg|png|Store|Contact|contact|Contacteer|Catalog|catalog|contacteer)']

   


    response_type_whitelist = ['text/html']
    


    def parse(self, response, comp, count, id):
        if count <= 2 :
            
            print("///////////////////////")
            print( response.url  )
            print(comp)
            text = ''.join(response.selector.xpath("//body//text()").extract() )
            print("///////////////////////")
        
            query = 'INSERT INTO dep."html_paginas"("naam","url", "text", "id") VALUES(  %s,%s,%s,%s ) '
            insert_query(query, comp , id, text,response.url)
            for url in LinkExtractor(allow_domains=self.allowed_domains).extract_links(response):
                if url:
                    
                    yield    response.follow(url = url,
                                callback = self.parse,cb_kwargs={'comp':comp, 'count' : count+1, "id":id})
        
        else: 
            print(f" DONE ON DEPTH {count}")

   
    
process = CrawlerProcess()

process.crawl(WebSpider)
process.start()
