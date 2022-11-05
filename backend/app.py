from mongoengine.fields import EmbeddedDocumentListField, ReferenceField, DictField, StringField, ListField, IntField, DateTimeField, ReferenceField
from threading import Lock
from mongoengine import Document, disconnect, connect
from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Resource, Api, reqparse
import pymongo
app = Flask(__name__)
api = Api(app)


app.config["MONGO_URI"] = 'mongodb://localhost:27017/dashboards'
# mongo = PyMongo(app)
# db = mongo.db
parser = reqparse.RequestParser()

# dashboards = []
# dashboard = {
#     "id": 202020,
#     "widgets": [
#         {
#             "source": "url",
#             "interval": 60,
#             "last_scraped": "datetime",
#             "scrapes": [obiecte dastea care au name val selector],
#         }
#     ]
# }


class Scrape(Document):
    selector = StringField()
    name = StringField()
    val = DictField()


class Source(Document):
    url = StringField()
    interval = IntField()
    last_scraped = DateTimeField()
    scrapes = ListField(ReferenceField(Scrape))


class Widget(EmbededDocument):
    source = ReferenceField(Source)
    # TBD FRONTEND
    name = StringField()


class dashboard(Document):
    widget = EmbeddedDocumentListField(Widget)
    name = 


class MongoConnection(object):
    def __init__(self):
        self.lock = Lock()
        self.connection = None

    def __enter__(self):
        self.lock.acquire()
        self.connection = connect(
            "dashboards",
            host="localhost",
        )

    def __exit__(self, type, value, traceback):
        disconnect("dashboards")
        self.lock.release()


mongoConnection = MongoConnection()


@api.route('/api/scraper')
class Scraper(Resource):
    def get(self):
        with mongoConnection:

            if expired_scrapes:

            else:
                return {"status": "empty"}

    def post(self):


@api.route('/api/scrapes')
class Scrapes(Resource):
    def get(self):
        return scrapes

    def post(self):
        args = parser.parse_args()
        print(args)


@api.route('/api/scrape/<string:scrape_id>')
class Scrape(Resource):
    def get(self, scrape_id):
        # replace with proper scrape id
        return scrapeYt


if __name__ == '__main__':
    app.run(debug=True, port=8069)
