from . import app
from .const import AVLCHARS
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  + os.path.join(basedir, 'urls.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    fullUrl = db.Column(db.String(2048), unique=False, nullable=False)
    shortUrl = db.Column(db.String(50), unique=True, nullable=False)
    redirectsCount = db.Column(db.Integer, unique=False, nullable=False, default=0)
    createdDate = db.Column(db.DateTime, unique=False, nullable=False)
    def returnDict(self):
        return {'fullUrl':self.fullUrl,
            'shortUrl':self.shortUrl,
            'createdDate':self.createdDate,
            'redirectsCount':self.redirectsCount}


def convert(n):
    # this will allow to convert about 15 millions of urls
    shortUrl = [None]*4
    for i in range(4):
        shortUrl[i] = AVLCHARS[i][n%62]
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