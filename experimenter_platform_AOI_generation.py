import tornado
from tornado.options import define, options
import os.path

import sqlite3
import datetime
import json
import random

import time
from application.middleend.adaptation_loop import AdaptationLoop
from application.application_state_controller import ApplicationStateController
from application.application_web_socket import ApplicationWebSocket


import params


##########################################

define("port", default=8888, help="run on the given port", type=int)
TOBII_CONTROLLER = "tobii_controller"
APPLICATION_STATE_CONTROLLER = "application_state_controller"
ADAPTATION_LOOP = "adaptation_loop"


class Application(tornado.web.Application):
    def __init__(self):
        # connects url with code
        self.app_state_control = ApplicationStateController(0)
        self.adaptation_loop = AdaptationLoop(self.app_state_control)
        websocket_dict = {APPLICATION_STATE_CONTROLLER: self.app_state_control,
                          ADAPTATION_LOOP: self.adaptation_loop}
        handlers = [
            (r"/", MainHandler),
            (r"/writePolygon", PolygonAjaxHandler),
            (r"/websocket", MMDWebSocket, dict(websocket_dict=websocket_dict))
        ]
        # connects to database
        self.conn = sqlite3.connect(params.USER_MODEL_STATE_PATH)
        # "global variable" to save current UserID of session
        UserID = -1;
        # global variable to track start and end times
        start_time = '';
        end_time = '';
        # where to look for the html files
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), params.FRONT_END_TEMPLATE_PATH),
            static_path=os.path.join(os.path.dirname(__file__), params.FRONT_END_STATIC_PATH),
            debug=True,
        )
        # initializes web app
        tornado.web.Application.__init__(self, handlers, **settings)


class MMDWebSocket(ApplicationWebSocket):

    def open(self):
        self.websocket_ping_interval = 0
        self.websocket_ping_timeout = float("inf")
        self.adaptation_loop.liveWebSocket = self

    def on_message(self, message):
        print("RECEIVED MESSAGE: " + message)
        return

    def on_close(self):
        self.app_state_control.logTask(user_id=self.application.cur_user)


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.application.cur_user = -1
        self.application.cur_mmd = 3
        self.application.start_time = str(datetime.datetime.now().time())
        self.render('MMDforAOI.html', mmd=self.application.cur_mmd)


class PolygonAjaxHandler(tornado.web.RequestHandler):
    def post(self):
        # gets polygon coordinates and refIds from frontend coordinateRefSentences
        json_obj = json.loads(self.request.body)
        query_results = self.application.conn.execute('SELECT name FROM aoi WHERE task=?', (json_obj['MMDid'],))
        aois = query_results.fetchall()
        aoi_array = [aoi for sublist in aois for aoi in sublist]
        print(aoi_array)
        for polygon_obj in json_obj['references']:
            ref_id = 'ref_' + polygon_obj['refId']
            polygon = polygon_obj['polygonCoords']
            polygon_tuple = str(list(map(lambda p: tuple(p.values()), polygon)))
            polygon_data = (polygon_tuple, ref_id, json_obj['MMDid'])
            polygon_data2 = (ref_id, json_obj['MMDid'], polygon_tuple)
            # updates polygon in entry in db with same refId and task number
            if (ref_id in aoi_array):
                self.application.conn.execute('UPDATE aoi SET polygon=? WHERE name=? AND task=?', polygon_data)
            else:
                print('writing a new entry')
                self.application.conn.execute('INSERT INTO aoi (name, task, polygon) VALUES (?,?,?)', polygon_data2)
        self.application.conn.commit()


# main function is first thing to run when application starts
def main():
    tornado.options.parse_command_line()
    # Application() refers to 'class Application'
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
