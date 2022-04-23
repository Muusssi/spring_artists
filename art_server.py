
import json
import os
import sys

import tornado.ioloop
import tornado.web
import tornado.httpserver

import database as db

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
STATIC_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'static'))
TEMPLATES_DIRECTORY = os.path.abspath(os.path.join(APP_DIRECTORY, 'templates'))


class Application(tornado.web.Application):
    def __init__(self, database):
        handlers = [
                (r"/", MainPageHandler),
                (r"/data/paintings", PaintingsDataHandler),
            ]

        settings = dict(
                template_path=TEMPLATES_DIRECTORY,
                static_path=STATIC_DIRECTORY,
                debug=True,
            )

        self.database = database
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.database

    def data_received(self, chunk):
        pass


class MainPageHandler(BaseHandler):
    def get(self):
        self.render("main_page.html")

    def post(self):
        strokes = json.loads(self.request.body).get('strokes', [])
        painting_id = self.db.store_painting(strokes)
        print(painting_id)

class PaintingsDataHandler(BaseHandler):
    def get(self):
        self.write({'paintings': self.db.paintings()})


def load_config_file(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("error: missing config file")
        sys.exit(1)

    config = load_config_file(sys.argv[1])
    database = db.Database(config)
    httpserver = tornado.httpserver.HTTPServer(Application(database))
    httpserver.listen(config['port'])
    print('starting server:', config['port'])
    tornado.ioloop.IOLoop.current().start()

