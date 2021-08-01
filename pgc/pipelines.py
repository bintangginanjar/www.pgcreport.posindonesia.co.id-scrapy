# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pgc.items import AlokasiItem, RealisasiItem


class PgcPipeline:
    def removeComma(self, text):
        text = text.replace(',', '')

        return text

    def process_item(self, item, spider):
        if isinstance(item, AlokasiItem):
            return self.processAlokasiItem(item, spider)

        if isinstance(item, RealisasiItem):
            return self.processRealisasiItem(item, spider)

    def processAlokasiItem(self, item, spidr):
        adapter = ItemAdapter(item)

        if adapter.get('alokasi'):
            item['alokasi'] = self.removeComma(item['alokasi'][0])
        else:
            item['alokasi'] = 0

        return item

    def processRealisasiItem(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('realisasi'):
            item['realisasi'] = self.removeComma(item['realisasi'][0])
        else:
            item['realisasi'] = 0

        return item
