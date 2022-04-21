
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


PORT = 8003

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("error: missing password")
        sys.exit(1)

    httpserver = tornado.httpserver.HTTPServer(Application(db.Database(sys.argv[1])))
    httpserver.listen(PORT)
    print('starting server:', PORT)
    tornado.ioloop.IOLoop.current().start()

