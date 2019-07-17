import tornado
from tornado.options import define, options
import os.path

import sqlite3
import datetime
import json
import random

# Imports required for EYE TRACKING Code:
import time
from application.backend.eye_tracker_newsdk import TobiiControllerNewSdk
from application.middleend.adaptation_loop import AdaptationLoop
from application.application_state_controller import ApplicationStateController
from application.application_web_socket import ApplicationWebSocket

from application.backend.fixation_detector import FixationDetector
from application.backend.emdat_component import EMDATComponent
from application.backend.ml_component import MLComponent
from application.backend.mouse_keyboard_event_detector import MouseKeyboardEventDetector


import params


##########################################

define("port", default=8888, help="run on the given port", type=int)
TOBII_CONTROLLER = "tobii_controller"
APPLICATION_STATE_CONTROLLER = "application_state_controller"
ADAPTATION_LOOP = "adaptation_loop"
FIXATION_ALGORITHM = "fixation_algorithm"
EMDAT_COMPONENT = "emdat_component"
ML_COMPONENT = "ml_component"
MOUSE_KEY_COMPONENT = "mouse_key_component"

class Application(tornado.web.Application):
    def __init__(self):
        #connects url with code

        self.tobii_controller = TobiiControllerNewSdk()
        self.tobii_controller.activate()
        self.app_state_control = ApplicationStateController(0)
        self.adaptation_loop = AdaptationLoop(self.app_state_control)

        self.fixation_component = FixationDetector(self.tobii_controller, self.adaptation_loop)
        self.emdat_component = EMDATComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD)
        self.ml_component = MLComponent(self.tobii_controller, self.adaptation_loop, callback_time = params.EMDAT_CALL_PERIOD, emdat_component = self.emdat_component)
        self.mouse_key_component = MouseKeyboardEventDetector(self.tobii_controller, self.adaptation_loop, self.emdat_component, params.USE_MOUSE, params.USE_KEYBOARD)
        websocket_dict = {TOBII_CONTROLLER: self.tobii_controller,
                         APPLICATION_STATE_CONTROLLER: self.app_state_control,
                         ADAPTATION_LOOP: self.adaptation_loop,
                         FIXATION_ALGORITHM: self.fixation_component,
                         EMDAT_COMPONENT: self.emdat_component,
                         ML_COMPONENT: self.ml_component,
                         MOUSE_KEY_COMPONENT: self.mouse_key_component}
        handlers = [
            (r"/", MainHandler),
            (r"/mmd", MMDHandler),
            (r"/questionnaire", QuestionnaireHandler),
            (r"/resume", ResumeHandler),
            (r"/userID", UserIDHandler),
            (r"/prestudy", PreStudyHandler), (r"/(Sample_bars.png)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
                                             (r"/(Sample_bars_2.png)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
            (r"/sample_MMD", SampleHandler), (r"/(ExampleMMD.png)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
            (r"/sample_Q", SampleHandler2), (r"/(ExampleQ.png)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
            (r"/calibration", CalibrationHandler), (r"/(blank_cross.jpg)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
            (r"/tobii", TobiiHandler),
            (r"/ready", ReadyHandler),
            (r"/done", DoneHandler),
            (r"/final_question", FinalHandler), (r"/(1.png)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
                                                (r"/(2.png)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
                                                (r"/(3.png)", tornado.web.StaticFileHandler, {'path': params.FRONT_END_STATIC_PATH + 'sample/'}),
            (r"/done2", DoneHandler2),
            (r"/websocket", MMDWebSocket, dict(websocket_dict = websocket_dict))
        ]
        #connects to database
        self.conn = sqlite3.connect('database.db')
        #"global variable" to save current UserID of session
        UserID = -1;
        #global variable to track start and end times
        start_time = '';
        end_time = '';
        #where to look for the html files
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), params.FRONT_END_TEMPLATE_PATH),
            static_path=os.path.join(os.path.dirname(__file__), params.FRONT_END_STATIC_PATH),
            debug=True,
        )
        #initializes web app
        tornado.web.Application.__init__(self, handlers, **settings)

class MMDWebSocket(ApplicationWebSocket):

    def open(self):
        self.websocket_ping_interval = 0
        self.websocket_ping_timeout = float("inf")
        self.adaptation_loop.liveWebSocket = self
        # print self.tobii_controller.eyetrackers

        self.start_detection_components()
        self.tobii_controller.startTracking()

    def on_message(self, message):
        print("RECEIVED MESSAGE: " + message)
        if (message == "next_task"):
            self.stop_detection_components()
            self.tobii_controller.stopTracking()
            return
        else:
            self.stop_detection_components()
            self.tobii_controller.stopTracking()
            self.tobii_controller.destroy()
            self.app_state_control.resetApplication(user_id = self.application.cur_user)
            return

    def on_close(self):
        self.app_state_control.logTask(user_id = self.application.cur_user)

class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.application.start_time = str(datetime.datetime.now().time())
        self.render('index.html', mmd="181")

    def post(self):

        q1 = self.get_argument('element_1')
        if(int(q1)==1):
            # self.application.mmd_order = [31, 32, 33, 34, 35, 36,
            #                               181, 182, 183, 184, 185, 186,
            #                               281, 282, 283, 284, 285, 286]
            # conditions = [181, 182, 183,
            #               281, 282, 283]
            conditions = [[181, 281], [182, 282], [183, 283]]
            for intervention in conditions:
                random.shuffle(intervention)
            # self.application.mmd_order = [60]
            # shuffle MMD order
            random.shuffle(conditions)
            self.application.mmd_order = [cond for intervention in conditions for cond in intervention]
            self.application.mmd_index = 0
            self.redirect('/userID')
        else:
            self.redirect('/resume')

    def loadMMDQuestions (self):
        conn = sqlite3.connect('database.db')
        query_results = conn.execute('select * from MMD_questions')

        return json.dumps(query_results.fetchall())


class ResumeHandler(tornado.web.RequestHandler):
    def get(self):
        users_list = self.loadUsersList()
        # print users_list
        self.render('resume.html', users = users_list)

    def loadUsersList (self):
        conn = sqlite3.connect('database.db')
        query_results = conn.execute('select * from user_data ORDER BY user_id DESC')
        user_data = query_results.fetchall()
        user_array = []
        for user in user_data:
            user_array.append(user[0])

        return json.dumps(user_array)

    def post(self):
        userOptions = self.get_argument('userOptions')
        # print 'selected user id',userOptions
        self.application.cur_user = int(userOptions)
        query_results = self.application.conn.execute('select * from study_progress where user_id=' + str(userOptions))
        user_data = query_results.fetchall()

        last_page = []
        if (len(user_data)>0):
            last_page = user_data[len(user_data)-1]

        if last_page[1]=='prestudy':
            self.redirect('/prestudy')

        if last_page[1]=='mmd':
            self.application.cur_mmd = int(last_page[2])
            print ('last mmd',self.application.cur_mmd)

            #find the mmd order for this user
            query_results = self.application.conn.execute('select * from user_data where user_id=' + str(userOptions))
            user_data = query_results.fetchall()

            if (len(user_data)>0):
                self.application.mmd_order = eval(user_data[0][2])
                print (self.application.mmd_order)
                counter = 0
                for mmd in self.application.mmd_order:
                    print (mmd)
                    if int(mmd)== self.application.cur_mmd:
                        self.application.mmd_index = counter+1
                        print ('mmd_index', self.application.mmd_index)
                        self.redirect('/mmd')
                    counter+=1
            else:
                print ('ERROR! Cannot resule this user')

class QuestionnaireHandler(tornado.web.RequestHandler):
    def get(self):
        #displays contents of index.html
        # print 'questionnaire handler'
        self.application.start_time = str(datetime.datetime.now().time())
        mmdQuestions = self.loadMMDQuestions()
        noofMMD = len(self.application.mmd_order)
        progress = str(self.application.mmd_index)+ ' of '+ str(noofMMD)
        if (self.application.mmd_index % 2 == 0):
            self.render('questionnaire.html', mmd=self.application.cur_mmd, progress = progress, questions = mmdQuestions)
        else:
            self.redirect('/mmd')

        print("finished rendering qustionnaire")

    def post(self):
        print ('post')
        answers = self.get_argument('answers')
        # print answers

        answers = json.loads(answers)

        # print answers

        self.application.end_time = str(datetime.datetime.now().time())
        questionnaire_data = [
        self.application.cur_user, self.application.cur_mmd, self.application.start_time, self.application.end_time]

        task_data = (self.application.cur_user, self.application.cur_mmd,'questions' ,self.application.start_time, self.application.end_time)
        self.application.conn.execute('INSERT INTO MMD_performance VALUES (?,?,?,?,?)', task_data)
        self.application.conn.commit()

        i =1
        for a in answers:
            #questionnaire_data.append(a)
            answer_data = (self.application.cur_user, self.application.cur_mmd,i, a[0],a[1])
            # print 'question results:'
            # print answer_data
            self.application.conn.execute('INSERT INTO Questions_results VALUES (?,?,?,?,?)', answer_data)
            i = i+1

        #print tuple(questionnaire_data)


        self.application.conn.commit()

        self.application.conn.execute('INSERT INTO Study_progress VALUES (?,?,?,?)', [  self.application.cur_user,'mmd' ,self.application.cur_mmd, str(datetime.datetime.now().time())])
        self.application.conn.commit()
        #refers to database connected to in 'class Application'
        #database = self.application.db.database
        #empty entry to insert into database in order to generate a user id
        #entry = {}
        #inserts empty entry and saves it to UserID variable in 'class Application'
        #self.application.UserID = database.insert_one(entry).inserted_id
        #print self.application.UserID

        self.redirect('/mmd')

    def loadMMDQuestions (self):
        conn = sqlite3.connect('database_questions_pilot.db')
        query_results = conn.execute('select * from MMD_questions where mmd_id='+str(self.application.cur_mmd))

        # hard-coded two questions as they appear in all mmds
        questions = []

        # for pilot only
        questions.append([self.application.cur_mmd, "1", "The underline and link intervention was helpful.", "Likert", "Subjective"])

        # questions.append([self.application.cur_mmd, "2", "The snippet I read was easy to understand.", "Likert", "Subjective"])

        # questions.append([self.application.cur_mmd, "2", "I would be interested in reading the full article.", "Likert", "Subjective"])

        questions.extend(query_results.fetchall())

        return json.dumps(questions)

class MMDHandler(tornado.web.RequestHandler):
    def get(self):
        #displays contents of index.html
        self.application.start_time = str(datetime.datetime.now().time())
        print ('mmd order',self.application.mmd_order, self.application.mmd_index)
        if self.application.mmd_index<len(self.application.mmd_order):
            self.application.cur_mmd = self.application.mmd_order[self.application.mmd_index]

            if (self.application.show_question_only):
                self.redirect('/questionnaire')
            else:
                self.render('MMDExperimenter.html', mmd=str(self.application.cur_mmd))
            self.application.mmd_index+=1
        else:
            self.redirect('/done')

    def post(self):
        #refers to database connected to in 'class Application'
        #database = self.application.db.database
        #empty entry to insert into database in order to generate a user id
        #entry = {}
        #inserts empty entry and saves it to UserID variable in 'class Application'
        #self.application.UserID = database.insert_one(entry).inserted_id
        #print self.application.UserID

        #self.application.cur_user = random.randint(0, 1000)  #random number for now
        print ("POST RECEIVED")
        self.application.end_time = str(datetime.datetime.now().time())
        task_data = (self.application.cur_user, self.application.cur_mmd,'mmd' ,self.application.start_time, self.application.end_time)
        self.application.conn.execute('INSERT INTO MMD_performance VALUES (?,?,?,?,?)', task_data)
        self.application.conn.commit()
        self.redirect('/questionnaire')


class UserIDHandler(tornado.web.RequestHandler):
    def get(self):
        #gets time upon entering form
        self.application.start_time = str(datetime.datetime.now().time())
        #display contents of prestudy.html
        self.application.show_question_only = 0
        self.render("userid.html")
    def post(self):
        #gets time upon completing form
        self.application.end_time = str(datetime.datetime.now().time())
        #get contents submitted in the form for prestudy
        self.application.cur_user = self.get_argument('userID')

        # store the new userID
        user_data = [self.application.cur_user, str(self.application.start_time), str(self.application.mmd_order)]
        self.application.conn.execute('INSERT INTO User_data VALUES (?,?,?)', user_data)
        self.application.conn.commit()

        # self.redirect('/prestudy') FOR TEST
        self.redirect('/mmd')

class PreStudyHandler(tornado.web.RequestHandler):
    def get(self):
        #gets time upon entering form
        self.render("prestudy.html")
    def post(self):

        #get contents submitted in the form for prestudy
        q1 = self.get_argument('age')
        q2 = self.get_argument('gender')
        q3 = self.get_argument('occupation')
        q4 = self.get_argument('field')
        q5 = self.get_argument('first_language')
        q6 = self.get_argument('pref_language')
        q7 = self.get_argument('enlish_proficiency')
        q8 = self.get_argument('read_freq')
        q9 = self.get_argument('distrcted')
        q10 = self.get_argument('complex_bar')

        pre_data = [self.application.cur_user, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        self.application.conn.execute('INSERT INTO prestudy VALUES (?,?,?,?,?,?,?,?,?,?,?)', pre_data)
        self.application.conn.commit()

        self.redirect('/sample_MMD')

class SampleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("sample_mmd.html")
    def post(self):
        self.redirect('/sample_Q')

class SampleHandler2(tornado.web.RequestHandler):
    def get(self):
        self.render("sample_questionnaire.html")
    def post(self):
        self.redirect('/tobii')

class TobiiHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("load_tobii.html")
    def post(self):
        self.redirect('/calibration')

class CalibrationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("calibration.html")
    def post(self):
        self.redirect('/ready')

class ReadyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ready.html")
    def post(self):
        self.redirect('/mmd')

class DoneHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("done.html")
    def post(self):
        self.redirect('/final_question')

class FinalHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("final_question.html")
    def post(self):
        q1 = self.get_argument('viz_pref')

        pre_data = [self.application.cur_user, q1]
        self.application.conn.execute('INSERT INTO final_question VALUES (?,?)', pre_data)
        self.application.conn.commit()

        self.redirect('/done2')

class DoneHandler2(tornado.web.RequestHandler):
    def get(self):
        self.render("done2.html")

#main function is first thing to run when application starts
def main():
    tornado.options.parse_command_line()
    #Application() refers to 'class Application'
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
