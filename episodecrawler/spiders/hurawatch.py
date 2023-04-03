import scrapy

from .helpers.helper import replace_whitespace
from urllib.parse import urlencode
class HurawatchSpider(scrapy.Spider):
    name = "hurawatch"
    allowed_domains = ["hurawatch.cc"]
    start_urls = ["http://hurawatch.cc/"]
    end_page = 5 # max page is 5
    search_term = 'family guy'
    
    def __init__(self, search_term = 'family guy'):
        self.search_term = replace_whitespace(
            search_term.strip() # strip all the trailing whitespaces
            ) # replace all the whitespaces with a dash

    def start_requests(self):
        main_path = 'http://hurawatch.cc/search/'
        current_page = 1

        params = {
            'page': 1
            }
        
        while current_page != self.end_page:
            params['page'] = current_page
            current_page += 1
        yield scrapy.Request(url= main_path + self.search_term + '?' + urlencode(params), callback=self.parse)

    def parse(self, response):
        print(response.text)
