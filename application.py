import datetime
import os
import requests
import validators
from string import ascii_letters, ascii_uppercase, ascii_lowercase, digits
from flask import Flask, render_template, json, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from user_agents import parse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  + os.path.dirname(__file__) + 'urls.db'
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
        return {
            'fullUrl':self.fullUrl,
            'shortUrl':self.shortUrl,
            'createdDate':self.createdDate,
            'redirectsCount':self.redirectsCount
        }


# creating multiple char dicts, so that initial links won't have many consecutive same characters
myChars = [None]*4
myChars[0] =  {i: char for i, char in enumerate(ascii_letters + digits)}
myChars[1] =  {i: char for i, char in enumerate(ascii_letters[::-1] + digits[::-1])}
myChars[2] =  {i: char for i, char in enumerate(digits + ascii_letters[::-1])}
myChars[3] =  {i: char for i, char in enumerate(ascii_lowercase + digits + ascii_uppercase)}


# this will allow to convert about 15 millions of urls
def convert(n):
    shortUrl = [None]*4
    for i in range(4):
        shortUrl[i] = myChars[i][n%62]
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


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/<shortUrl>')
def getFullUrl(shortUrl):
    root = request.url_root
    user_agent = parse(str(request.user_agent))

    if (user_agent.is_pc):
        deviceType = 'desktop'
    elif (user_agent.is_tablet):
        deviceType = 'tablet'
    elif (user_agent.is_mobile):
        deviceType = 'mobile'
    else:
        deviceType = 'other'

    url = Url.query.filter_by(shortUrl=request.url_root + shortUrl).first()
    if url:
        url.redirectsCount += 1
        db.session.commit()
        return redirect(url.fullUrl + '?deviceType=' + deviceType) 
    return redirect('/')


@app.route('/getShortUrl/', methods=['POST'])
def getShortUrl():
    
    fullUrl = json.loads(request.data.decode('utf-8'))['fullUrl']

    if not validators.url(fullUrl):
        return Response(json.dumps({'message':'not a valid url'}), status=400)

    url = Url.query.filter_by(fullUrl=fullUrl).first()
    if not url:
        root = request.url_root
        url = createNewRecord(root,fullUrl)

    return Response(json.dumps(url.returnDict()), status=200) 


@app.route('/getAllUrls/', methods=['POST'])
def getAllUrls():
    urls = Url.query.all()
    return Response(json.dumps([url.returnDict() for url in urls]), status=200)


if __name__ == "__main__":
    app.debug = False
    app.run()

