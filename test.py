from run import app
import unittest
import json
from flask_testing import TestCase

# I had problems to change the database
# therefore I am testing on the production database (I know it is bad)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client(self)  

    def test_index_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code,200)


    def test_index_render(self):
        response = self.app.get('/')
        self.assertTrue(b'Get shortened Url' in response.data)


    def check_new_url(self,url):
        response = self.app.post('/getShortUrl/', 
            data=json.dumps({'fullUrl':url}))    
        values = json.loads(response.get_data())
        code = values['shortUrl'][-4:]
        response = self.app.get('/' + code)
        self.assertEqual(response.location, url + '?deviceType=other')


    def test_urls(self):
        urls = ['https://www.google.com/','https://github.com/','https://www.ted.com/']
        for url in urls:
            self.check_new_url(url)

        response = self.app.post('/getAllUrls/')
        values = json.loads(response.get_data())
        self.assertTrue(len(values)>2)


if __name__ == '__main__':

    unittest.main()
