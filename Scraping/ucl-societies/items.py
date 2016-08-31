from scrapy.item import Item, Field


class Website(Item):
    name = Field()
    description = Field()
    url = Field()


class Society(Item):
    name = Field()
    about = Field()
    facebook = Field()
    membership = Field()
    date_established = Field()
    president = Field()
    email = Field()
