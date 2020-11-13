import datetime as dt
import requests as rq
import random as rnd
from textblob import TextBlob
from googletrans import Translator
import config

today = dt.date.today()
weekAgo = today - dt.timedelta(days = 7)
keyWord = 'intel'
apiKey = config.apiKey
url = f"http://newsapi.org/v2/everything?q={keyWord}&from={weekAgo}&sortBy=publishedAt&apiKey={apiKey}"

try:
    response = rq.get(url)
except rq.exceptions.Timeout:
    print("Timeout for your request, please try agin for a moment")
except rq.exceptions.TooManyRedirects:
    print("Probably sth is wrong with your url")
except rq.exceptions.RequestException as err:
    # print error and call sys.exit in case catastrophic error
    raise SystemExit(err)

jsonResp = response.json()
numOfRndNews = rnd.randint(0, len(jsonResp["articles"])-1)
paragraph = jsonResp["articles"][numOfRndNews]['content']
source = "Źródło: " +"\n" +jsonResp["articles"][numOfRndNews]['url']
sentencesList = []
sentencesList = paragraph.split(".")

for sentence in sentencesList:
    occure = sentence.find("Intel")
    if (occure != -1):
        lang = TextBlob(sentence).detect_language()
        if(lang != 'pl'):
            try:
                plSentence = Translator().translate(sentence, src=lang, dest='pl').text
            except AttributeError as err:
                print("This is problem on Google site, sorry", err)
                break
            else:
                print("\"", plSentence, "\"", source)
                break
        else:
            print("\"", sentence, "\"", source)
            break
    else:
        print("This news is related to 'Intel' key-word, but it doesn't contain it directly.")
        break
