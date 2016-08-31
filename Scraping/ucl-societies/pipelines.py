from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scrapy import signals


class EmptyPipeline(object):
    def process_item(self, item, spider):
        if item['name']:
            # print item['name']
            return item
        else:
            raise DropItem("Empty entry")


class QuotePipeline(object):
    def process_item(self, item, spider):
        item['about'] = item['about'].encode('utf-8')
        # item['about'] = 'hi!'
        return item

class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_societies.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['name', 'president', 'email', 'url', 'facebook', 'membership', 'about',
                                          'date_established']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
