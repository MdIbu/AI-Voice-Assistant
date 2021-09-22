import webbrowser

import pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()
engine = pyttsx3.init() # Windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-10)
def website_open():
    iput= input("open facebook.com")
    query=(str(iput))
    indx = query.split().index('open')
    quer = query.split()[indx + 1:]
    print(quer)
    webbrowser.open("https://www." + '+'.join(quer))

  
from urllib.request import urlopen
from bs4 import BeautifulSoup 


def news():
    """
    This method will tells top 15 current NEWS
    :return: list / bool
    """
    try:
        news_url = "https://news.google.com/news/rss"
        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()
        soup_page = BeautifulSoup(xml_page, "xml")
        news_list = soup_page.findAll("item")
        li = []
        for news in news_list[:5]:
            li.append(str(news.title.text.encode('utf-8'))[1:])
        return li
    except Exception as e:
        print(e)
        return False
#newsp=news()
#print(newsp)
#speak(newsp)
import wolframalpha
def wa(input):
    app_id = "9HRE5G-Y4V6Q43P6K"
    client = wolframalpha.Client(app_id)
    indx = input.lower().split().index('calculate')
    query = input.split()[indx + 1:]
    res = client.query(' '.join(query))
    try:
        wa_result = next(res.results).text
        answer = wa_result
    except Exception as e:
        answer = "No results"
    return

def wa2(input):
    app_id = "9HRE5G-Y4V6Q43P6K"
    client = wolframalpha.Client(app_id)
    indx = input.lower().split().index('is')
    query = input.split()[indx + 1:]
    res = client.query(' '.join(query))
    try:
        wa_result = next(res.results).text
        answer = wa_result
    except Exception as e:
        answer = "No results"
    return
import webbrowser
query="open fb.com"
def open_website(query):
    
    if "open" in query and ".com" in query:
        input = query
        indx = input.lower().split().index('open')
        query = input.split()[indx + 1:]
        res = ("http://www." + "+".join(query))
        print (res)
        webbrowser.open(res)
        answer=("Opening website")
open_website(query)