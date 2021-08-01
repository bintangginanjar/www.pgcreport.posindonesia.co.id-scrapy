# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join


class AlokasiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    program = Field()
    nopend = Field()
    kprk = Field()
    alokasi = Field()    

    pass


class RealisasiItem(scrapy.Item):
    program = Field()
    nopend = Field()
    kprk = Field()    
    tanggal = Field()
    realisasi = Field()
    nominal = Field()

    pass