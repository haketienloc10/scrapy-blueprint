import scrapy
import time
import requests
from scrapy.selector import Selector
import json

class ExtractSpider(scrapy.Spider):

    name = 'text'
    handle_httpstatus_list = [404, 500, 503]

    def extension_xpath(self, argument):
        switcher = {
            "text": "//text()",
            "href": "//@href",
            "img": "//@src"
        }
        return switcher.get(argument, "nothing")

    def parse(self, response):
        try:
            if response.status in (404, 500):
                response = requests.get(response.url)
            start = time.time()
            if len(self.quotes_list) > 0:
                    self.quotes_list.clear()
            self.quotes_list.update({"web":response.url})
            tmp_dict = {}
            selector = Selector(response)
            for d in self.data:
                xpath = d.get('xpath')
                xpath += self.extension_xpath(d.get('type'))
                quotes = []
                for quote in selector.xpath(xpath).extract():
                    if len(quote.encode('utf-8').strip()) > 0:
                        quotes.append(quote)
                if len(quotes) > 1:
                    tmp_dict.update({d.get('field'):quotes})
                else:
                    tmp_dict.update({d.get('field'):quotes[0]})
            self.quotes_list.update({"data":tmp_dict})
        finally:
            end = time.time()
            print(end - start)
