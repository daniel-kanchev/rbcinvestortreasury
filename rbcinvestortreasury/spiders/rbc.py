import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from rbcinvestortreasury.items import Article


class RbcSpider(scrapy.Spider):
    name = 'rbc'
    start_urls = ['https://www.rbcits.com/en/who-we-are/media/press-releases.page']

    def parse(self, response):
        links = response.xpath('//div[@class="news-item"]//h3/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="content"]//h1/text()').get().strip()
        date = response.xpath('//div[@class="article-date"]/text()').get().strip()
        date = datetime.strptime(date, '%B %d, %Y')
        date = date.strftime('%Y/%m/%d')
        content = response.xpath('//div[@class="article-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
