# Scrapy settings for daytonlocal project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dayton-healthcheck'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'dayton-healthcheck'

FEED_URI = 'feed.json'
FEED_FORMAT = 'json'

#ITEM_PIPELINES
