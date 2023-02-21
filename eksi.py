from dataclasses import replace
import string
import requests
import argparse
import sys
from bs4 import BeautifulSoup
import cloudscraper
import datetime
import os

eksiGundem = "https://eksisozluk.com/basliklar/gundem"
eksiHome = "https://eksisozluk.com/"
test = ""

def hackLink(link):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome') 
    info = scraper.get(link).text
    soup = BeautifulSoup(info, "html.parser")
    return soup

def getArticles():
    result = []
    soup = hackLink(eksiGundem)

    articleTags = soup.find("div", id="index-section").find_all("a", href=True)
    for i in articleTags:
        result.append(i['href'])
    return result

def getParagraphs(articleLink):
    result = []
    soup = hackLink(articleLink).find("div", id="content")
    result.append(["", soup.find("h1", id="title").text.strip()])

    pageCount = int(soup.find("div", class_="pager")["data-pagecount"])    
    for i in range(pageCount):
        currentPage = hackLink(articleLink+"&p="+str(i+1)).find("div", id="topic")
        entries = currentPage.find_all("li")
        for entry in entries:
            result.append([entry["data-author"], entry.find("div", class_="content").text.strip()])
    return result
        
def writeArticle(file, paragraphs):
    for pair in paragraphs:
        file.write(pair[0] + "> " + pair[1] + "\n")

folderPath = "./Eksi-"+str(datetime.date.today());
try:
    os.makedirs(folderPath)
except:
    pass

#testArticle = getParagraphs(test)
#writeArticle(sys.stdout, testArticle)

articles = getArticles()
for article in articles:
    paragraphs = getParagraphs(eksiHome+article)
    f = open(folderPath+"/"+paragraphs[0][1]+".txt", "w")
    writeArticle(f, paragraphs)

