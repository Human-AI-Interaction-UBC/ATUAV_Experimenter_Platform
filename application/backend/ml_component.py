from detection_component import DetectionComponent
from tornado import gen
import math
from utils import *
import geometry
import time



class MLComponent(DetectionComponent):

    def __init__(self, tobii_controller, app_state_control, callback_time, emdat_component):
        DetectionComponent.__init__(self, tobii_controller, app_state_control, is_periodic=True,
                                    callback_time=callback_time)
        self.predicted_features = {}
        self.id = 1
        self.emdat_component = emdat_component
        self.feature_select = self.application_state_controller.getMLFeatures()
        self.threshold = 0.5
        """
        classifier = YourClassifier()
        classifier.loadModelParameters()
        """

    def run(self):
        ## Do something
        """
        ### With self.emdat_component, you have access to interval and task features
        ### With self.tobii_controller, you have access to global features
        predicted_features['your_feature'] = classifier.predict(features_you_need)
        """
        self.notify_app_state_controller()
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
                self.application_state_controller.updateMlTable(feature, self.id, feature, time.time(),
                                                                predicted_features[feature], val)




    """
    
    need to have a nested dictionary of models:
    first level  : target variable names (e.g. cognitive abilities)
    second level : prediction type (e.g. across, within)
    third level  : windows (dict of window - model pairs) 
    
    [can only specify model for windows where change of model is required 
    otherwise the platform should keep using the previous model]
    
    models = {
        'VisLit': {
            'across': {1: model_1, 3: model_3, ...},
            'within': {1: model_1, 2: model_2, ...},
            }
        'ReadP': {
            'across': {1: model_1, 4: model_4, ...},
            'within': {1: model_1, 26: model_26, ...},
            }
            ...
    }
    
    
    need to know get prediction type, current window
    model_to_use = models[target][prediction_type][window]
    
    if models[target][prediction_type][window] does not exist -> keep using the previous model
    """
