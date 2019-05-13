from detection_component import DetectionComponent
from tornado import gen
import math
from utils import *
import geometry
import time
from pynput import mouse, keyboard

class MouseKeyboardEventDetector(DetectionComponent):

    def __init__(self, tobii_controller, application_state_controller, emdat_component, use_mouse, use_keyboard):
        DetectionComponent.__init__(self, tobii_controller, application_state_controller, is_periodic = False)
        self.predicted_features = {}
        self.id = 1
        self.emdat_component = emdat_component
        self.listeners = []
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
        print("Constructed the mouse listener")


    def notify_app_state_controller(self, aoi, time_stamp, pressed):
        self.cur_mouse_event_id += 1
        self.application_state_controller.updateMouseTable(aoi, self.cur_mouse_event_id, time_stamp, pressed)
        self.adaptation_loop.evaluateRules(aoi, time_stamp)

    def run(self):
        ## Do something
        print("RUNNING THE MOUSE")
        self.cur_mouse_event_id = 0
        self.AOIS = self.application_state_controller.getMouseAoiMapping()
        for listener in self.listeners:
            listener.start()

    def on_click(self, x, y, button, pressed):
		print('{0} at {1}'.format( 'Pressed' if pressed else 'Released', (x, y)))
		for aoi in self.AOIS:
			if (utils.point_inside_polygon(x, y, self.AOIS[aoi])):
				self.notify_app_state_controller(aoi, self.tobii_controller.LastTimestamp, pressed == 1)
				break

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
