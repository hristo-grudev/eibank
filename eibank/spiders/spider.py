import scrapy

from scrapy.loader import ItemLoader

from ..items import EibankItem
from itemloaders.processors import TakeFirst


class EibankSpider(scrapy.Spider):
	name = 'eibank'
	start_urls = ['https://www.eibank.com/media-centre']

	def parse(self, response):
		post_links = response.xpath('//article')
		for post in post_links:
			url = post.xpath('./a/@href').get()
			date = post.xpath('./span/text()').get()
			title = post.xpath('./p/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		description = response.xpath('//div[@class="col-md-12"]//text()[normalize-space() and not(ancestor::div[@class="pr-header"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=EibankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
