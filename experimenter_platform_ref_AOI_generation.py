import tornado
from tornado.options import define, options
import os.path
import itertools
import operator
import re
import collections

import sqlite3
import datetime
import json
import random

import time
#from application.backend.eye_tracker_newsdk import TobiiControllerNewSdk
from application.middleend.adaptation_loop import AdaptationLoop
from application.application_state_controller import ApplicationStateController
from application.application_web_socket import ApplicationWebSocket

#from application.backend.fixation_detector import FixationDetector
#from application.backend.emdat_component import EMDATComponent
#from application.backend.ml_component import MLComponent
#from application.backend.mouse_keyboard_event_detector import MouseKeyboardEventDetector


import params


##########################################
"""
This script will write all the reference sentence AOI files for each MSNV,
with each aoi name being the name from the aoi table in the user state db
    - First an empty log folder in the 1st level of root folder will need to be created
    - It will render each MSNV to get the coordinates, so just open up localhost:8888 once you have started up the
      script and the script will do everything else
    - There is no notification for the script being done, but once it's done flashing it's usually done - (I can add
      some kind of notification if that is preferred)
    - You will know it is done when you see all the .aoi files have been generated

Everything related to connection to the eyetracker, ML and mouse keyboard events have been commented out, so that
it works locally.
"""

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
        #self.tobii_controller = TobiiControllerNewSdk()
        #self.tobii_controller.activate()
        self.app_state_control = ApplicationStateController(0)
        self.adaptation_loop = AdaptationLoop(self.app_state_control)

        #self.fixation_component = FixationDetector(self.tobii_controller, self.adaptation_loop)
        #self.emdat_component = EMDATComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD)
        #self.ml_component = MLComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD, emdat_component = self.emdat_component)
        #self.mouse_key_component = MouseKeyboardEventDetector(self.tobii_controller, self.adaptation_loop, self.emdat_component, params.USE_MOUSE, params.USE_KEYBOARD)
        websocket_dict = {#TOBII_CONTROLLER: self.tobii_controller,
                          APPLICATION_STATE_CONTROLLER: self.app_state_control,
                          ADAPTATION_LOOP: self.adaptation_loop
                          #FIXATION_ALGORITHM: self.fixation_component,
                          #EMDAT_COMPONENT: self.emdat_component,
                          #ML_COMPONENT: self.ml_component,
                          #MOUSE_KEY_COMPONENT: self.mouse_key_component
                          }
        handlers = [
            (r"/", MainHandler),
            (r"/writePolygon", PolygonAjaxHandler),
            (r"/websocket", MMDWebSocket, dict(websocket_dict=websocket_dict))
        ]
        # connects to database
        self.conn = sqlite3.connect(params.USER_MODEL_STATE_PATH)
        # "global variable" to save current UserID of session
        UserID = -1
        # global variable to track start and end times
        start_time = ''
        end_time = ''
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
        self.application.conn.execute('DELETE FROM aoi')
        self.application.conn.commit()

    def on_message(self, message):
        print("RECEIVED MESSAGE: " + message)
        if (message == "done_generating"):
            self.writeAOIsToFile()
        return

    def on_close(self):
        print('closed connection')

    def writeAOIsToFile(self):
        query_result2 = self.application.conn.execute('SELECT task, polygon, name FROM aoi ORDER BY task')
        allAOIs = query_result2.fetchall()
        aoiByTask = {task: {name: polygon for _, polygon, name in aois} for task, aois in itertools.groupby(allAOIs, operator.itemgetter(0))}

        for task, aois in aoiByTask.items():
            f = open(str(task) + ".aoi", "w+")
            overall = 'overall_' + str(task)
            to_write = []
            for ref_name, aoi in aois.items():
                noSpace = re.sub(r"\s", '', aoi)
                tabSeparated = re.sub(r"\),\(", '\t', noSpace)
                bracketsRemoved = re.sub(r"(\)\])|(\[\()", '', tabSeparated)
                overall += '\t'+ bracketsRemoved + '\t;'
                bracketsRemoved = ref_name+'\t'+ bracketsRemoved
                to_write.append(bracketsRemoved)

            to_write = '\n'.join(to_write)
            f.write(to_write)
            f.write('\n'+overall)
            f.close()


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.application.cur_user = -1
        self.application.cur_mmd = 3
        self.application.start_time = str(datetime.datetime.now().time())
        self.render('MMDforAOI.html', mmd=self.application.cur_mmd)


class PolygonAjaxHandler(tornado.web.RequestHandler):
    def post(self):
        # gets polygon coordinates and refIds from frontend coordinateRefSentences
        json_obj = json.loads(self.request.body, object_pairs_hook=collections.OrderedDict)
        for polygon_obj in json_obj['references']:
            ref_id = 'ref_' + polygon_obj['refId']
            polygon = polygon_obj['polygonCoords']
            polygon_tuple = str(list(map(lambda p: tuple(p.values()), polygon)))
            polygon_data = (ref_id, json_obj['MMDid'], polygon_tuple)
            # updates polygon in entry in db with same refId and task number
            self.application.conn.execute('INSERT INTO aoi (name, task, polygon) VALUES (?,?,?)', polygon_data)
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
