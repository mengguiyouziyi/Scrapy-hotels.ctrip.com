import random
import time
import json
import scrapy
import requests
from scrapy.selector import Selector


# 目前爬去的只是北京的所有酒店的 id map
class HotellistSpider(scrapy.Spider):
    name = 'hotel_list'
    print('starting...')

    start_urls = [
        'http://hotels.ctrip.com/hotel/beijing1',
    ]

    def parse(self, response):
        sel = Selector(response)
        total_page = sel.css('.c_page_list a').xpath('@data-value').extract()[-1]
        page_nums = [i+2 for i in range(int(total_page) - 50)]                      # 减少10页
        random.shuffle(page_nums)

        url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
        head = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "1729",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "hotels.ctrip.com",
            "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
            "Origin": "http://hotels.ctrip.com",
            "Referer": "http://hotels.ctrip.com/hotel/beijing1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
        form = {
            '__VIEWSTATEGENERATOR': 'DB1FBB6D', 'cityName': '%25E5%258C%2597%25E4%25BA%25AC', 'StartTime': '2018-01-17',
            'DepTime': '2018-01-18', 'txtkeyword': '', 'Resource': '', 'Room': '', 'Paymentterm': '', 'BRev': '', 'Minstate': '',
            'PromoteType': '', 'PromoteDate': '', 'operationtype': 'NEWHOTELORDER', 'PromoteStartDate': '', 'PromoteEndDate': '',
            'OrderID': '', 'RoomNum': '', 'IsOnlyAirHotel': 'F', 'cityId': '1', 'cityPY': 'beijing', 'cityCode': '010',
            'cityLat': '39.9105329229', 'cityLng': '116.413784021', 'positionArea': '', 'positionId': '', 'hotelposition': '', 'keyword': '',
            'hotelId': '', 'htlPageView': '0', 'hotelType': 'F', 'hasPKGHotel': 'F', 'requestTravelMoney': 'F', 'isusergiftcard': 'F',
            'useFG': 'F', 'HotelEquipment': '', 'priceRange': '-2', 'hotelBrandId': '', 'promotion': 'F', 'prepay': 'F', 'IsCanReserve': 'F',
            'OrderBy': '99', 'OrderType': '', 'k1': '', 'k2': '', 'CorpPayType': '', 'viewType': '', 'checkIn': '2018-01-17',
            'checkOut': '2018-01-18', 'DealSale': '', 'ulogin': '', 'hidTestLat': '0%257C0',
            'AllHotelIds': '608345%252C375126%252C452197%252C1641390%252C1249518%252C2642089%252C691682%252C1722447%252C431617%252C436066%252C1641301%252C1725911%252C456474%252C457242%252C1563509%252C1836257%252C9627725%252C5226364%252C1251776%252C6684925%252C5389632%252C8019672%252C457112%252C9293254%252C511769',
            'psid': '', 'HideIsNoneLogin': 'T', 'isfromlist': 'T', 'ubt_price_key': 'htl_search_result_promotion', 'showwindow': '',
            'defaultcoupon': '', 'isHuaZhu': 'False', 'hotelPriceLow': '', 'htlFrom': 'hotellist', 'unBookHotelTraceCode': '',
            'showTipFlg': '',
            'hotelIds': '608345_1_1%2C375126_2_1%2C452197_3_1%2C1641390_4_1%2C1249518_5_1%2C2642089_6_1%2C691682_7_1%2C1722447_8_1%2C431617_9_1%2C436066_10_1%2C1641301_11_1%2C1725911_12_1%2C456474_13_1%2C457242_14_1%2C1563509_15_1%2C1836257_16_1%2C9627725_17_1%2C5226364_18_1%2C1251776_19_1%2C6684925_20_1%2C5389632_21_1%2C8019672_22_1%2C457112_23_1%2C9293254_24_1%2C511769_25_1',
            'markType': '0', 'zone': '', 'location': '', 'type': '', 'brand': '', 'group': '', 'feature': '', 'equip': '', 'star': '',
            'sl': '', 's': '', 'l': '', 'price': '', 'a': '0', 'keywordLat': '', 'keywordLon': '', 'contrast': '0', 'contyped': '0',
            'productcode': '',
        }
        pages_list = []
        pages_map = {}
        while len(page_nums) > 10:
            cur_page = page_nums.pop(0)
            print("downloading page: ", cur_page)
            form['page'] = str(cur_page)
            try:
                time.sleep(random.randint(6, 12))
                result = requests.post(url, data=form, headers=head)
                print('successful ', len(page_nums))
            except:
                time.sleep(60)
                page_nums.append(cur_page)
                print('error ', len(page_nums))
                continue

            try:
                pages_list.append(result.text)
                di = json.loads(result.text)
                nums = len(di['hotelPositionJSON'])
                for i in range(nums):
                    pages_map[di['hotelPositionJSON'][i]['id']] = di['hotelPositionJSON'][i]['name']
            except:
                continue

        filename1 = 'data/beijing_hotel_list.pages'
        filename2 = 'data/beijing_hotel_list.map'
        filename3 = 'data/beijing_hotel_list.ids'
        with open(filename1, 'w') as f:
            for item in pages_list:
                f.write(item + '\n')
        with open(filename2, 'w') as f:
            f.write(json.dumps(pages_map))
        with open(filename3, 'w') as f:
            for key in pages_map.keys():
                f.write(str(key) + '\n')

        print('Ending...')


