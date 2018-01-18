import re
import scrapy
import os
import math
import random
import time
import urllib
import logging
import urllib.request
from scrapy.selector import Selector
# from Spider_ctrip.items import SpiderHotelCommentItem
from scrapy import Request


class HotelCommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['hotels.ctrip.com']
    start_urls = [
        'http://hotels.ctrip.com/hotel/691682.html',
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        filename = 'data/beijing_hotel_list.ids'
        self.urls = []
        with open(filename) as f:
            line = f.readline()
            while line:
                self.urls.append(line)
                line = f.readline()

    def parse(self, response):
        cur_url, cur_url_num = response.url, '691682'
        logging.info(cur_url + '\tStarting...')
        try:
            cur_url_num = re.search('hotel/(\d{1,9}).html', cur_url).groups()[0]
        except:
            pass

        filename = 'data/hotel_page/hotel-%s.html' % (cur_url_num)
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(response.body)
        filename = 'data/hotel_comment/comment-%s.json' % (cur_url_num)
        if not os.path.exists(filename):
            try:
                sel = Selector(response)
                total_page = sel.css('.c_page_list a').xpath('@value').extract()[-1]
                pages = [i + 2 for i in range(int(total_page) - 1)]
                random.shuffle(pages)
            except:
                pages = []

            results, record = [], self.handle_ajax(response)
            while len(pages) > 1:
                cur_page = pages.pop(0)
                time.sleep(random.randint(5, 7))
                logging.info(cur_url_num + '\thandling page: ' + str(cur_page))
                try:
                    result = self.request_info(cur_page, cur_url_num, record)
                except:
                    time.sleep(80)
                    logging.info('sleeping for 80 seconds.')
                    pages.append(cur_page)
                    continue

                if result.startswith("<div class='detail_cmt_box'>"):
                    results.append(result)
                    logging.info(cur_url_num + '\tsuccessful ' + str(len(pages)))
                else:
                    pages.append(cur_page)
                    logging.info(cur_url_num + '\terror ' + str(len(pages)))

            if results != []:
                with open(filename, 'a') as f:
                    for item in results:
                        f.write(item + '\n')

        logging.info(cur_url + '\tEnding...')

        n = self.urls.pop(0)[:-1]
        new_url = 'http://hotels.ctrip.com/hotel/' + str(n) + '.html'
        logging.info(new_url)
        yield Request(new_url, callback=self.parse)

    def handle_ajax(self, response):
        result = response.body.decode('utf-8')
        result = result.split('\n')
        res, record = '', ''
        for line in result:
            if line.lstrip().startswith('ajaxCommentList'):
                res = line
                break
        if res == '':
            return 'over'

        match1 = re.search('(RecordCount.*)\',', res)
        if match1:
            record = match1.groups()[0]
        else:
            return 'over'
        return record

    def eleven(self, response1):
        match = re.search('return res}\((.*),function\(it.*fromCharCode\(item-([0-9]{1,7})\)', response1)
        if match:
            num = match.groups()[1]
            num_arr = match.groups()[0]
        else:
            return 'error'
        result1 = "".join(map(lambda item: chr(int(item) - int(num)), eval(num_arr)))  # 翻译为字母组合
        # result1 = result1[:15] + 'document = []; window = [];' + result1[15:]
        result1 = re.sub('= \[32769,26495,32473,23567,', '== [32769,26495,32473,23567,', result1)
        result1 = re.sub('CAS[a-zA-Z]{15}\(new Function\(\'return \"\' \+', 'console.log(', result1)
        result1 = re.sub('\+ \'\";\'\)\);', ');phantom.exit();', result1)
        # result1 = result1.replace('new Image();', 'var tt = 0;')
        match2 = re.search(r'(\"\/hotel\/.{4,8}\.html\")', result1)
        if match2:
            result1 = result1.replace('window.location.href', match2.groups()[0])
        else:
            return 'error'
        # print(result1)
        with open('data/runjs.js', 'w') as f:  # 写入文件中
            f.write(result1)

        # os.system('phantomjs runjs.js >> tt')  # 执行文件
        # with open('tt') as f:
        #     result1 = f.readline()
        # print(result1)

        result1 = os.popen('phantomjs data/runjs.js').read()  # 执行文件

        # print("popen", result1)

        return result1[:-1]

    def callran(self, t):
        arr = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
               "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        cal = "CAS"
        for i in range(t):
            ran = math.ceil(51 * random.random())
            cal += arr[ran]
        return cal

    def request_eleven(self, hotel):
        url = "http://hotels.ctrip.com/domestic/cas/oceanball?callback=" + self.callran(15) + "&_=" + \
              str(int(time.time() * 1000))
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "hotels.ctrip.com",
            "Referer": "http://hotels.ctrip.com/hotel/" + str(hotel) + ".html",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/63.0.3239.132 Safari/537.36"
        }
        req = urllib.request.Request(url, None, headers)
        response1 = urllib.request.urlopen(req)
        page_source = response1.read()

        # print(url)
        # print(page_source.decode('utf-8'))

        return page_source.decode('utf-8')

    def request_info(self, page, hotel, record):
        response1 = self.eleven(self.request_eleven(hotel))
        if response1 == 'error' or re.search('([g-zA-Z<>:?!])', response1):
            return 'error'
        # print(response1)
        url = "http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=" + str(
            hotel) + "&hotel=" + \
              str(hotel) + "&NewOpenCount=0&AutoExpiredCount=0&" + \
              str(
                  record) + "&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=2&currentPage=" + \
              str(page) + "&viewVersion=c&contyped=0&eleven=" + response1 + "&callback=" + self.callran(14) + "&_=" + \
              str(int(time.time() * 1000))
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Host": "hotels.ctrip.com",
            "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
            "Referer": "http://hotels.ctrip.com/hotel/" + str(hotel) + ".html",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/63.0.3239.132 Safari/537.36",
        }
        req = urllib.request.Request(url, None, headers)
        response1 = urllib.request.urlopen(req)
        page_source = response1.read()

        # print(url)
        # print(page_source.decode('utf-8'))

        return page_source.decode('utf-8')
