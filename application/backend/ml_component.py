from detection_component import DetectionComponent
from tornado import gen
import math
from utils import *
import geometry
import time
import joblib
from sklearn.ensemble import RandomForestClassifier
class MLComponent(DetectionComponent):

    def __init__(self, tobii_controller, app_state_control, callback_time, emdat_component):
        DetectionComponent.__init__(self, tobii_controller, app_state_control, is_periodic=True,
                                    callback_time=callback_time)
        self.predicted_features = {}
        self.id = 1
        self.emdat_component = emdat_component
        # for now, only visual literacy is concerned
        self.feature_select = self.application_state_controller.getMLFeatures()
        self.threshold = 0.5
        self.predictor = {}
        self.feature_names = {}
        print("ml created")
        self.load_predictor()
        print("predictor done")

    def load_predictor(self):
        # load multiple classifiers, for now the only 'feature' is vislit
        for feature in self.feature_select:
            self.predictor[feature] = joblib.load(
                "./application/backend/classifiers/classifier_" + str(feature) + ".joblib")
            self.feature_names[feature] = joblib.load(
                "./application/backend/classifiers/feature_names_" + str(feature) + ".joblib")
            print(str(feature) + " done")

    def run(self):
        ## Do something
        """
        ### With self.emdat_component, you have access to interval and task features
        ### With self.tobii_controller, you have access to global features
        predicted_features['your_feature'] = classifier.predict(features_you_need)
        """
        for label in self.feature_select:
            if label in self.predictor:
                estimator = self.predictor[label]
                features = self.feature_names[label]
                emdat_raw = self.tobii_controller.emdat_global_features
                X = []
                for feature in features:
                    # AOI features
                    if '_' in feature:
                        aoi_name = feature.split('_', 1)[0]
                        aoi_feature = feature.split('_', 1)[1]
                        if aoi_name not in emdat_raw:
                            X.append(-1)
                        elif aoi_feature not in emdat_raw[aoi_name]:
                            X.append(-1)
                        else:
                            X.append(emdat_raw[aoi_name][aoi_feature])
                    # non-AOI
                    else:
                        if feature not in emdat_raw:
                            X.append(-1)
                        else:
                            X.append(emdat_raw[feature])
                prediction = estimator.predict([X])[0]
                self.predicted_features[label] = prediction
        self.notify_app_state_controller()
        self.id += 1

    def notify_app_state_controller(self):
        """
        send features to the database
        """
    # TODO: FIX TIMESTAMP
        # update dynamic tables by inserting a row of prediction result into corresponding table
        for feature in self.predicted_features.keys():
            if feature in self.feature_select:
                val = "high" if self.predicted_features[feature] >= self.threshold else "low"
                print("run " + str(self.id))
                print(val)
                print(self.predicted_features[feature])
                timestamp = int(time.time() * 1000)
                self.application_state_controller.updateMlTable(feature, self.id, timestamp,
                                                                self.predicted_features[feature], val)
                self.adaptation_loop.evaluateRules(feature, timestamp)