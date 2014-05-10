# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DaftItem(Item):
    property_id = Field()
    url = Field()
    address = Field()
    lat = Field()
    lng = Field()
    show_area = Field()
    property_type = Field()
    floor_area = Field()
    price = Field()
    beds = Field()
    baths = Field()
    description = Field()
    first_listed = Field()
    ber_rating = Field()
    energy_performance_indicator = Field()
