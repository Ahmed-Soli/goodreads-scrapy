# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose , TakeFirst , Join 
from w3lib.html import remove_tags

def remove_unicodes_char(value):
    return value.replace(u"\u201c",'').replace(u"\u201d",'')


class QuoteItem(scrapy.Item):
    
    text = scrapy.Field(
        input_processor = MapCompose(str.strip,remove_unicodes_char),
        output_processor= TakeFirst()
    )
    author = scrapy.Field(        
        input_processor = MapCompose(remove_tags,lambda value: value.replace('\n',''),str.strip),
        output_processor = TakeFirst()
    )
    tags = scrapy.Field(
        input_processor = MapCompose(str.strip,remove_tags),
        output_processor = Join(',')
        )
