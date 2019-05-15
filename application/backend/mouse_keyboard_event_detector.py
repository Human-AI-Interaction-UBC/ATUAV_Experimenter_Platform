from detection_component import DetectionComponent
from tornado import gen
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
        	self.drag_drop_queue = Queue.Queue()
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
				print("MOUSE click in AOI: ", click.aoi)
				self.cur_mouse_event_id += 1
				self.application_state_controller.updateMouseTable(click.aoi, self.cur_mouse_event_id, click)
				self.adaptation_loop.evaluateRules(click.aoi, click.time_stamp)
			elif self.drag_drop_queue.qsize() > 0:
				# TODO: Figure out what to do with drag/drops outside of AOIs
				drag_drop = self.mouse_queue.get()
        		self.cur_dragdrop_event_id += 1
				self.application_state_controller.updateDragDropTable(drag_drop.aoi, self.cur_dragdrop_event_id, drag_drop)
				self.adaptation_loop.evaluateRules(drag_drop.aoi, drag_drop.time_stamp)
            else:
                yield

    def run(self):
        ## Do something
        print("RUNNING THE MOUSE")
        self.cur_mouse_event_id = 0
        self.cur_dragdrop_event_id = 0
        self.AOIS = self.application_state_controller.getMouseAoiMapping()
        print("AOIS in mouse: ", self.AOIS)
        for listener in self.listeners:
            listener.start()

    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format( 'Pressed' if pressed else 'Released', (x, y)))
		this_click = BasicMouseEvent(aoi=None, x=x, y=y, is_press=(pressed == 1), time_stamp=self.tobii_controller.LastTimestamp)
        for aoi in self.AOIS:
            if (utils.point_inside_polygon(x, y, self.AOIS[aoi])):
				this_click.aoi = aoi
                self.mouse_queue.put(this_click)
                break
		if pressed:
			self.last_press = this_click
		else:
			distance_to_press = utils.euclidean_distance((x, y), (self.last_press.x, self.last_press.y))
			curr_timestamp = self.tobii_controller.LastTimestamp
			time_since_press = curr_timestamp - self.last_press.time_stamp
			if time_since_press > self.min_drag_drop_dur and distance_to_press > self.min_drag_drop_dist:
				self.drag_drop_queue.put(DragDropMouseEvent(self.last_press.time_stamp, time_since_press, distance_to_press, drag_start=True, aoi=last_press.aoi))
				self.drag_drop_queue.put(DragDropMouseEvent(curr_timestamp, time_since_press, distance_to_press, drag_start=False, aoi=this_click.aoi))
			self.last_press = None

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def stop(self):
        self.run_mouse_checks = False
