import scrapy
from scrapy.http import Request, FormRequest
from zalando.items import ZalandoItem
import json

class zalandoSpider(scrapy.Spider):
    name = "zalando"
    
    allowed_domains = ["https://fr.zalando.ch",]
    
    #start_urls_1 = ["https://fr.zalando.ch/mode-femme/?p="+str(item) for item in range(25)]
    #start_urls_2 = ["https://fr.zalando.ch/chaussures-femme/?p="+str(item) for item in range(25)]
    #start_urls_3 = ["https://fr.zalando.ch/sacs-accessoires-femme/?p="+str(item) for item in range(5)]
    #start_urls = start_urls_1 + start_urls_2 + start_urls_3

    start_urls_1 = ["https://fr.zalando.ch/mode-homme/?p="+str(item) for item in range(35)]
    start_urls_2 = ["https://fr.zalando.ch/chaussures-homme/?p="+str(item) for item in range(10)]
    start_urls_3 = ["https://fr.zalando.ch/sacs-accessoires-homme/?p="+str(item) for item in range(5)]
    start_urls = start_urls_1 + start_urls_2 + start_urls_3
    
    @staticmethod
    def save_to_path(url):
        filename = url.split('/')[-1]
        return './zalando_male/%s' % filename

    def parse(self, response):
        a = response.xpath('//body/div[@id="wrapper"]/div[@id="wt_refpoint"]/div[@id="content"]/div[@class="mainCol"]/ul[@id="catalogItemsListParent"]/li/div[@class="catalogArticlesList_container"]/div[@class="catalogArticlesList_overlay"]/div[@class="catalogArticlesList_content"]/a/@href').extract()
        a = json.loads('["' + '","'.join(str(e) for e in a) +'"]')
        next_page = response.xpath('//body/div[@id="wrapper"]/div[@id="wt_refpoint"]/div[@id="content"]/div[@class="mainCol"]/div[@class="catalog_pager"]/div[@class="catalogPagination"]/a[@class="catalogPagination_button catalogPagination_button-next"]/@href').extract_first()
        request_list = []
        for el in a:
            request_list.append(scrapy.Request("https://fr.zalando.ch"+el, callback=self.parse_prod,dont_filter=True))
        return request_list
       
    def parse_prod(self, response):
        url = response.xpath('.//body/*/*/*/*/*/*/img/@src').extract_first()
        request = scrapy.Request(url, callback=self.save_image, dont_filter=True)
        return request

    def save_image(self, response):
        path = self.save_to_path(response.url)
        with open(path, "wb") as f:
            f.write(response.body)
