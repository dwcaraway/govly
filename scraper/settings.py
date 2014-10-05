# Scrapy settings for Vitals project
BOT_NAME = 'dayton-healthcheck'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'dayton-healthcheck'

ITEM_PIPELINES = {
    'scraper.pipelines.DatabasePipeline': 1000
}

#LOG_FILE='scrapy.log'
LOG_LEVEL='WARNING'

#Feed output
FEED_URI = './scrapeddata/scraped_business.json'
FEED_FORMAT = 'json'

STATS_ENABLED = True
