from application.backend.detection_component import DetectionComponent
import numpy as np
import os
import json
import joblib
from application.backend.ml_module.ml_utils import filter_features
from ml_params import across_task_models, within_task_models
import time
import pandas as pd


class MLComponent(DetectionComponent):

    def __init__(self, tobii_controller, app_state_control, callback_time, emdat_component, prediction_type):

        # With self.emdat_component, you have access to interval and task features
        # With self.tobii_controller, you have access to global features

        DetectionComponent.__init__(self, tobii_controller, app_state_control, is_periodic=True,
                                    callback_time=callback_time)
        # self.predictions = {}
        self.record_id = 1
        self.start_time = int(time.time())
        self.emdat_component = emdat_component
        self.prediction_type = prediction_type
        # self.emdat_raw = self.tobii_controller.emdat_global_features
        # self.ml_features = self.application_state_controller.getMLFeatures()

        print("CONSTRUCTED NEW ML OBJECT")

        # model = joblib.load('application//backend//ml_module//ml_models//within//verbalwm//2_LR.joblib')

        # loading models based on prediction_type
        self.prediction_type = prediction_type
        if self.prediction_type == 'across':
            self.models = self.load_models(across_task_models)
        elif self.prediction_type == 'within':
            self.models = self.load_models(within_task_models)

        print("all models successfully loaded!")

        # print(self.ml_features)
        # print('emdat_raw', self.emdat_raw)

    # -------------------------------------------------------------------
    def restructure_features(self, features):
        new_features = {}
        for key in features.keys():
            if isinstance(features[key], dict):
                for inner_key in features[key].keys():
                    new_features['{}_{}'.format(key, inner_key)] = features[key][inner_key]
            else:
                new_features[key] = features[key]
        return new_features

    # -------------------------------------------------------------------
    def load_models(self, models):

        """
        loads models and features from files
        """
        loaded_models = {}
        for measure, best_windows in models.items():
            loaded_models[measure] = {}
            for window, (model_path, features_path) in best_windows.items():

                if features_path is not None:
                    if features_path.split('.')[-1] == 'json':
                        with open(features_path, 'r') as fp:
                            features = json.load(fp)
                    else:
                        raise NameError('(features) was not a json file')

                if model_path.split('.')[-1] == 'joblib':
                    # print(model_path)

                    # model = 1
                    model = joblib.load(model_path)
                    # model = joblib.load(model_path)
                    print('{} loaded'.format(model_path))

                loaded_models[measure][window] = (model, features)

        return loaded_models

    # -------------------------------------------------------------------
    def predict(self, emdat_features):
        """[summary]

        Args:
            emdat_features (pd.DataFrame): [EMDAT features]
            current_window (int): [current window of interaction]

        Returns:
            [dict]: [predictions]
        """
        self.predictions = {}
        for measure, best_windows in self.models.items():
            if self.current_window in best_windows:
                # start_time = time.time()
                self.predictions[measure] = {}
                loaded_model = self.models[measure][self.current_window][0]
                features = self.models[measure][self.current_window][1]

                emdat_features = pd.DataFrame(self.restructure_features(emdat_features), index=[0])
                # emdat_features.to_csv('emdat_features.csv')
                emdat_features = emdat_features.fillna(-1)
                # filtered_emdat_features = filter_features(
                #     emdat_features, prediction_type='within', window_size=1000, slice=current_window)
                X = emdat_features[features]
                start_time = time.time()
                y_pred = loaded_model.predict(X)[0]
                # print("Complete Prediction execution --- %.12f seconds --- \n" % (time.time() - start_time))
                self.predictions[measure]['window'] = self.current_window
                self.predictions[measure]['prediction'] = y_pred

                try:
                    # y_prob = 0
                    y_prob = loaded_model.predict_proba(X)[0].max()
                    self.predictions[measure]['prediction_prob'] = y_prob
                except:
                    self.predictions[measure]['prediction_prob'] = None

        return self.predictions

    # -------------------------------------------------------------------
    def notify_app_state_controller(self):

        if self.predictions != {}:

            for measure in self.predictions.keys():
                window = self.predictions[measure]['window']
                predicted_label = self.predictions[measure]['prediction']
                prediction_prob = self.predictions[measure]['prediction_prob']

                print(window, measure, predicted_label, prediction_prob)

                timestamp = int(time.time() * 1000)

                self.application_state_controller.updateMlTable(measure, self.record_id, timestamp,
                                                                prediction_prob, predicted_label)
                self.record_id += 1

    # -------------------------------------------------------------------

    def run(self):

        start_time = time.time()
        # current_time = int(time.time())
        # current_window = current_time - self.start_time
        self.current_window = self.emdat_component.id
        print('current window: ', self.current_window)

        if self.prediction_type == 'within':
            features = self.emdat_component.emdat_task_features
        elif self.prediction_type == 'across':
            features = self.emdat_component.tobii_controller.emdat_global_features

        self.predict(features)
        self.notify_app_state_controller()


        print("Complete ML execution --- %.12f seconds --- \n\n" % (time.time() - start_time))


def main():
    mlc = MLComponent(DetectionComponent)
