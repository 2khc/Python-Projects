from scrapy import Request

from scrapy.spider import Spider
from ..items import Society
from scrapy.loader import ItemLoader
from ..itemloaders import SocietyLoader


class UclSpider(Spider):
    name = "ucl"
    allowed_domains = ["uclu.org"]
    start_urls = [
        "http://uclu.org/clubs-societies/directory"
    ]

    def parse(self, response):
        items = []

        for sel in response.xpath('//div[@class="view-content"]/div'):

            href = sel.xpath('article/header/h2/a/@href')

            request = None

            if href:
                url = response.urljoin(href[0].extract())
                request = Request(url, callback=self.parse_society_page)
                # request.meta['item'] = item

            yield request

        next = response.xpath('//li[@class="pager-next"]/a/@href')
        if next:
            url = response.urljoin(next[0].extract())
            yield Request(url, self.parse)
            print "Next page exists."
        else:
            print "Reached the final page."

            # def parse_next_page(self, response):

    def parse_society_page(self, response):
        loader = SocietyLoader(item=Society(), response=response)
        loader.add_xpath('name', '//h1[@id="page-title"]')

        loader.add_xpath('about',
                         '//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]/div/div/descendant-or-self::text()')
        loader.add_xpath('membership',
                         '//div[@class="field field-name-commerce-price field-type-commerce-price field-label-hidden"]/div/div/text()')
        loader.add_xpath('facebook',
                         '//article/div/div[@class="field field-name-field-facebook-group field-type-link-field field-label-hidden"]/div/div/a/@href')
        loader.add_xpath('date_established',
                         '//div[@class="field field-name-field-club-established field-type-datetime field-label-inline"]/div/div/span/text()')
        loader.add_xpath('president', '//li[@class="first last"]/span[2]/text()')
        loader.add_xpath('email', '//div[@class="uclu-societies-mail"]/a/text()')
        return loader.load_item()
