from . import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
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