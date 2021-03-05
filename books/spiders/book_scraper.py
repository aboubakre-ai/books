import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookScraperSpider(CrawlSpider):
    name = 'book_scraper'
    allowed_domains = ['books.toscrape.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'

    start_urls = ['https://books.toscrape.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    
    def start_request(self):
        yield scrapy.Request(url= 'https://books.toscrape.com',headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//article[@class="product_pod"]/h3/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield{
            'book_name': response.xpath("//div[contains(@class,'product_main')]/h1/text()").get(),
            'price': response.xpath("//div[contains(@class,'product_main')]/p[1]/text()").get(),
        }
