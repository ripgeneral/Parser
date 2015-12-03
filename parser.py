# -*- coding: utf-8 -*-
#!/usr/bin/env python3


import urllib.request , os ,sys ,pprint ,json,datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pymongo import MongoClient

client = MongoClient('172.16.0.154',27017)
db = client.test

def getPage(url):
    response =  urllib.request.urlopen(url)
    return response.read().decode('cp1251')

def parse(html):
    soup = BeautifulSoup(html, "html5lib")
    table = soup.find('div',{"class":"projects"})
    rows = table.find_all('div',{'class':'proj'})
    projects = []
    for row in rows:
        db.test.insert({
            'link':'https://freelance.ru'+row.find("a").get('href'),
            'date':datetime.datetime.strptime((row.find('li',{'class':'pdata'}).text).replace("Поднято ",""),'%d.%m.%y'),
            'applications':row.find('i').text,
            'desc':row.find('a',{'class':'descr'}).span.nextSibling.text,
            'price':row.find('span',{'class':'cost'}).text,
            'title':row.find('a',{'class':'ptitle'}).text,
            #Stealing id from freelance
            'id':(urlparse(row.find("a").get('href')).path)[-11:-5]
        })
        #break
    return projects

def checkPagesCount(html):
    soup = BeautifulSoup(html, "html5lib")
    pagination = soup.find('ul',{'class':'pagination'})
    lst = pagination.find_all('li')
    li = []
    for x in lst:
        li.append(x)
    return int(li[len(li)-2].text)

def save(projects,path):
    # Экспорт в csv
    # with open(path,'a', encoding='utf-8') as csvfile:
    #     for project in projects:
    #         writer.writerow((project['id'],project['title'],project['price'],project['desc'],project['date'],project['applications'],project['link'],))

    #Экспорт в json
    with open(path,'a') as jsonf:
        json.dump(projects,jsonf)


def parsePage(url):
    page= getPage(url)
    totalPages = checkPagesCount(page)
    out= []
    # save(("'id','Project','Price','Desc','Date','Applications','Link'"),'output.csv')
    for i in range(1,totalPages+1):
        out += parse(getPage('https://freelance.ru/projects/?page=' + str(i)))
        #if i>2:
        #    break
        print("Processed %d out of  %s" % (i,totalPages))
        break
        # save(out,'json.txt')




def main():
    parsePage("https://freelance.ru/projects")

if __name__=="__main__":
    main()

# https://freelance.ru/projects/sistema-elektrosnabzheniya-stadiona-na-45000-zritelskih-mest-583842.html