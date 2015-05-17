
BOT_NAME = 'Honline'

SPIDER_MODULES = ['Honline.spiders']
USER_AGENT = 'chovy (+http://chbshoot.me/)'
MAIL_KEY = True
MAIL_HOST = 'smtp.gmail.com'
MAIL_USER = ''
MAIL_PASS = ''
MAIL_PORT = 587
MAIL_LIST = [
	'some@email.com'
]
EXTENSIONS = {
    'Honline.extensions.MailKey' : 80
}
ITEM_PIPELINES = {
        'Honline.pipelines.HonlineCheckPipeline' : 300,
        'Honline.pipelines.HonlineInsertPipeline' : 500,
}