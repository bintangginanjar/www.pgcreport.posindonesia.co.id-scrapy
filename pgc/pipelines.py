# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import logging

from sqlalchemy.orm import sessionmaker
from itemadapter import ItemAdapter
from pgc.items import AlokasiItem, RealisasiItem
from pgc.models import dbConnect, createTable, Alokasi, Realisasi


class PgcPipeline:
    def removeComma(self, text):
        text = text.replace(',', '')

        return text

    def __init__(self):
        logging.info("****Data saving****")

        # Initializes database connection and sessionmaker
        engine = dbConnect()
        # Creates table
        createTable(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("****Database connected****")

    def process_item(self, item, spider):
        if isinstance(item, AlokasiItem):
            return self.processAlokasiItem(item, spider)

        if isinstance(item, RealisasiItem):
            return self.processRealisasiItem(item, spider)

    def processAlokasiItem(self, item, spidr):
        adapter = ItemAdapter(item)
        session = self.Session()

        if adapter.get('alokasi'):
            item['alokasi'] = self.removeComma(item['alokasi'][0])
        else:
            item['alokasi'] = 0

        tbAlokasi = Alokasi()
        tbAlokasi.program = item['program'][0]
        tbAlokasi.nopend = item['nopend'][0]
        tbAlokasi.kprk = item['kprk'][0]
        tbAlokasi.alokasi = item['alokasi']
        #tbAlokasi.tanggalReport = datetime.datetime.now().strftime('%m-%d-%Y')

        try:
            session.add(tbAlokasi)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

    def processRealisasiItem(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('realisasi'):
            item['realisasi'] = self.removeComma(item['realisasi'][0])
        else:
            item['realisasi'] = 0

        tbRealisasi = Realisasi()

        return item