# import scrapy
# from collections import OrderedDict
# from scrapy.selector import Selector
# from Spider_ctrip.items import SpiderCtripItem
#
#
# class HotellistSpider(scrapy.Spider):
#     name = 'hotel_list'
#     print('starting....')
#     #
#     # start_urls = [
#     #     'http://hotels.ctrip.com/hotel/beijing1#ctm_ref=hod_hp_sb_lst',
#     # ]
#     #
#     # def parse(self, response):
#     #     # page = response.url.split("/")[-2]
#     #     # filename = 'dafang-%s.html' % page
#     #     # with open(filename, 'wb') as f:
#     #     #     f.write(response.body)
#     #     # result = response.body.decode('utf-8')
#     #
#     #     sel = Selector(response)
#     #     # temp_id = sel.css('.hotel_new_list').xpath('@id').extract()
#     #     temp_name = sel.css('.hotel_item_pic')
#     #     items = []
#     #     for index, item in enumerate(temp_name):
#     #         it = SpiderCtripItem()
#     #         it['hotel_id'] = item.xpath('@data-hotel').extract()[0]
#     #         it['hotel_name'] = item.xpath('@title').extract()[0]
#     #         print('%s,\t%s' % (it['hotel_id'], it['hotel_name']))
#     #         items.append(it)
#     #     return items
#     #     # print(temp_name)
#
#     # start_urls = ["http://www.example.com/"]
#
#     # def start_requests(self):
#     #     url = 'http://www.renren.com/PLogin.do'
#     #
#     #     # FormRequest 是Scrapy发送POST请求的方法
#     #     yield scrapy.FormRequest(
#     #         url=url,
#     #         formdata={"email": "xxx", "password": "xxxxx"},
#     #         callback=self.parse_page
#     #     )
#     #
#     # def parse_page(self, response):
#     # # do something
#
#     # start_urls = ["http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"]
#
#     def start_requests(self):
#         url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
#
#         HEADER = {
#             "Accept": "*/*",
#             "Accept-Encoding": "gzip, deflate",
#             "Accept-Language": "zh-CN,zh;q=0.9",
#             "Cache-Control": "max-age=0",
#             "Connection": "keep-alive",
#             "Content-Length": "1729",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Host": "hotels.ctrip.com",
#             "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
#             "Origin": "http://hotels.ctrip.com",
#             "Referer": "http://hotels.ctrip.com/hotel/nanjing12",
#             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
#         }
#         FORMDATA = {'__VIEWSTATEGENERATOR':'DB1FBB6D',
#                     'cityName':'%25E5%258D%2597%25E4%25BA%25AC',
#                     'StartTime':'2018-01-25',
#                     'DepTime':'2018-01-27',
#                     'txtkeyword':'',
#                     'Resource':'',
#                     'Room':'',
#                     'Paymentterm':'',
#                     'BRev':'',
#                     'Minstate':'',
#                     'PromoteType':'',
#                     'PromoteDate':'',
#                     'operationtype':'NEWHOTELORDER',
#                     'PromoteStartDate':'',
#                     'PromoteEndDate':'',
#                     'OrderID':'',
#                     'RoomNum':'',
#                     'IsOnlyAirHotel':'F',
#                     'cityId':'12',
#                     'cityPY':'nanjing',
#                     'cityCode':'025',
#                     'cityLat':'32.0481520777',
#                     'cityLng':'118.7904455801',
#                     'positionArea':'',
#                     'positionId':'',
#                     'hotelposition':'',
#                     'keyword':'',
#                     'hotelId':'',
#                     'htlPageView':'0',
#                     'hotelType':'F',
#                     'hasPKGHotel':'F',
#                     'requestTravelMoney':'F',
#                     'isusergiftcard':'F',
#                     'useFG':'F',
#                     'HotelEquipment':'',
#                     'priceRange':'-2',
#                     'hotelBrandId':'',
#                     'promotion':'F',
#                     'prepay':'F',
#                     'IsCanReserve':'F',
#                     'OrderBy':'99',
#                     'OrderType':'',
#                     'k1':'',
#                     'k2':'',
#                     'CorpPayType':'',
#                     'viewType':'',
#                     'checkIn':'2018-01-25',
#                     'checkOut':'2018-01-27',
#                     'DealSale':'',
#                     'ulogin':'',
#                     'hidTestLat':'0%257C0',
#                     'AllHotelIds':'375288%252C670019%252C378829%252C6475650%252C6829860%252C471367%252C3327690%252C8867914%252C425945%252C754206%252C481006%252C1632876%252C710988%252C1632856%252C1632868%252C512269%252C531787%252C11932474%252C444648%252C1415920%252C2298282%252C7687802%252C5372071%252C846891%252C6473532',
#                     'psid':'',
#                     'HideIsNoneLogin':'T',
#                     'isfromlist':'T',
#                     'ubt_price_key':'htl_search_result_promotion',
#                     'showwindow':'',
#                     'defaultcoupon':'',
#                     'isHuaZhu':'False',
#                     'hotelPriceLow':'',
#                     'htlFrom':'hotellist',
#                     'unBookHotelTraceCode':'',
#                     'showTipFlg':'',
#                     'hotelIds':'375288_1_1%2C670019_2_1%2C378829_3_1%2C6475650_4_1%2C6829860_5_1%2C471367_6_1%2C3327690_7_1%2C8867914_8_1%2C425945_9_1%2C754206_10_1%2C481006_11_1%2C1632876_12_1%2C710988_13_1%2C1632856_14_1%2C1632868_15_1%2C512269_16_1%2C531787_17_1%2C11932474_18_1%2C444648_19_1%2C1415920_20_1%2C2298282_21_1%2C7687802_22_1%2C5372071_23_1%2C846891_24_1%2C6473532_25_1',
#                     'markType':'0',
#                     'zone':'',
#                     'location':'',
#                     'type':'',
#                     'brand':'',
#                     'group':'',
#                     'feature':'',
#                     'equip':'',
#                     'star':'',
#                     'sl':'',
#                     's':'',
#                     'l':'',
#                     'price':'',
#                     'a':'0',
#                     'keywordLat':'',
#                     'keywordLon':'',
#                     'contrast':'0',
#                     'page':'5',
#                     'contyped':'0',
#                     'productcode':''}
# #        FORMDATA['page'] = '9'
#         print(FORMDATA)
#         # FormRequest 是Scrapy发送POST请求的方法
#
#         yield scrapy.FormRequest(
#             url=url,
#             headers=HEADER,
#             formdata=FORMDATA,
#             callback=self.parse_page,
#         )
#
#     def parse_page(self, response):
#         print(response)
#
#         print('Ending....')
#         # value1 = response.meta["key1"]
#         # do something
#
#
