from detection_component import DetectionComponent
from tornado import gen
import math
from utils import *
import geometry
import time
from pynput import mouse, keyboard

class MouseKeyboardEventDetector(DetectionComponent):

    def __init__(self, tobii_controller, app_state_control, emdat_component, use_mouse, use_keyboard):
        DetectionComponent.__init__(self, tobii_controller, app_state_control, is_periodic = False)
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
#            					    on_release=on_release,
								    on_press=self.on_press
                                    ))

    def run(self):
        ## Do something
        """
        ### With self.emdat_component, you have access to interval and task features
        ### With self.tobii_controller, you have access to global features
        predicted_features['your_feature'] = classifier.predict(features_you_need)
        """
        for listener in self.listeners:
			listener.start()
        #self.notify_app_state_controller()
        self.predicted_features = {}
        self.id += 1
        pass

    def notify_app_state_controller(self):
        """
        send features to the database
        """
    # TODO: FIX TIMESTAMP
        for feature in predicted_features.keys():
            if feature in self.feature_select:
                val = "high" if predicted_features['feature'] >= self.threshold else "low"
                self.application_state_controller.updateMlTable(feature, self.id, feature, time.time(), predicted_features[feature], val)

    def on_click(self, x, y, button, pressed):
	    print('{0} at {1}'.format(
	        'Pressed' if pressed else 'Released',
	        (x, y)))

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
