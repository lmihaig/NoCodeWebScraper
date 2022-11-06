import datetime
from bson import ObjectId
from mongoengine.fields import EmbeddedDocument, EmbeddedDocumentListField, ListField, StringField, IntField, DateTimeField, ReferenceField
from threading import Lock
from mongoengine import Document, disconnect, connect
from flask import Flask, request
from flask_restx import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class ScrapeEntry(EmbeddedDocument):
    val = ListField(StringField())
    scrapedDate = DateTimeField(default=datetime.datetime.now)

    def export_json(self):
        return {
            "val": self.val,
            "scrapedDate": self.scrapedDate,
        }


class Scrape(EmbeddedDocument):
    selector = StringField()
    name = StringField()
    values = EmbeddedDocumentListField(ScrapeEntry)


class Source(Document):
    url = StringField()
    interval = IntField(default=60*60)
    last_scraped = DateTimeField(default=datetime.datetime.min)
    scrapes = EmbeddedDocumentListField(Scrape)

    def scrape_job(self):
        return {
            "id": str(self.id), "url": self.url,
            "scrapes": [{
                "selector": scrape.selector,
                "name": scrape.name,
            } for scrape in self.scrapes]}


class Widget(EmbeddedDocument):
    source = ReferenceField(Source)
    name = StringField()
    x = IntField()
    y = IntField()
    width = IntField()
    height = IntField()

    def export_json(self):
        return {
            "source": str(self.source.id),
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


class Dashboard(Document):
    widgets = EmbeddedDocumentListField(Widget)
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


@app.route('/api/sources')
def get_sources():
    with mongoConnection:
        return {"sources": [
            {
                "id": str(source.id),
                "url": source.url,
                "scrapes": [
                    scrape.name for scrape in source.scrapes
                ]
            } for source in list(Source.objects)
        ]}


@app.route('/api/source/<source_id>')
def get_source_data(source_id):
    with mongoConnection:
        source = Source.objects.get(id=source_id)
        return {
            scrape.name: list(map(ScrapeEntry.export_json, scrape.values))
            for scrape in source.scrapes}


@api.route('/api/scraper')
class Scraper(Resource):
    def get(self):
        with mongoConnection:
            for source in Source.objects:
                if source.last_scraped + datetime.timedelta(seconds=source.interval) > datetime.datetime.now():
                    continue

                return {"status": "work", "job": source.scrape_job()}
            return {"status": "empty"}

    def post(self):
        args = request.get_json()
        print(args)
        if args["status"] != "OK":
            return 0
        with mongoConnection:
            source = Source.objects.filter(id=args["id"])
            if len(source) != 1:
                return {}, 400

            source = source[0]

            source.last_scraped = datetime.datetime.now()
            for i in range(len(source.scrapes)):
                source.scrapes[i].values.append(ScrapeEntry(val=args["scrapes"][i]))
            source.save()


@api.route('/api/extension')
class Extension(Resource):
    def post(self):
        args = request.get_json()
        with mongoConnection:
            Source(
                url=args["url"],
                scrapes=[
                    Scrape(name=scrape["name"], selector=scrape["selector"])
                    for scrape in args["scrapes"]]
            ).save()


def exportObjID(field_name):
    def internal(object):
        object.__setattr__(field_name, str(object.__getattribute__(field_name).id))
        print(str(object.__getattribute__(field_name)))
        return object
    return internal


@api.route("/api/widget")
class Widgets(Resource):
    def get(self):
        with mongoConnection:
            dashboard = Dashboard.objects.get(id="6367338f7c658786739d54cc")
            out = list(map(Widget.export_json, list(dashboard.widgets)))
            return out

    def post(self):
        args = request.get_json()
        print(args)
        with mongoConnection:
            dashboard = Dashboard.objects.get(id="6367338f7c658786739d54cc")
            dashboard.widgets.append(Widget(
                name=args["name"],
                source=ObjectId(args["source"]),
                x=args["x"],
                y=args["y"],
                width=args["width"],
                height=args["height"],
            ))
            dashboard.save()


@app.route("/api/dashboard/reorder", methods=["POST"])
def resize_widget():
    with mongoConnection:
        dashboard = Dashboard.objects.get(id="6367338f7c658786739d54cc")
        args = request.get_json()
        print(args[0])
        for i in range(len(dashboard.widgets)):
            dashboard.widgets[i].x = args[i]["x"]
            dashboard.widgets[i].y = args[i]["y"]
            dashboard.widgets[i].width = args[i]["width"]
            dashboard.widgets[i].height = args[i]["height"]

        dashboard.save()
    return "", 200


@app.route("/api/widget/<widget_id>", methods=["DELETE"])
def delete_widget(widget_id):
    with mongoConnection:
        dashboard = Dashboard.objects.get(id="6367338f7c658786739d54cc")
        del dashboard.widgets[int(widget_id)]
        dashboard.save()


if __name__ == '__main__':
    app.run(debug=True, port=8069, host="0.0.0.0")
