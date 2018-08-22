import tornado.websocket


import params


TOBII_CONTROLLER = "tobii_controller"
APPLICATION_STATE_CONTROLLER = "application_state_controller"
ADAPTATION_LOOP = "adaptation_loop"
FIXATION_ALGORITHM = "fixation_algorithm"
EMDAT_COMPONENT = "emdat_component"
ML_COMPONENT = "ml_component"


class ApplicationWebSocket(tornado.websocket.WebSocketHandler):

    def initialize(self, websocket_dict):
        self.tobii_controller = websocket_dict[TOBII_CONTROLLER]
        self.app_state_control = websocket_dict[APPLICATION_STATE_CONTROLLER]
        self.adaptation_loop = websocket_dict[ADAPTATION_LOOP]
        next_task = self.application.cur_mmd
        self.app_state_control.changeTask(next_task, self.application.cur_user)
        self.fixation_component = websocket_dict[FIXATION_ALGORITHM]
        self.emdat_component = websocket_dict[EMDAT_COMPONENT]
        self.ml_component = websocket_dict[ML_COMPONENT]

    def open(self):

        self.websocket_ping_interval = 0
        self.websocket_ping_timeout = float("inf")
        self.adaptation_loop.liveWebSocket = self

        print self.tobii_controller.eyetrackers
        self.start_detection_components()
        self.tobii_controller.startTracking()

    def on_message(self, message):
        if (message == "close"):
            self.stop_detection_components()
            self.tobii_controller.stopTracking()
            self.tobii_controller.destroy()
            self.app_state_control.resetApplication()
            return

        elif (message.find("switch_task") != -1):
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

    def start_detection_components(self):
        if (params.USE_FIXATION_ALGORITHM):
            self.fixation_component.restart_fixation_algorithm()
            self.fixation_component.start()
        if (params.USE_EMDAT):
            self.emdat_component.setup_new_emdat_component()
            self.emdat_component.start()
            if (params.USE_ML):
                self.ml_component.start()

    def stop_detection_components(self):
        if (params.USE_FIXATION_ALGORITHM):
            self.fixation_component.stop()
        if (params.USE_EMDAT):
            self.emdat_component.stop()
            if (params.USE_ML):
                self.ml_component.stop()
