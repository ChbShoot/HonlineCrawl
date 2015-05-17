from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender

class MailKey(object):
    def __init__(self, recipients, mail, crawler):
        self.keys = [ ]
        self.num_keys = 0
        self.recipients = recipients
        self.mail = mail
    @classmethod
    def from_crawler(cls, crawler):
        recipients = crawler.settings.getlist('MAIL_LIST')
        if not crawler.settings.getbool('MAIL_KEY'):
            raise NotConfigured

        mail = MailSender.from_settings(crawler.settings)
        instance = cls(recipients, mail, crawler)

        crawler.signals.connect(instance.item_scraped, signal=signals.item_scraped)
        #crawler.signals.connect(instance.spider_error, signal=signals.spider_error)
        crawler.signals.connect(instance.spider_closed, signal=signals.spider_closed)

        return instance
    def item_scraped(self, item, response, spider):
        self.keys.append(item)
        self.num_keys += 1

    def spider_closed(self, spider, reason):
        if self.num_keys == 0:
            return
        body = '''Found {0} keys!'''.format(self.num_keys)
        for key in self.keys:
            body += ''' \n http://vk.com/{0}
                        Post time: {1}
                        Key:
                                    {2}'''.format(key['post_link'], key['post_time'], key['key'])
        return self.mail.send(
            to=self.recipients,
            subject="We got Keys!",
            body = body)