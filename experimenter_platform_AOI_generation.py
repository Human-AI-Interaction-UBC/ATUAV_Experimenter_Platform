import tornado
from tornado.options import define, options
import os.path

import sqlite3
import datetime
import json
import random

# Imports required for EYE TRACKING Code:
import time
from application.backend.eye_tracker_newsdk import TobiiControllerNewSdk
from application.middleend.adaptation_loop import AdaptationLoop
from application.application_state_controller import ApplicationStateController
from application.application_web_socket import ApplicationWebSocket

from application.backend.fixation_detector import FixationDetector
from application.backend.emdat_component import EMDATComponent
from application.backend.ml_component import MLComponent
from application.backend.mouse_keyboard_event_detector import MouseKeyboardEventDetector


import params


##########################################

define("port", default=8888, help="run on the given port", type=int)
TOBII_CONTROLLER = "tobii_controller"
APPLICATION_STATE_CONTROLLER = "application_state_controller"
ADAPTATION_LOOP = "adaptation_loop"
FIXATION_ALGORITHM = "fixation_algorithm"
EMDAT_COMPONENT = "emdat_component"
ML_COMPONENT = "ml_component"
MOUSE_KEY_COMPONENT = "mouse_key_component"


class Application(tornado.web.Application):
    def __init__(self):
        # connects url with code

        self.tobii_controller = TobiiControllerNewSdk()
        self.tobii_controller.activate()
        self.app_state_control = ApplicationStateController(0)
        self.adaptation_loop = AdaptationLoop(self.app_state_control)

        self.fixation_component = FixationDetector(self.tobii_controller, self.adaptation_loop)
        self.emdat_component = EMDATComponent(self.tobii_controller, self.adaptation_loop, callback_time=params.EMDAT_CALL_PERIOD)
        self.ml_component = MLComponent(self.tobii_controller, self.adaptation_loop, callback_time=params.EMDAT_CALL_PERIOD, emdat_component=self.emdat_component)
        self.mouse_key_component = MouseKeyboardEventDetector(self.tobii_controller, self.adaptation_loop, self.emdat_component, params.USE_MOUSE, params.USE_KEYBOARD)

        websocket_dict = {TOBII_CONTROLLER: self.tobii_controller,
                          APPLICATION_STATE_CONTROLLER: self.app_state_control,
                          ADAPTATION_LOOP: self.adaptation_loop,
                          FIXATION_ALGORITHM: self.fixation_component,
                          EMDAT_COMPONENT: self.emdat_component,
                          ML_COMPONENT: self.ml_component,
                          MOUSE_KEY_COMPONENT: self.mouse_key_component}
        handlers = [
            (r"/", MainHandler),
            (r"/calibration", CalibrationHandler), (r"/(blank_cross.jpg)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
            (r"/tobii", TobiiHandler),
            (r"/ready", ReadyHandler),
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
        print self.tobii_controller.eyetrackers

        # self.start_detection_components()
        # self.tobii_controller.startTracking()

    def on_message(self, message):
        print("RECEIVED MESSAGE: " + message)
        self.stop_detection_components()
        self.tobii_controller.stopTracking()
        self.tobii_controller.destroy()
        return

    def on_close(self):
        self.app_state_control.logTask(user_id=self.application.cur_user)


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.application.start_time = str(datetime.datetime.now().time())
        self.render('generateAOIIndex.html')


class TobiiHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("load_tobii.html")

    def post(self):
        self.redirect('/calibration')


class CalibrationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("calibration.html")

    def post(self):
        self.redirect('/ready')


class ReadyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ready.html")
    def post(self):
        self.redirect('/mmd')


class PolygonAjaxHandler(tornado.web.RequestHandler):
    def post(self):
        # gets polygon coordinates and refIds from frontend coordinateRefSentences
        json_obj = json.loads(self.request.body)
        for polygon_obj in json_obj['references']:
            ref_id = 'ref_' + polygon_obj['refId']
            polygon = polygon_obj['polygonCoords']
            polygon_tuple = str(list(map(lambda p: tuple(p.values()), polygon)))
            polygon_data = (polygon_tuple, ref_id, json_obj['MMDid'])
            # updates polygon in entry in db with same refId and task number
            self.application.conn.execute('UPDATE aoi SET polygon=? WHERE name=? AND task=?', polygon_data)
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
