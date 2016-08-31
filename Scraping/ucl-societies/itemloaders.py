from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
import unicodedata


class SocietyLoader(ItemLoader):
    default_output_processor = TakeFirst()

    name_in = MapCompose(remove_tags)
    name_out = Join()

    membership_in = MapCompose(lambda x: x.replace(u'\xa3', ''))
    membership_out = Join()

    about_in = MapCompose(lambda x: x.replace(u'\xa0', u' '), unicode.strip)
    about_out = Join()

    # facebook_in = MapCompose()
    # facebook_out = Join()

    # date_established_in = MapCompose()
    # date_established_out = Join()

    # president_in = MapCompose()
    # president_out = Join()

    # email_in = MapCompose()
    # email_out = Join()
