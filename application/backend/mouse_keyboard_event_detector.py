from detection_component import DetectionComponent
from tornado import gen
import params

import math
import utils
import geometry
import time
from pynput import mouse, keyboard
import Queue
from tornado.ioloop import IOLoop
from mouse_events import *


class MouseKeyboardEventDetector(DetectionComponent):

    def __init__(self, tobii_controller, application_state_controller, emdat_component, use_mouse, use_keyboard):
        DetectionComponent.__init__(self, tobii_controller, application_state_controller, is_periodic = False)
        self.predicted_features = {}
        self.emdat_component = emdat_component
        self.listeners = []
        if use_mouse:
            self.last_press = None
            self.min_drag_drop_dur = 0
            self.min_drag_drop_dist = 0
            self.mouse_queue = Queue.Queue()
            self.double_click_queue = Queue.Queue()
            self.keyboard_queue = Queue.Queue()
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
                click = self.mouse_queue.get()
                print("Click at", click.x, ", ", click.y)
                self.cur_mouse_event_id += 1
                self.application_state_controller.updateMouseTable(click.aoi, self.cur_mouse_event_id, click)
                self.adaptation_loop.evaluateRules(click.aoi, click.time_stamp)
            elif self.double_click_queue.qsize() > 0:
                double_click = self.double_click_queue.get()
                self.cur_doubleclick_event_id += 1
                if double_click.aoi is not None:
                    self.application_state_controller.updateDoubleClickTable(double_click.aoi, self.cur_doubleclick_event_id, double_click)
                    self.adaptation_loop.evaluateRules(double_click.aoi, double_click.time_stamp)
            elif self.keyboard_queue.qsize() > 0:
                key_event = self.keyboard_queue.get()
                self.keyboard_event_id += 1
                self.application_state_controller.updateKeyboardTable("ref_keyboard", self.keyboard_event_id, key_event)
                self.adaptation_loop.evaluateRules("ref_keyboard", key_event.time_stamp)
            else:
                yield

    def run(self):
        ## Do something
        print("RUNNING THE MOUSE")
        self.cur_mouse_event_id = 0
        self.cur_doubleclick_event_id = 0
        self.keyboard_event_id = 0
        self.last_release = None
        self.AOIS = self.application_state_controller.getMouseAoiMapping()
        print("AOIS in mouse: ", self.AOIS)
        for listener in self.listeners:
            listener.start()

    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format( 'Pressed' if pressed else 'Released', (x, y)))
        print(self.tobii_controller.LastTimestamp)
        this_click = BasicMouseEvent(aoi=None, x=x, y=y, is_press=(pressed == 1), time_stamp=self.tobii_controller.LastTimestamp)
        for aoi in self.AOIS:
            if (utils.point_inside_polygon(x, y, self.AOIS[aoi])):
                this_click.aoi = aoi
                self.mouse_queue.put(this_click)
                break
        if not pressed:
            if self.last_release is not None:
                curr_timestamp = self.tobii_controller.LastTimestamp
                clicks_time_difference = curr_timestamp - self.last_release.time_stamp
                if clicks_time_difference < params.MAX_DOUBLE_CLICK_DUR:
                    self.double_click_queue.put(DoubleClickMouseEvent(x=self.last_release.x, y=self.last_release.y, time_stamp=self.last_release.time_stamp, aoi=self.last_release.aoi, is_first_click=False))
                    self.double_click_queue.put(DoubleClickMouseEvent(x=this_click.x, y=this_click.y, time_stamp=this_click.time_stamp, aoi=this_click.aoi, is_first_click=True))
            self.last_release = this_click

    def on_press(self, key):
        try:
            self.keyboard_queue.put(KeyboardEvent(key.char, self.tobii_controller.LastTimestamp))
        except AttributeError:
            pass
            #self.keyboard_queue.put(KeyboardEvent(key, self.tobii_controller.LastTimestamp))

    def stop(self):
        self.run_mouse_checks = False
