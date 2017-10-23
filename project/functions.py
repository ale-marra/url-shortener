from .sql import Url, db
import datetime
import random
import string
from sqlalchemy import func

def getRandomUrl():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=4))

def getShortUrl():
    # theoretically, the max number of short urls is 14,776,336
    # however I limit the insertion to 5,000,000
    # otherwise this function would be very slow
    shortUrlCount = db.session.query(Url.shortUrl).distinct().count()
    if shortUrlCount > 5000000:
        raise Exception('url mapping full')

    while True:
        shortUrl = getRandomUrl()
        if Url.query.filter_by(shortUrl=shortUrl).first() == None:
            break

    return shortUrl


def updateRecords(targetUrl, deviceTypes, shortUrl):
    urls = []
    for deviceType in deviceTypes:
        url = Url.query.filter_by(shortUrl=shortUrl, deviceType=deviceType).first()
        url.targetUrl = targetUrl
        urls += [url.returnDict()]
    db.session.commit()
    return urls


def createRecords(targetUrl, deviceTypes, root):
    now = datetime.datetime.utcnow()
    shortUrl = root + getShortUrl()
    urls = []
    for deviceType in deviceTypes:
        url = Url(targetUrl=targetUrl, shortUrl=shortUrl, createdDate=now, deviceType=deviceType)
        db.session.add(url)
        urls += [url.returnDict()]
    db.session.commit()
    return urls