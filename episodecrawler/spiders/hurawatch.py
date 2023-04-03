import scrapy

from pprint import pprint
from .helpers.helper import replace_whitespace, get_cosine_similarity, vectorize_string, get_cosine_similarity2, capitalize_all_words
from urllib.parse import urlencode
class HurawatchSpider(scrapy.Spider):
    name = "hurawatch"
    allowed_domains = ["hurawatch.cc"]
    start_urls = ['http://hurawatch.cc/']

    current_page = 1
    end_page = 6 # max page is 5
    
    def __init__(self, search_term = 'family guy'):
        self.container = []
        self.search_term = replace_whitespace(
            search_term.strip().capitalize() # strip all the trailing whitespaces
            ) # replace all the whitespaces with a dash
        self.actual_term = capitalize_all_words(search_term.strip()) # capitalize all the words in the search term

    def start_requests(self):
        main_path = 'http://hurawatch.cc/search/'

        for i in range(self.current_page, self.end_page):
            params = {'page': i}
            url = main_path + self.search_term + '?' + urlencode(params)
            print(url)
            yield scrapy.FormRequest(url= url, callback=self.parse)


    def parse(self, response):
        try:
            shows = response.css('div.flw-item')
            for show in shows:
                link = show.css('div.film-poster a::attr(href)').get()
                if link:
                    link = 'http://hurawatch.cc' + link
                title = show.css('div.film-detail h2.film-name a::text').get()

                try: # get cosine similarity, if first fails, it means the dimensions are different, so use the second method
                    title_vector = vectorize_string(title)
                    search_term_vector = vectorize_string(self.actual_term)
                    similarity = get_cosine_similarity(title_vector, search_term_vector)
                    if similarity > 0.5:
                        self.container.append( {title : {
                            'similarity': similarity,
                            'page': self.current_page, 
                            'link': link
                            }
                        })
                
                except ValueError:
                    title_vector = vectorize_string(title)
                    search_term_vector = vectorize_string(self.actual_term)
                    similarity = get_cosine_similarity2(title_vector, search_term_vector)
                    if similarity > 0.5:
                        self.container.append( {title : {
                            'similarity': similarity,
                            'page': self.current_page, 
                            'link': link
                            }
                        })

            highest_value = 0
            highest_value_link = ''
            for item in self.container:
                for key, value in item.items():
                    if value['similarity'] > highest_value:
                        highest_value = value['similarity']
                        highest_value_link = value['link']
            print(f"Highest value: {highest_value} with link: {highest_value_link}")

        except Exception as e:
            print(repr(e))
