from project import app, db, Url
import unittest
import json
import datetime


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['TESTING'] = True


class FlaskrTestCase(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client(self) 
        Url.query.delete()
        db.session.commit()


    def tearDown(self):
        Url.query.delete()
        db.session.commit()


    def test_index_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code,200)


    def test_index_render(self):
        response = self.app.get('/')
        self.assertTrue(b'Get shortened Url' in response.data)


    def add_url(self,targetUrl,shortUrl,deviceType):
        now = datetime.datetime.utcnow()
        url = Url(targetUrl=targetUrl, deviceType=deviceType, shortUrl=shortUrl, createdDate=now)
        db.session.add(url)
        db.session.commit()
    

    def test_add_url_and_query(self):
        self.add_url('https://www.jooraccess.com/','/joor','Desktop')
        url = Url.query.filter_by(shortUrl='/joor').first()
        self.assertEqual(url.targetUrl, 'https://www.jooraccess.com/')


    def get_short_url(self,targetUrl):
        response = self.app.post('/getshorturl/', data=json.dumps({'targetUrl':targetUrl}))    
        results = json.loads(response.get_data())
        return results[0]['shortUrl']


    def get_full_url(self,shortLink):
        response = self.app.get(shortLink)
        return response.location


    def test_redirect_cycles(self):
        targetUrls = ['https://www.salesforce.com/','https://www.wsj.com/','https://www.youtube.com/']
        for targetUrl in targetUrls:
            shortLink = self.get_short_url(targetUrl)
            targetUrlAfterCycle = self.get_full_url(shortLink)
            self.assertEqual(targetUrlAfterCycle, targetUrl)


    def test_configure_short_url(self):
        targetUrl = 'https://twitter.com'
        shortUrl = self.get_short_url(targetUrl)
        newTargetUrl = 'https://facebook.com'
        data = {'shortUrl':shortUrl,'deviceTypes':["Desktop"],'targetUrl':newTargetUrl}
        response = self.app.post('/configureshorturl/', data=json.dumps(data))    
        redirect = self.get_full_url(shortUrl)
        self.assertEqual(redirect, newTargetUrl)


    def test_get_all_urls(self): 
        urls = ['https://www.google.com/','https://github.com/','https://www.ted.com/']
        for url in urls:
            self.get_short_url(url)
        response = self.app.post('/getallurls/')
        result = json.loads(response.get_data())
        self.assertEqual(len(result),9)


if __name__ == '__main__':
    unittest.main()
