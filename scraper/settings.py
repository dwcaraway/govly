# Scrapy settings for Vitals project
BOT_NAME = 'fedvitals'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'fedvitals'

ITEM_PIPELINES = {
    #'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    'scraper.pipelines.PhoneNormalizationPipeline':5,
    'scraper.pipelines.DatabasePipeline': 1000
}

#Image Download Support
IMAGES_STORE = './scrapeddata/images'
IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}

#LOG_FILE='scrapy.log'
LOG_LEVEL='WARNING'

#Feed output
#FEED_URI = './scrapeddata/scraped_business.json'
#FEED_FORMAT = 'json'

LOG_ENABLED=True
LOG_LEVEL='WARNING'
LOG_FILE='./scrapeddata/scrapy.log'
