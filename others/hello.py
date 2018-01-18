from urllib2 import urlopen
import urlparse
import bs4
import csv

BASE_URL = "http://http://nba.hupu.com/"
PLAYER_LIST_QUERY = "/playerSearch.aspx?lega=%s&pn=%d"
league = ['epl','seri','bund','liga','fran','scot','holl','belg']
page_number_limit = 100
player_fields = ['league_cn','img','name_cn','name','team','age','position_cn','nation','birth','query','id','teamid','league']
def get_players(baseurl):
    html = urlopen(baseurl).read()
    soup = bs4.BeautifulSoup(html, "lxml")
    players = [ dd for dd in soup.select('.searchResult tr') if dd.contents[1].name != 'th']
    result = []
    for player in players:
        record = []
        link = ''
        query = []
        for item in player.contents:
            if type(item) is bs4.element.Tag:
                if not item.string and item.img:
                    record.append(item.img['src'])
                else :
                    record.append(item.string and item.string.strip() or 'na')
                try:
                    o = urlparse.urlparse(item.a['href']).query
                    if len(link) == 0:
                        link = o
                        query = dict([(k,v[0]) for k,v in urlparse.parse_qs(o).items()])
                except:
                    pass

        if len(record) != 10:
            for i in range(0, 10 - len(record)):
                record.append('na')
        record.append(unicode(link,'utf-8'))
        record.append(unicode(query["id"],'utf-8'))
        record.append(unicode(query["teamid"],'utf-8'))
        record.append(unicode(query["lega"],'utf-8'))
        result.append(record)
    return result

def write_csv(filename, content, header = None):
    file = open(filename, "wb")
    file.write('\xEF\xBB\xBF')
    writer = csv.writer(file, delimiter=',')
    if header:
        writer.writerow(header)
    for row in content:
        encoderow = [dd.encode('utf8') for dd in row]
        writer.writerow(encoderow)

result = []
for url in [ BASE_URL + PLAYER_LIST_QUERY % (l,n) for l in league for n in range(page_number_limit) ]:
    result = result +  get_players(url)

write_csv('players.csv',result,player_fields)
