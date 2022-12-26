from bs4 import BeautifulSoup
import requests
import requests
from bs4 import BeautifulSoup
import json
url = "https://quizlet.com/2335790/top-50-drugs-flash-cards/"


def parseQuizlet(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    allWords = soup.findAll('span', class_="TermText")
    totalWords = []
    for i in allWords:
        totalWords.append(i.text)
    return(totalWords)


