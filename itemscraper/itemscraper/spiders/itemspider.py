import scrapy


class ItemspiderSpider(scrapy.Spider):
    name = "itemspider"
    allowed_domains = ["hoanghamobile.com"]
    start_urls = ["https://hoanghamobile.com/"]

    def parse(self, response):
        # Crawl menu chính
        menu_items = response.css('nav ul.root li')
        for item in menu_items:
            menu_name = item.css('a span::text').get()
            menu_url = item.css('a::attr(href)').get()
            item_url = 'https://hoanghamobile.com' + menu_url
            yield response.follow(item_url, callback=self.parse_item_page, meta={'menu_name': menu_name})

    def parse_item_page(self, response):
        menu_name = response.meta.get('menu_name')

        # Tìm tất cả các sản phẩm
        products = response.css('.v5-list .v5-grid-items .v5-item')
        for product in products:
            # Lấy URL tương đối của sản phẩm
            relative_url = product.css('h3 a ::attr(href)').get()

            # Tạo URL đầy đủ cho sản phẩm
            product_url = 'https://hoanghamobile.com' + relative_url 
            # Follow URL sản phẩm và gọi hàm parse_product_page để xử lý
            yield response.follow(product_url, callback=self.parse_product_page, meta={'menu_name': menu_name})

        # Xử lý pagination nếu có trang tiếp theo
        next_page = response.css('div.v5-more-product a ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://hoanghamobile.com' + next_page 
            yield response.follow(next_page_url, callback=self.parse, meta={'menu_name': menu_name})
    
    
    def parse_product_page(self, response):
        menu_name = response.meta.get('menu_name')

        # Lấy thông số kỹ thuật của sản phẩm
        tables = response.css('.box-technical-specifications .box-specs-content ul li:nth-child(odd)')
        
        specs = {}
        for table in tables:
            spec_name = table.css('strong::text').get()
            spec_value = table.css('span::text').get()

            if spec_name and spec_value:
                specs[spec_name.strip()] = spec_value.strip()

        yield {
            'url': response.url,
            'title': response.css('body .product-detail .box-header .header-name h1::text').get(),
            'price': response.css('.detail-info-right .box-price strong::text').get().strip(),
            'category': menu_name,
            'specs': specs
        }


