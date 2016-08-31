# Scrapy settings for dirbot project

SPIDER_MODULES = ['ucl-societies.spiders']
NEWSPIDER_MODULE = 'ucl-societies.spiders'
DEFAULT_ITEM_CLASS = 'ucl-societies.items.Website'

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True

ITEM_PIPELINES = {
    'ucl-societies.pipelines.EmptyPipeline': 2,
    'ucl-societies.pipelines.QuotePipeline': 10,
    'ucl-societies.pipelines.CsvExportPipeline': 25
}

