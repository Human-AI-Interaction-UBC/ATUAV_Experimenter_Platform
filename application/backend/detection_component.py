from abc import abstractmethod
from tornado import gen
from tornado.ioloop import IOLoop, PeriodicCallback

class DetectionComponent():

    '''
    Abstract class for defining detection components - classes responsible for calculating features
    from raw data and sending them to Application State. Abstracts away all the interactions with
    Tornado framework, providing an intuitive and flexible base for implementing feature extractors.
    '''

    def __init__(self, tobii_controller, adaptation_loop, is_periodic = False, callback_time = 600000):
        '''
        Args:
            tobii_controller - an instance of TobiiController already connected to an eyetracker
            adaptation_loop - instance of AdaptationLoop to send the computed features to Application State
            is_periodic - boolean - true if run() method should be called periodically.
            callback_time (Long) - if is_periodic = True, specifies how often should the run() method be called, in microseconds.
        '''
        self.tobii_controller  = tobii_controller
        self.adaptation_loop = adaptation_loop
        self.application_state_controller = self.adaptation_loop.app_state_controller
        self.is_periodic = is_periodic
        self.callback_time = callback_time

    @abstractmethod
    def notify_app_state_controller(self):
        '''
        Abstract method for sending features to Application State.
        Should be called at the end of execution of run().
        '''
        pass

    @abstractmethod
    def run(self):
        '''
        Abstract method for calculating features from raw data.
        Gets called periodically or once, depending on how the DetectionComponent was initialized.
        '''
        pass

    def start(self):
        '''
        Method for scheduling a run() call in Tornado's IOLoop.
        Depending on how DetectionComponent was initialized, run()
        gets scheduled to run either periodically or once.
        '''
        print("TRYING HERE")
        if (self.is_periodic):
            if (not hasattr(self, "cb")):
                self.cb = PeriodicCallback(callback = self.run, callback_time = self.callback_time)
                self.cb.start()
            else:
                self.cb.start()
        else:
            IOLoop.instance().add_callback(callback = self.run)

    def stop(self):
        '''
        Method for stopping periodic call of the run() method
        '''
        if (self.is_periodic):
            self.cb.stop()
