from . import app, sql
from .sql import Url, db
import requests
import validators
from flask import Flask, render_template, json, request, redirect, Response
from user_agents import parse


@app.route('/', methods=['GET'])
def index():
    return render_template("home.html")


@app.route('/<shortUrl>', methods=['GET'])
def getFullUrl(shortUrl):

    
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
        url = sql.createNewRecord(root,fullUrl)

    return Response(json.dumps(url.returnDict()), status=200) 


@app.route('/getAllUrls/', methods=['POST'])
def getAllUrls():

    urls = Url.query.all()
    return Response(json.dumps([url.returnDict() for url in urls]), status=200)

