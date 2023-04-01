import scrapy


class FmoviesSpider(scrapy.Spider):
    name = "fmovies"
    allowed_domains = ["fmovies.wtf"]
    start_urls = ["http://fmovies.wtf/"]

    def parse(self, response):
        pass
