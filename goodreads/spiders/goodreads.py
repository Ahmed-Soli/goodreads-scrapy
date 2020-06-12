import scrapy
from scrapy.loader import ItemLoader
from goodreads.items import QuoteItem

class GoodReadsSpider(scrapy.Spider):
    #identity
    name = 'goodreads'
    #request
    def start_requests(self):
        url = 'https://www.goodreads.com/quotes?page=1'
        
        yield scrapy.Request(url=url,callback=self.parse)
    #response
    def parse(self,response):
        for quote in response.selector.xpath('//div[@class="quote"]'): # Returns a selector object
            # a loader is like a container where we can clean the data 
            loader = ItemLoader(item=QuoteItem(),selector=quote,response=response)
            loader.add_xpath('text','.//div[@class="quoteText"]/text()[1]')
            loader.add_xpath('author','.//span[@class="authorOrTitle"]')
            loader.add_xpath('tags','.//div[@class="greyText smallText left"]/a')
            yield loader.load_item()
        
        next_page = response.selector.xpath('//a[@class="next_page"]/@href').extract_first()

        if next_page is not None :
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link,callback=self.parse)