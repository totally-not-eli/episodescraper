import scrapy

from pprint import pprint
from .helpers.helper import replace_whitespace, get_cosine_similarity, vectorize_string, get_cosine_similarity2
from urllib.parse import urlencode
class HurawatchSpider(scrapy.Spider):
    name = "hurawatch"
    allowed_domains = ["hurawatch.cc"]
    start_urls = ["http://hurawatch.cc/"]
    BASE_URL = 'http://hurawatch.cc'

    current_page = 1
    end_page = 6 # max page is 5
    
    def __init__(self, search_term = 'family guy'):
        self.container = dict()
        self.search_term = replace_whitespace(
            search_term.strip() # strip all the trailing whitespaces
            ) # replace all the whitespaces with a dash

    def start_requests(self):
        main_path = 'http://hurawatch.cc/search/'
        params = {
            'page': self.current_page
            }
        
        while self.current_page != self.end_page:
            
            if self.current_page == 5:
                print("Scraping last page...")
                print(self.container)
                # once we scraped all the 5 pages, we now check the highest value in the container
                # and return the link to the highest value
                highest_value = max(self.container, key=lambda x: self.container[x]['similarity'])
                print("Highest value:", highest_value)
                print("Similarity:", self.container[highest_value]['similarity'])
                print("Page:", self.container[highest_value]['page'])
                print("Link:", self.container[highest_value]['link'])
                

            params['page'] = self.current_page
            self.current_page += 1
            yield scrapy.Request(url= main_path + self.search_term + '?' + urlencode(params), callback=self.parse)

    def parse(self, response):
        try:
            shows = response.css('div.flw-item')
            for show in shows:
                link = show.css('div.film-poster a::attr(href)').get()
                if link:
                    link = self.BASE_URL + link
                title = show.css('div.film-detail h2.film-name a::text').get()

                try: # get cosine similarity, if first fails, it means the dimensions are different, so use the second method
                    title_vector = vectorize_string(title)
                    search_term_vector = vectorize_string(self.search_term)
                    similarity = get_cosine_similarity(title_vector, search_term_vector)
                    if similarity > 0.5:
                        self.container[title] = {
                            'similarity': similarity,
                            'page': self.current_page, 
                            'link': link
                            }

                except ValueError:
                    title_vector = vectorize_string(title)
                    search_term_vector = vectorize_string(self.search_term)
                    similarity = get_cosine_similarity2(title_vector, search_term_vector)
                    if similarity > 0.5:
                        self.container[title] = {
                            'similarity': similarity,
                            'page': self.current_page, 
                            'link': link
                            }
            
            pprint(self.container)
                        
                    


        except Exception as e:
            print(repr(e))
