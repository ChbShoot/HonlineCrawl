import scrapy
from scrapy.mail import MailSender
from Honline.items import HonlineItem

class CheeseSpider(scrapy.Spider):
    name = "klyuchi"
    allowed_domains = ["m.vk.com"]
    start_urls = [ "http://m.vk.com/halo.online" ]


    def parse(self, response):
        items = [ ]
        mailer = MailSender.from_settings(self.settings)
        sel = scrapy.Selector(response)
        posts = sel.xpath('//div [@class="wall_item"]')
        for post in posts:
            item = HonlineItem()
            #AUTHOR = post.xpath('.//div[1]//div[1]//div[1]//a[1]/text()').extract() #wi_head/wi_cont/wi_author/a
            item['post_link'] = str(post.xpath('.//div[1]//div[1]//div[2]//a[1]/@href').extract()[0])
            item['post_time'] = str(post.xpath('.//div[1]//div[1]//div[2]//a[1]/text()').extract()[0])
            item['key'] = (post.re('\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d')) #" 289276165354594 "

            if len(item['key']) > 0:
                item['key'] = str(item['key'][0])
                items.append(item)
        return items