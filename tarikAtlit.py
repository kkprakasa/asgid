import urllib2
from bs4 import BeautifulSoup
from time import sleep
import re
import csv

#jumlah halaman atlet 834

athletes = []
for n in range(1,835,1):
    detik = 'https://id.asiangames2018.id/athletes/page/'+str(n)+'/'
    print('halaman '+detik)
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36' }
    req = urllib2.Request(detik, None, headers)
    dres = urllib2.urlopen(req)
    dhtml = dres.read()
    dsoup = BeautifulSoup(dhtml)
    for i in range(len(dsoup.findAll('li',{'class':'or-athletes__item'}))):
        athletesdict = {}
        atlit = 'https://id.asiangames2018.id'+dsoup.findAll('li',{'class':'or-athletes__item'})[i].find('a',href=True).attrs['href']
        req = urllib2.Request(atlit, None, headers)
        try:
            dres = urllib2.urlopen(req) 
            dhtml = dres.read()
            asoup = BeautifulSoup(dhtml)
            name = asoup.find('div',{'class':'or-athlete-profile__name'}).findAll('span')[0].text
            surename = asoup.find('div',{'class':'or-athlete-profile__name'}).findAll('span')[1].text
            print('memproses '+name)
            athletesdict['nama'] = name+' '+surename
            athletesdict['negara'] = asoup.find('div',{'class':'or-athlete-profile__nationality'}).find('img').get('title')
            athletesdict['noc'] = asoup.find('div',{'class':'or-athlete-profile__nationality'}).find('span').text
            athletesdict['cabor'] = asoup.find('div',{'class':'or-athlete-profile__discipline'}).text
            athletesdict['tgll'] = asoup.find('span',{'class':'or-athlete__birth--date'}).text
            athletesdict['kotal'] = asoup.find('span',{'class':'or-athlete__birth--city'}).text if asoup.find('span',{'class':'or-athlete__birth--city'}) is not None else "NA"
            athletesdict['negl'] = re.sub('\W','',asoup.find('span',{'class':'or-athlete__birth--country'}).text) if asoup.find('span',{'class':'or-athlete__birth--country'}) is not None else "NA"
            athletesdict['tinggi'] = re.sub('\s','',asoup.findAll('div',{'class':'or-anagraphic__data'})[2].text).split('/')[0]
            athletesdict['berat'] = re.sub('\s','',asoup.findAll('div',{'class':'or-anagraphic__data'})[3].text).split('/')[0]
            athletesdict['url'] = atlit
            athletes.append(athletesdict)
        except:
            athletesdict['status'] = "error"
            athletesdict['url'] = atlit
            athletes.append(athletesdict)
            pass
keys = athletes[0].keys()
with open('AtlitAsianGames03.csv', 'wb') as o_f:
    d_w = csv.DictWriter(o_f, keys)
    d_w.writeheader()
    d_w.writerows(athletes)