import sys, os
import tobii_research as tr
from websocket_client import EyetrackerWebsocketClient
from SimulationSocket import SimulationSocket
import subprocess

sys.path.append('E:\\Users\\admin\\Desktop\\experimenter_platform_core\\ATUAV_Experimenter_Platform\\Modules')
sys.path.append(os.path.join(sys.path[0],'tobii_binder'))

# Parent eyetracker class
class EyeTracker(object):
    def __init__(self, tracker_type):
        self.tracker_type = tracker_type
    
    def activate(self, tobii_controller):
        print("connecting to default (Tobii 4c) eye tracker")
        subprocess.Popen("application/backend/websocket_app/GazeServer.exe")
        self.websocket_client = EyetrackerWebsocketClient(tobii_controller)
    

    def start_tracking(self, tobii_controller):
        self.websocket_client.start_tracking()

    def stop_tracking(self, tobii_controller):
        self.websocket_client.stop_tracking()


# Tobii T120 (old eyetracker) implemetation
class TobiiT120EyeTracker(EyeTracker):
    def __init__(self):
        super(TobiiT120EyeTracker, self).__init__("Tobii T120")
        self.eyetracker = None
        self.eyetrackers = {}
    
    def activate(self, tobii_controller):
        print("connecting to TobiiT120 eyetracker")
        while self.eyetracker is None:
            eyetrackers = tr.find_all_eyetrackers()
            for tracker in eyetrackers:
                self.eyetrackers[tracker.model] = tracker
            self.eyetracker = self.eyetrackers.get(self.tracker_type, None)
    

    def start_tracking(self, tobii_controller):
        self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, tobii_controller.on_gazedata, as_dictionary=True)

    def stop_tracking(self, tobii_controller):
        self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, tobii_controller.on_gazedata)


# 4C implementation
class Tobii4CEyeTracker(EyeTracker):
    def __init__(self):
        super(Tobii4CEyeTracker, self).__init__("IS4_Large_Peripheral")


# Simulation implementation
class SimulationEyeTracker(EyeTracker):
    def __init__(self):
        super(SimulationEyeTracker, self).__init__("simulation")
    
    def activate(self, tobii_controller):
        self.websocket_client = SimulationSocket(tobii_controller)
        print("connected to simulation eye tracker")