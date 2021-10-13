
EYETRACKERS = {
    0: "Tobii Pro X3-120 EPU",
    1: "4C eyetracker",
    2: "IS4_Large_Peripheral"
}
EYETRACKER_TYPE = EYETRACKERS[1]

#Pilot condition
PILOT_CONDITION_TEXT_INTERVENTION = True
PILOT_CONDITION_NO_REMOVAL = True
#PILOT_CONDITION_NO_REMOVAL = False

#PILOT mmd subset to load
#PILOT_MMD_SUBSET = [3,9,11,20,27,60,74] #try and ensure 74 is in removal
#PILOT_MMD_SUBSET = [5,28,30,62,66,72,76]
PILOT_MMD_SUBSET = [5]

# Project paths:
# Reference highlighting rules
#RUN USING:  python -u experimenter_platform_stage_1_demo.py
if PILOT_CONDITION_TEXT_INTERVENTION:
    # USER_MODEL_STATE_PATH = "./database/user_model_state_ref_highlight.db"
    USER_MODEL_STATE_PATH = "./database/user_model_state_ref_highlight_ml_new.db"
else:
    USER_MODEL_STATE_PATH = "./database/user_model_state_ref_highlight.db"


# GAZE_EVENT_RULES_PATH = "./database/gaze_event_rules_ref_highlight_and_text.db"
if PILOT_CONDITION_TEXT_INTERVENTION:
    GAZE_EVENT_RULES_PATH = "./database/gaze_event_rules_ref_highlight_and_text_pilot_noremoval.db"
else:
    if PILOT_CONDITION_NO_REMOVAL:
        GAZE_EVENT_RULES_PATH = "./database/gaze_event_rules_ref_highlight_pilot_noremoval_test.db"
    else:
        GAZE_EVENT_RULES_PATH = "./database/gaze_event_rules_ref_highlight_pilot_removal.db"


# Project paths:
# Reference highlighting rules - SD testing
#RUN USING:  python -u experimenter_platform_study_bars_SD.py
#USER_MODEL_STATE_PATH = "./database/user_model_state_ref_highlight_SD.db"
#GAZE_EVENT_RULES_PATH = "./database/gaze_event_rules_ref_highlight_SD_bold1.db"

# Legend highlighting rules
#RUN USING:  python -u experimenter_platform_study_1.py
#GAZE_EVENT_RULES_PATH = "./database/gaze_event_rules_legend_highlighting.db"
#USER_MODEL_STATE_PATH = "./database/user_model_state_legend_highlighting.db"

FRONT_END_STATIC_PATH = "./application/frontend/static/"
FRONT_END_TEMPLATE_PATH = "./application/frontend/templates/"

# Platform configuration:
USE_FIXATION_ALGORITHM = True
USE_EMDAT = True
USE_ML = True
USE_KEYBOARD = False
USE_MOUSE = False


# Features to use
USE_PUPIL_FEATURES = False
USE_DISTANCE_FEATURES = False
USE_FIXATION_PATH_FEATURES = True
USE_TRANSITION_AOI_FEATURES = True

# Sets of features to keep
KEEP_TASK_FEATURES = True
KEEP_GLOBAL_FEATURES = True

#Frequency of ML/EMDAT calls:
EMDAT_CALL_PERIOD = 1000
ML_CALL_PERIOD = 1000

# Prediction setup
PREDICTION_SETUP = ['within', 'across'][0]

# Some parameter from EMDAT
MAX_SEG_TIMEGAP= 10

# Fixation detector parameters
FIX_MAXDIST = 35
FIX_MINDUR = 100000

REST_PUPIL_SIZE = 0
PUPIL_ADJUSTMENT = "rpscenter"

# The amount of time to wait after starting a new task before starting recording
# fixations (to account for html loading time)
FIX_DETECTION_DELAY = 1000000

#Logs configuration
LOG_PREFIX = "./log/AdaptiveMSNV_log"

# Mouse events
MAX_DOUBLE_CLICK_DUR = 500000
