# paths to models and their associated data
path_to_across_models = 'application//backend//ml_module//ml_models//across'
path_to_within_models = 'application//backend//ml_module//ml_models//within'

# --------------------------------------------------------------
# a dict of dicts: for each measure, provide a key-val pair where the key is the window and the value 
# is a pair of paths to the model to be used for that window (.sav file) and its features
# e.g., 'vislit': {window: (path_to_model, path_to_model_features)}
# --------------------------------------------------------------

across_task_models = {

    'vislit': {
        2: ('{}//vislit//2_LR.joblib'.format(path_to_across_models),
            '{}//vislit//2_LR_features.json'.format(path_to_across_models)),

        3: ('{}//vislit//3_LR.joblib'.format(path_to_across_models),
            '{}//vislit//3_LR_features.json'.format(path_to_across_models)),
    },

    'readp': {
        2: ('{}//readp//2_LR.joblib'.format(path_to_across_models),
            '{}//readp//2_LR_features.json'.format(path_to_across_models)),

        3: ('{}//readp//3_LR.joblib'.format(path_to_across_models),
            '{}//readp//3_LR_features.json'.format(path_to_across_models)),
    },

    'verbalwm': {
        2: ('{}//verbalwm//2_LR.joblib'.format(path_to_across_models),
            '{}//verbalwm//2_LR_features.json'.format(path_to_across_models)),

        3: ('{}//verbalwm//3_LR.joblib'.format(path_to_across_models),
            '{}//verbalwm//3_LR_features.json'.format(path_to_across_models)),
    }
}

# --------------------------------------------------------------

within_task_models = {

    'vislit': {
        2: ('{}//vislit//2_LR.joblib'.format(path_to_within_models),
            '{}//vislit//2_LR_features.json'.format(path_to_within_models)),

        3: ('{}//vislit//3_LR.joblib'.format(path_to_within_models),
            '{}//vislit//3_LR_features.json'.format(path_to_within_models)),
    },

    'readp': {
        2: ('{}//readp//2_LR.joblib'.format(path_to_within_models),
            '{}//readp//2_LR_features.json'.format(path_to_within_models)),

        3: ('{}//readp//3_LR.joblib'.format(path_to_within_models),
            '{}//readp//3_LR_features.json'.format(path_to_within_models)),
    },

    'verbalwm': {
        2: ('{}//verbalwm//2_LR.joblib'.format(path_to_within_models),
            '{}//verbalwm//2_LR_features.json'.format(path_to_within_models)),

        3: ('{}//verbalwm//3_LR.joblib'.format(path_to_within_models),
            '{}//verbalwm//3_LR_features.json'.format(path_to_within_models)),
    },

    'taskcomp': {
        2: ('{}//taskcomp//2_LR.joblib'.format(path_to_within_models),
            '{}//taskcomp//2_LR_features.json'.format(path_to_within_models)),

        3: ('{}//taskcomp//3_LR.joblib'.format(path_to_within_models),
            '{}//taskcomp//3_LR_features.json'.format(path_to_within_models)),
    },

    'tasktime': {
        2: ('{}//tasktime//2_LR.joblib'.format(path_to_within_models),
            '{}//tasktime//2_LR_features.json'.format(path_to_within_models)),

        3: ('{}//tasktime//3_LR.joblib'.format(path_to_within_models),
            '{}//tasktime//3_LR_features.json'.format(path_to_within_models)),
    }
}

# --------------------------------------------------------------
