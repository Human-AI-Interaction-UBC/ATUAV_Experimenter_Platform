
from eye_tracker import TobiiController
from fixation_detector import FixationDetector
from emdat_component import EMDATComponent


class ExperimenterPlatform():

    def __init__(self):
        ## Initialize eye tracker
        self.tobii_controller = TobiiController()
        self.websocket = set()
        self.tobii_controller.waitForFindEyeTracker()
        self.tobii_controller.activate(self.tobii_controller.eyetrackers.keys()[0])
        # Initialize detection components
        self.fixation_detector = FixationDetector(self.tobii_controller)
        self.emdat_component = EMDATComponent(self.tobii_controller, True)

    def initialize_platform(self, features, AOIs):
        # Start all components
        self.tobii_controller.startTracking()
        self.fixation_detector.start()
        self.emdat_component.start()

    def switch_task(self, features, AOIs):
        pass
