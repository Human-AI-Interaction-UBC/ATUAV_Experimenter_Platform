from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect


class EyetrackerWebsocketClient(object):
    def __init__(self, tobii_controller):
        self.gaze_url = "ws://localhost:8887/gaze"
        self.tobii_controller = tobii_controller
        self.ws = None
        self.track_data = False
        self.connect()

    @gen.coroutine
    def connect(self):
        print "trying to connect"
        try:
            self.ws = yield websocket_connect(self.gaze_url)
        except Exception, e:
            print "connection error"
        else:
            print "connected"

    @gen.coroutine
    def run(self):
        while self.track_data:
            msg = yield self.ws.read_message()
            #print msg
            if msg is not None:
                msg = msg.split(",")
                self.tobii_controller.on_gazedata_4c(float(msg[0]), float(msg[1]), float(msg[2]) * 1000)
            else:
                print("Eyetracker websocket connection was interrupted!")

    @gen.coroutine
    def start_tracking(self):
        self.track_data = True
        IOLoop.instance().add_callback(callback = self.run)


    def stop_tracking(self):
        self.track_data = False
