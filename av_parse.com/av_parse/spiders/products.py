import scrapy
import re
import requests
from scrapy.http.request import NO_CALLBACK


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["av.ru"]
    start_urls = ["https://av.ru"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }

    def start_requests(self):
        iter_flag = True
        page_count = 1
        while iter_flag:
            url = f'https://av.ru/category/offer?q=%3Aacbestseller&showPreOrder=false&pageSize=50&page={page_count}'
            response = requests.get(url, headers=self.headers)
            if response.json()['products']:
                page_count += 1
                for i in response.json()['products']:
                    url = f'https://av.ru{i["url"]}'
                    print(url)
                    yield scrapy.Request(url, callback=self.parse)
            else:
                iter_flag = False

    def parse(self, response):
        item = {
            'good_name': response.css('.product-cart-head_product-name::text').extract_first('').strip(' \n'),
            'price': response.css('.product-cart-special_main_price_num::text').extract_first('').strip(' ₽\n').replace(',', '.').replace(' ', ''),
            'price_old': response.css('.product-cart-special_sale_num::text').extract_first('').strip(' ₽\n').replace(',', '.').replace(' ', ''),
            'img_url': re.search(r"http([\S]+)(.jpg|.jpeg|.png|.gif|.svg)", response.css('.image::attr(style)').extract_first(''))[0],
            'url': response.url,
            'unit_raw': re.search(r"([А-я]+)", response.css('.product-cart-special_main_price_sub::text').extract_first(''))[0],
            'item_id': response.url[-7:][:6],
            'category': response.css('.breadcrumbs_item::text').extract()[-2].strip(' \n'),
            'region': response.css('.header-main-city_text::text').extract_first('').strip(' \n'),
            'retailer_name': 'av',
        }
        yield item
