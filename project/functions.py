from .const import ALLCHARS
from .sql import Url, db
import datetime


def convert(n):
    # 62 is the number of characters used in the short url
    # this will allow to convert about 15 millions of urls
    shortUrl = [None]*4
    for i in range(4):
        shortUrl[i] = ALLCHARS[i][n%62]
        n //= 62
    return ''.join(shortUrl)

def createNewRecord(root, fullUrl):
    now = datetime.datetime.utcnow()
    number = db.session.query(Url).count()

    if number > 14776336:
        raise Exception('url mapping full')

    shortUrl = root + convert(number)
    url = Url(fullUrl=fullUrl, shortUrl=shortUrl, createdDate=now)
    db.session.add(url)
    db.session.commit()
    return url