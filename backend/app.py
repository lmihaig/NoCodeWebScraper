import datetime
from mongoengine.fields import EmbeddedDocument, EmbeddedDocumentListField, ReferenceField, DictField, StringField, ListField, IntField, DateTimeField, ReferenceField
from threading import Lock
from mongoengine import Document, disconnect, connect
from flask import Flask, request
from flask_restx import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class ScrapeEntry(EmbeddedDocument):
    val = DictField()
    scrapedDate = DateTimeField(default=datetime.datetime.now)


class Scrape(EmbeddedDocument):
    selector = StringField()
    name = StringField()
    values = EmbeddedDocumentListField(ScrapeEntry)


class Source(Document):
    url = StringField()
    interval = IntField()
    last_scraped = DateTimeField()
    scrapes = EmbeddedDocumentListField(Scrape)

    def scrape_job(self):
        return {
            "id": self.id, "url": self.url,
            "scrapes": [{
                "selector": self.scrapes.selector,
                "name": self.scrapes.name,
            } for scrape in self.scrapes]}


class Widget(EmbeddedDocument):
    source = ReferenceField(Source)
    # TODO  FRONTEND
    name = StringField()


class Dashboard(Document):
    widget = EmbeddedDocumentListField(Widget)
    name = StringField()


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
            expired_scrapes = []
            for source in Source.objects:
                if source.lastscraped + datetime.timedelta(seconds=source.interval) < datetime.datetime.now():
                    continue

                return {"status": "work", "job": source.scrape_job()}
            return {"status": "empty"}

    def post(self):
        args = request.get_json()
        if args["status"] != "OK":
            return 0
        with mongoConnection:
            source = Source.objects.filter(id=args["id"])

            source.last_scraped = datetime.datetime.now()
            for scrape in source.scrapes:
                for new_entry in args["scrapes"]:
                    if scrape.name == new_entry["name"]:
                        scrape.values.append(ScrapeEntry(val=new_entry["val"]))
                        break
            source.save()


@api.route('/api/extension')
class Extension(Resource):
    def post(self):
        args = request.get_json()
        with mongoConnection:
            

if __name__ == '__main__':
    app.run(debug=True, port=8069)
