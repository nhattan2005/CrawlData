import scrapy


class ProductspiderSpider(scrapy.Spider):
    name = "productspider"
    allowed_domains = ["hoanghamobile.com"]
    start_urls = ["https://hoanghamobile.com/"]

    def parse(self, response):
        products = response.css('div[class="item"]')
        for product in products:
            item = {
                'name' : product.css('div a::text').get(),
                'price' : product.css('.info .price strong::text').get(),
                'url' : product.css('div a').attrib['href']
            }
            print(item)  # In ra dữ liệu đã crawl
            yield 
