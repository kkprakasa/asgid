import urllib2
from bs4 import BeautifulSoup
from time import sleep
import re
import csv

def tarik(url):
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36' }
    req = urllib2.Request(url, None, headers)
    dres = urllib2.urlopen(req)
    dhtml = dres.read()
    return BeautifulSoup(dhtml)

dataDict = []
x = tarik('https://id.asiangames2018.id/sport/')
for i in range(len(x.findAll('li',{'class':'or-sportshub__item'}))):
    print('memproses '+x.findAll('li',{'class':'or-sportshub__item'})[i].find('a',href=True).attrs['href'].split('/')[2])
    l=tarik('https://id.asiangames2018.id/schedule-results'+x.findAll('li',{'class':'or-sportshub__item'})[i].find('a',href=True).attrs['href'])
    for n in range(len(l.findAll('span', {'class':'dcm-dt'}))):
        print('proses no'+str(n))
        dataList = {}
        dataList['cabor'] = x.findAll('li',{'class':'or-sportshub__item'})[i].find('a',href=True).attrs['href'].split('/')[2]
        if n % 2 == 0 :
            dataList['tanggal'] = re.sub("\s","",l.findAll('span', {'class':'dcm-dt'})[n].text)
        else :
            dataList['jam'] = re.sub("\s","",l.findAll('span', {'class':'dcm-dt'})[1].text)
        dataList['kelas']= re.sub('\W','',l.findAll('span', {'class':'or-evt-phase_evt'})[0].text)
        dataList['fase'] = re.sub('\W','',l.findAll('span', {'class':'or-evt-phase_ph'})[0].text)
        dataDict.append(dataList)

keys = athletes[0].keys()
with open('AtlitAsianGames03.csv', 'wb') as o_f:
    d_w = csv.DictWriter(o_f, keys)
    d_w.writeheader()
    d_w.writerows(athletes)