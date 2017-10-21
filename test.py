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


    def add_url(self,fullUrl,shortUrl):
        now = datetime.datetime.utcnow()
        url = Url(fullUrl=fullUrl, shortUrl=shortUrl, createdDate=now)
        db.session.add(url)
        db.session.commit()
    

    def test_add_url_and_query(self):
        self.add_url('https://www.jooraccess.com/','/joor')
        url = Url.query.filter_by(shortUrl='/joor').first()
        self.assertEqual(url.fullUrl, 'https://www.jooraccess.com/')


    def get_short_url(self,fullUrl):
        response = self.app.post('/getShortUrl/', data=json.dumps({'fullUrl':fullUrl}))    
        response = json.loads(response.get_data())
        return response['shortUrl'][-5:]


    def get_full_url(self,shortLink):
        response = self.app.get(shortLink)
        return response.location


    def test_redirect_cycles(self):
        fullUrls = ['https://www.salesforce.com/','https://www.wsj.com/','https://www.youtube.com/']
        for fullUrl in fullUrls:
            fullUrl = 'https://www.google.com/'
            shortLink = self.get_short_url(fullUrl)
            fullUrlAfterCycle = self.get_full_url(shortLink)
            self.assertEqual(fullUrlAfterCycle, fullUrl + '?deviceType=other')


    def test_get_all_urls(self): 
        urls = ['https://www.google.com/','https://github.com/','https://www.ted.com/']
        for url in urls:
            self.get_short_url(url)
        response = self.app.post('/getAllUrls/')
        values = json.loads(response.get_data())
        self.assertEqual(len(values),3)


if __name__ == '__main__':
    unittest.main()
