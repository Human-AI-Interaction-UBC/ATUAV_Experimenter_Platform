from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
import time

class SimulationSocket(object):
    def __init__(self, tobii_controller):
        self.tobii_controller = tobii_controller
        self.ws = None
        self.track_data = False

    @gen.coroutine
    def connect(self):
        try:
            IOLoop.instance().add_callback(callback = self.run)
        except Exception, e:
            print "connection error"
        else:
            print "simulation started"
			
    @gen.coroutine
    def run(self):
        i = 1
        #time.sleep(10)
        while True:
            msg1 = "400,310,"+str(i)
            msg2 = "600,310,"+str(i)
            msg = msg1
            current_message = 1
            #print msg
            if msg is not None:
                if self.track_data:
                    if (i % 10) == 0:
                        msg = msg2 if current_message == 1 else msg1
                        current_message = 2 if current_message == 1 else 1 
                    msg = msg.split(",")
                    self.tobii_controller.on_gazedata_simulation(float(msg[0]), float(msg[1]), float(msg[2]) * 20000)
                    #print "msg"
                    yield gen.sleep(.1)
                    i += 1
            else:
                print("Eyetracker websocket connection was interrupted!")

    def start_tracking(self):
        self.track_data = True
        self.connect()

    def stop_tracking(self):
        self.track_data = False
