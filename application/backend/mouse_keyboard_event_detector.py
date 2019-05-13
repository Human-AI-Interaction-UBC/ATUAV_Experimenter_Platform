from detection_component import DetectionComponent
from tornado import gen
import math
import utils
import geometry
import time
from pynput import mouse, keyboard
import Queue
from tornado.ioloop import IOLoop


class MouseKeyboardEventDetector(DetectionComponent):

    def __init__(self, tobii_controller, application_state_controller, emdat_component, use_mouse, use_keyboard):
        DetectionComponent.__init__(self, tobii_controller, application_state_controller, is_periodic = False)
        self.predicted_features = {}
        self.id = 1
        self.emdat_component = emdat_component
        self.listeners = []
        self.mouse_queue = Queue.Queue()
        if use_mouse:
            self.listeners.append(mouse.Listener(
    								#on_move=on_move,
                                    #on_scroll=on_scroll,
    								on_click=self.on_click
    								))
        if use_keyboard:
			self.listeners.append(keyboard.Listener(
            					    #on_release=on_release,
								    on_press=self.on_press
                                    ))
        IOLoop.instance().add_callback(callback = self.notify_app_state_controller)
        self.run_mouse_checks = True
        print("Constructed the mouse listener")

    @gen.coroutine
    def notify_app_state_controller(self):
        while self.run_mouse_checks:
            if self.mouse_queue.qsize() > 0:
                aoi, time_stamp, pressed = self.mouse_queue.get()
                print("MOUSE click in AOI: ", aoi)                
                self.cur_mouse_event_id += 1
                self.application_state_controller.updateMouseTable(aoi, self.cur_mouse_event_id, time_stamp, pressed)
                self.adaptation_loop.evaluateRules(aoi, time_stamp)
            else:
                yield

    def run(self):
        ## Do something
        print("RUNNING THE MOUSE")
        self.cur_mouse_event_id = 0
        self.AOIS = self.application_state_controller.getMouseAoiMapping()
        print("AOIS in mouse: ", self.AOIS)
        for listener in self.listeners:
            listener.start()

    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format( 'Pressed' if pressed else 'Released', (x, y)))
        for aoi in self.AOIS:
            if (utils.point_inside_polygon(x, y, self.AOIS[aoi])):
                self.mouse_queue.put((aoi, self.tobii_controller.LastTimestamp, pressed == 1))
                break

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def stop(self):
        self.run_mouse_checks = False
