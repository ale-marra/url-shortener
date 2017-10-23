from . import app, sql
from .sql import Url, db
from .functions import updateRecords, createRecords

import validators
from flask import Flask, render_template, json, request, redirect, Response
from user_agents import parse


@app.route('/', methods=['GET'])
def index():
    return render_template("home.html")


@app.route('/<shortUrl>', methods=['GET'])
def getFullUrl(shortUrl):

    user_agent = parse(str(request.user_agent))
    if (user_agent.is_mobile):
        deviceType = 'Mobile'
    elif (user_agent.is_tablet):
        deviceType = 'Tablet'
    else:
        deviceType = 'Desktop'

    url = Url.query.filter_by(shortUrl=request.url_root + shortUrl, deviceType=deviceType).first()
    if url:
        url.redirectsCount += 1
        db.session.commit()
        return redirect(url.targetUrl)
    return redirect('/')


@app.route('/getshorturl/', methods=['POST'])
def getShortUrl():
    targetUrl = json.loads(request.data.decode('utf-8'))['targetUrl'].strip()

    if not validators.url(targetUrl):
        return Response(json.dumps({'message':'not a valid target url'}), status=400)

    urls = createRecords(targetUrl, ['Mobile','Tablet','Desktop'], request.url_root)

    return Response(json.dumps(urls), status=200)


@app.route('/configureshorturl/', methods=['POST'])
def configureshorturl():

    shortUrl = json.loads(request.data.decode('utf-8'))['shortUrl'].strip()
    targetUrl = json.loads(request.data.decode('utf-8'))['targetUrl'].strip()
    deviceTypes = json.loads(request.data.decode('utf-8'))['deviceTypes']

    if not validators.url(targetUrl):
        return Response(json.dumps({'message':'not a valid target url'}), status=400)
    
    for deviceType in deviceTypes:
        if not Url.query.filter_by(shortUrl=shortUrl, deviceType=deviceType).first():
            return Response(json.dumps({'message': shortUrl + ' not found in the database'}), status=400)

    urls = updateRecords(targetUrl, deviceTypes, shortUrl)
    return Response(json.dumps(urls), status=200) 




@app.route('/getallurls/', methods=['POST'])
def getAllUrls():

    urls = Url.query.all()
    return Response(json.dumps([url.returnDict() for url in urls]), status=200)



@app.route('/clearall/', methods=['POST'])
def clearAll():
    urls = Url.query.delete()
    db.session.commit()
    return Response(status=200) 
