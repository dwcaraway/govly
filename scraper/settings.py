# Scrapy settings for Vitals project
BOT_NAME = 'dayton-healthcheck'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'dayton-healthcheck'

ITEM_PIPELINES = {
    'scraper.pipelines.DaytonLocalPipeline':300,
    'scraper.pipelines.DatabaseOutputPipeline': 1000
}
