from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from daft.items import DaftItem

import re


def clean_url(url):
    """
    Sometimes there are multiple offset parameters in the query string.
    We set them all to be whatever the max offset is.
    """

    if url.count('offset') < 2:
        return url

    else:
        pattern = "offset=(\d+)"
        offsets = re.findall(pattern, url)
        offset_numbers = map(int, offsets)
        max_offset = max(offset_numbers)
        new_url = re.sub(pattern, "offset=%d" % max_offset, url)
        return new_url


class DaftSpider(CrawlSpider):
    name = "daft"
    allowed_domains = ["daft.ie"]
    start_urls = [
        # "http://www.daft.ie/searchsale.daft?search=1"
        # "http://www.daft.ie/searchcommercial.daft?search=1"
        "http://www.daft.ie/searchrental.daft?search=1"
        ]
    rules = (
        Rule(SgmlLinkExtractor(allow=("sales/.*/\d+/$")),
             callback="parse_item"),
        Rule(SgmlLinkExtractor(allow=("lettings/.*/\d+/$")),
             callback="parse_item"),
        Rule(SgmlLinkExtractor(allow=("search[a-z]+\.daft\?id=\d+")),
             callback="parse_item"),
        Rule(SgmlLinkExtractor(restrict_xpaths=("//li[@class='next_page']"),
             process_value=clean_url)),
        )

    def parse_item(self, response):

        sel = Selector(response)

        item = DaftItem()

        item['address'] = sel.xpath("//title/text()").extract()[0].split("-")[0].strip()
        item['price'] = sel.xpath("//div[@id='smi-price-string']/text()").extract()[0].strip()

        # Location
        item['lat'] = float(sel.xpath("//script").re('latitude":"(\d+\.\d+)')[0])
        item['lng'] = float(sel.xpath("//script").re('longitude":"([-]*\d+\.\d+)')[0])
        item['show_area'] = sel.xpath("//script").re('showArea":(\w+),')[0]

        # BER
        ber_icon = sel.xpath("//span[@class='ber-icon']/@id")
        if ber_icon:
            item['ber_rating'] = ber_icon.extract()[0].split("-")[1]

        # Beds/baths
        header_text = sel.xpath('//span[@class="header_text"]/text()')
        if header_text:
            item['property_type'] = header_text[0].extract().strip()
            if header_text.re(r'(\d+) Beds'):
                item['beds'] = int(header_text.re(r'(\d+) Beds')[0])
            if header_text.re(r'(\d+) Baths'):
                item['baths'] = int(header_text.re(r'(\d+) Baths')[0])

        # Floor area
        if sel.xpath('//div[@class="description_block"]').re(r'(\d+) Sq. Metres'):
            item['floor_area'] = float(sel.xpath('//div[@class="description_block"]').re(r'(\d+) Sq. Metres')[0])

        # Property description
        item['description'] = "".join(sel.xpath('//div[@id="description"]/text()').extract())

        # kWh
        description_extras = sel.xpath("//div[@class='description_extras']")
        item['first_listed'] = description_extras.re(r'\d{1,2}/\d{1,2}/\d{4}')[0]
        if description_extras.re(r'(\d+\.\d*) kWh'):
            item['energy_performance_indicator'] = float(description_extras.re(r'(\d+\.\d*) kWh')[0])

        item['url'] = response.url
        if "=" in item['url']:
            item['property_id'] = int(item['url'].split("=")[1])
        else:
            item['property_id'] = int(item['url'].split("/")[-2])

        return item
