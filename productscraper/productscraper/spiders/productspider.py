import scrapy

class ProductSpider(scrapy.Spider):
    name = "productspider"
    allowed_domains = ["hoanghamobile.com"]
    start_urls = ["https://hoanghamobile.com/dien-thoai-di-dong"]

    def parse(self, response):
        # Tìm tất cả các sản phẩm
        products = response.css('.v5-list .v5-grid-items .v5-item')
        for product in products:
            # Lấy URL tương đối của sản phẩm
            relative_url = product.css('h3 a ::attr(href)').get()

            # Tạo URL đầy đủ cho sản phẩm
            product_url = 'https://hoanghamobile.com' + relative_url 
            # Follow URL sản phẩm và gọi hàm parse_product_page để xử lý
            yield response.follow(product_url, callback=self.parse_product_page)

        # Xử lý pagination nếu có trang tiếp theo
        next_page = response.css('div.v5-more-product a ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://hoanghamobile.com' + next_page 
            yield response.follow(next_page_url, callback=self.parse)


    def parse_product_page(self, response):
        # Lấy tiêu đề và các thông tin khác từ trang sản phẩm
        yield {
            'url': response.url,
            'title': response.css('body .product-detail .box-header .header-name h1::text').get(),
            'price': response.css('.product-summary .box-price .price ::text').get(),
            'camera_resolution': response.xpath('//strong[contains(text(),"Độ phân giải camera")]/following-sibling::span//text()').getall(),
            'operating_system': response.xpath('//strong[contains(text(),"Hệ điều hành")]/following-sibling::span//text()').get(),
            'internal_memory': response.xpath('//strong[contains(text(),"Bộ nhớ trong")]/following-sibling::span//text()').get(),
            'battery_capacity': response.xpath('//strong[contains(text(),"Dung lượng pin sản phẩm")]/following-sibling::span//text()').get(),
            'screen_technology': response.xpath('//strong[contains(text(),"Công nghệ màn hình")]/following-sibling::span//text()').get(),
            'screen_resolution': response.xpath('//strong[contains(text(),"Độ phân giải")]/following-sibling::span//text()').getall(),
            'processor': response.xpath('//strong[contains(text(),"Vi xử lý")]/following-sibling::span//text()').get(),
            'category' : response.xpath('//ol[@class="breadcrumb"]/li[3]//a/span[@itemprop="name"]/text()').get(),
            'description' : response.xpath('//div[@class="product-content-text box-content-text"]//p//text()').getall()
        }
