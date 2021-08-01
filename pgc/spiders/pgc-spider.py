import scrapy
import string
import re
import datetime

from datetime import date, timedelta
from scrapy.loader import ItemLoader
from loginform import fill_login_form
from scrapy.http import FormRequest
from pgc.items import AlokasiItem, RealisasiItem


class PgcSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'pgc.pipelines.PgcPipeline': 100,
            # 'name.pipelines.KamusNamaDataParse': 200
        }
    }

    name = 'kprk'
    # intranet URL
    #baseUrl = 'https://pgc.posindonesia.co.id:8011/'

    # internet URL
    baseUrl = 'https://pgcreport.posindonesia.co.id:33500/'

    nippos = '973365365'
    password = 'bansos2021'
    startDate = datetime.datetime(2021, 7, 25)
    endDate = datetime.datetime(2021, 7, 31)

    def __init__(self, *args, **kwargs):
        super(PgcSpider, self).__init__(*args, **kwargs)
        self.start_urls = (self.baseUrl)

    def start_requests(self):
        self.logger.info('Start request')
        yield scrapy.Request(self.baseUrl, callback=self.parseLogin)

    def parseLogin(self, response):
        self.logger.info('Parse login')
        token = response.xpath('//*[@name="_token"]/@value').extract_first()

        yield FormRequest.from_response(response, formdata={'nippos': self.nippos, 'password': self.password}, callback=self.chooseProgram, meta={'token': token})
        # self.logger.info(response.css('body').getall())
        # data, url, method = fill_login_form(response.url, response.body, self.username, self.password)
        # return FormRequest(response.url, formdata=data, method=method, callback=self.chooseProgram)

    def chooseProgram(self, response):
        self.logger.info('Choose program')
        self.logger.info(response.meta['token'])

        formData = {'_token': response.meta['token'], 'program': 'LOG'}

        pageUrl = self.baseUrl + 'choice_program'

        yield scrapy.FormRequest(pageUrl, formdata=formData, callback=self.parsePage, dont_filter=True)

        # self.logger.info(response.css('body').getall())

    def parsePage(self, response):
        self.logger.info('Parse page')
        # self.logger.info(response.css('body').getall())
        # self.logger.info(response.url)
        for i in range(1, 3):
            # self.logger.info(i)
            targetUrl = self.baseUrl + \
                'report/alokasi?kode_wilayah=&tag_voucher=' + str(i)
            yield scrapy.Request(targetUrl, callback=self.parsePageAlokasi, meta={'program': i})

    def parsePageAlokasi(self, response):
        self.logger.info('Parse page alokasi')
        # self.logger.info(response.css('table.table').getall())
        for row in response.css('table.table > tbody > tr'):
            # detailUrl = row.xpath('').get()
            # self.logger.info(row.xpath('td[9]/a/@href').get())
            targetUrl = response.urljoin(row.xpath('td[9]/a/@href').get())
            # self.logger.info(targetUrl)
            yield scrapy.Request(targetUrl, callback=self.parseAlokasiKprk, meta={'program': response.meta['program']})

    def parseAlokasiKprk(self, response):
        self.logger.info('Parse alokasi KPRK')
        kodeReg = re.search('[0-9][0-9][0-9][0-9][0-9]',
                            response.css('h3.card-title::text').get()).group(0)        
        for row in response.css('table.table > tbody > tr'):
            # self.logger.info(kodeReg)

            loader = ItemLoader(item=AlokasiItem(), selector=row)
            if response.meta['program'] == 1:
                loader.add_value('program', 'BST')
            else:
                loader.add_value('program', 'PKH')
            nopend = row.xpath('td[2]//text()').get()
            loader.add_value('nopend', nopend)            
            kprk = row.xpath('td[3]//text()').get()
            loader.add_value('kprk', kprk)
            loader.add_xpath('alokasi', 'td[4]//text()')
            
            dt = self.startDate

            while dt <= self.endDate:                
                targetUrl = 'https://pgcreport.posindonesia.co.id:33500/report_sum/kprk/' + str(kodeReg) + '?date_1=' + \
                    dt.strftime('%m/%d/%Y') + '&date_2=' + dt.strftime('%m/%d/%Y') + \
                    '&tag_voucher=' + str(response.meta['program'])
                yield response.follow(targetUrl, self.parseRealisasi, meta={
                    'program': response.meta['program'],
                    'nopend': nopend,
                    'kprk': kprk,
                    'tanggal': dt.strftime('%d-%m-%Y')
                })

                dt = dt + datetime.timedelta(days=1)

            yield loader.load_item()

    def parseRealisasi(self, response):
        self.logger.info('Parse page realisasi')
        # self.logger.info(response.url)

        #alokasiItem = response.meta['alokasiItem']

        for row in response.css('table.table > tbody > tr'):
            loader = ItemLoader(item=RealisasiItem(), selector=row)
            if response.meta['program'] == 1:
                loader.add_value('program', 'BST')
            else:
                loader.add_value('program', 'PKH')
            loader.add_value('nopend', response.meta['nopend'])
            loader.add_value('kprk', response.meta['kprk'])
            loader.add_value('tanggal', response.meta['tanggal'])
            loader.add_xpath('realisasi', 'td[4]//text()')

            yield loader.load_item()
