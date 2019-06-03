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
"""
This script will generate all the text AOI coordinates for each MSNV, and write it to the database.
    - It will render each MSNV to get the coordinates, so just open up localhost:8888 once you have started up the 
      script and the script will do everything else
    - There is no notification for the script being done, but once it's done flashing it's usually done - (I can add 
      some kind of notification if that is preferred)
    - You will know it is done when you see all the .aoi files have been generated
      
This script will also write all the .aoi files needed for the draw_text_AOIs.R, to verify that the AOIs have been 
generated correctly.
    - for the R script to run properly, you will need:
        - all the .aoi files
        - a screenshot for every MSNV that you have a .aoi file for (named [aoi_number].png)
        - all of the above in the same directory
    - all you have to do is change the path in the R script to be the path where your files are in, and check the array 
      of MSNVs that the script is looking for is the same as the numbers you have for your .aoi files
    - The R script will create [aoi_number]_drawn.png with the AOI coordinates plotted and drawn for you to verify the
      AOIs have been generated correctly

If you are running this locally, without an eye tracker:
    - you can comment out everything related to the following:
        - "tobii_controller"
        - "fixation_algorithm
        - "emdat_component"
        - "ml_component"
        - "mouse_key_component"
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
        self.tobii_controller = TobiiControllerNewSdk()
        self.tobii_controller.activate()
        self.app_state_control = ApplicationStateController(0)
        self.adaptation_loop = AdaptationLoop(self.app_state_control)

        self.fixation_component = FixationDetector(self.tobii_controller, self.adaptation_loop)
        self.emdat_component = EMDATComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD)
        self.ml_component = MLComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD, emdat_component = self.emdat_component)
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
        query_result2 = self.application.conn.execute('SELECT task, polygon FROM aoi ORDER BY task')
        allAOIs = query_result2.fetchall()
        aoiByTask = [(task, [polygon for _, polygon in aois]) for task, aois in itertools.groupby(allAOIs, operator.itemgetter(0))]

        for aoiSet in aoiByTask:
            aoiFileName = str(aoiSet[0])
            f=open(aoiFileName + ".aoi", "w+")
            aoiRefs = ','.join(aoiSet[1])
            noSpace = re.sub(r" ", '', aoiRefs)
            tabSeparated = re.sub(r"\),", '\t', noSpace)
            extraCommasRemoved = re.sub(r"\],", '\t', tabSeparated)
            final = re.sub(r"([\(\)\[\]])", '', extraCommasRemoved)
            f.write(final + "\n")


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
