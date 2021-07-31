# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PgcPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        def removeComma(text):
            text = text.replace(',', '')

            return text

        if adapter.get('alokasi'):
            item['alokasi'] = removeComma(item['alokasi'][0])
        else:
            item['alokasi'] = 0

        '''
        if adapter.get('realisasi'):
            item['realisasi'] = removeComma(item['realisasi'][0])
        else:
            item['realisasi'] = 0

        if adapter.get('nominal'):
            item['nominal'] = removeComma(item['nominal'][0])
        else:
            item['nominal'] = 0
        '''

        return item
