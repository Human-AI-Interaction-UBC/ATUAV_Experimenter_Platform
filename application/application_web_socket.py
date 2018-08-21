import tornado.websocket

from application.backend.eye_tracker import TobiiController
from application.backend.fixation_detector import FixationDetector
from application.backend.emdat_component import EMDATComponent
from application.backend.ml_component import MLComponent

import params

from application.middleend.adaptation_loop import AdaptationLoop
from application.application_state_controller import ApplicationStateController

class ApplicationWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        self.websocket_ping_interval = 0
        self.websocket_ping_timeout = float("inf")
        self.app_state_control = ApplicationStateController(1)
        self.adaptation_loop = AdaptationLoop(self.app_state_control)
        self.adaptation_loop.liveWebSocket = self

        self.tobii_controller = TobiiController()
        self.tobii_controller.waitForFindEyeTracker()
        print self.tobii_controller.eyetrackers
        self.tobii_controller.activate(self.tobii_controller.eyetrackers.keys()[0])
        self.start_detection_components()        
        self.tobii_controller.startTracking()
        print "tracking started"

    def on_message(self, message):
        if (message == "close"):
            print("destroying")
            self.stop_detection_components()
            self.tobii_controller.stopTracking()
            self.tobii_controller.destroy()
            self.app_state_control.resetApplication()
            return

        elif (message.find("switch_task") != -1):
            print("SWITCHIGN TASK")
            result = message.split(":")
            next_task = int(result[1])

            self.stop_detection_components()
            self.tobii_controller.stopTracking()
            self.app_state_control.changeTask(next_task)
            self.start_detection_components()
            self.tobii_controller.startTracking()
            return

        else:
            self.stop_detection_components()
            self.tobii_controller.stopTracking()
            self.tobii_controller.destroy()
            self.app_state_control.resetApplication()
            return

    def on_close(self):
        self.stop_detection_components()
        self.tobii_controller.stopTracking()
        self.tobii_controller.destroy()
        self.app_state_control.resetApplication()

    def start_detection_components(self):
        if (params.USE_FIXATION_ALGORITHM):
            self.fixation_component = FixationDetector(self.tobii_controller, self.adaptation_loop)
            self.fixation_component.start()
        if (params.USE_EMDAT):
            self.emdat_component = EMDATComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD)
            self.emdat_component.start()
            if (params.USE_ML):
                self.ml_component = MLComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD, emdat_component = self.emdat_component)
                self.ml_component.start()

    def stop_detection_components(self):
        if (params.USE_FIXATION_ALGORITHM):
            self.fixation_component.stop()
            del self.fixation_component
        if (params.USE_EMDAT):
            self.emdat_component.stop()
            del self.emdat_component
            if (params.USE_ML):
                self.ml_component.stop()
                del self.ml_component
