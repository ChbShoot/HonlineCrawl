import scrapy


class HonlineItem(scrapy.Item):
    post_link = scrapy.Field()
    post_time = scrapy.Field()
    key = scrapy.Field()
    pass
