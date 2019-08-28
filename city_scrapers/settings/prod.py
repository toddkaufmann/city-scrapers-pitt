from .base import *

USER_AGENT = "City Scrapers [production mode]. Learn more and say hello at https://citybureau.org/city-scrapers"

# Uncomment one of the following DiffPipeline classes to enable a diff pipeline class that will
# deduplicate JSCalendar UIDs based on City Scrapers IDs and list any meetings in the future which
# no longer appear in scraped results as cancelled.

# Configure item pipelines
ITEM_PIPELINES = {
    "city_scrapers.pipelines.MigrationPipeline": 50,
    "city_scrapers_core.pipelines.DefaultValuesPipeline": 100,
    "city_scrapers_core.pipelines.S3DiffPipeline": 200,
    "city_scrapers_core.pipelines.MeetingPipeline": 300,
    "city_scrapers_core.pipelines.JSCalendarPipeline": 400,
}

# Uncomment one of the StatusExtension classes to write an SVG badge of each scraper's status to
# Azure or S3 after each time it's run.

# By default, this will write to the same bucket or container as the feed export, but this can be
# configured by adding a value in the CITY_SCRAPERS_STATUS_BUCKET or CITY_SCRAPERS_STATUS_CONTAINER
# for S3 and Azure respectively.

EXTENSIONS = {
    "scrapy_sentry.extensions.Errors": 10,
    "city_scrapers_core.extensions.S3StatusExtension": 100,
    "scrapy.extensions.closespider.CloseSpider": None,
}

FEED_EXPORTERS = {
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
}

FEED_FORMAT = "jsonlines"

# Uncomment S3 or Azure to write scraper results to static file storage as newline-delimited JSON
# files made up of JSCalendar events following the meeting schema.

FEED_STORAGES = {
    "s3": "scrapy.extensions.feedexport.S3FeedStorage",
}

# Uncomment credentials for whichever provider you're using

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

CITY_SCRAPERS_STATUS_BUCKET = "city-scrapers-pitt"

# Uncomment the FEED_URI for whichever provider you're using

FEED_URI = "s3://city-scrapers-pitt/%(year)s/%(month)s/%(day)s/%(hour_min)s/%(name)s.json"
