import tornado
from tornado.options import define, options
import os.path

import sqlite3
import datetime
import json
import random

# Imports required for EYE TRACKING Code:
import time
from application.backend.eye_tracker import TobiiController
from application.middleend.adaptation_loop import AdaptationLoop
from application.application_state_controller import ApplicationStateController
from application.application_web_socket import ApplicationWebSocket
from application.backend.fixation_detector import FixationDetector

import params

##########################################

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        # connects url with code
        handlers = [
            (r"/", MainHandler),
            (r"/locus", LocusHandler),
            (r"/prestudy", PreStudyHandler),
            (r"/fixation", FixationHandler),
            (r"/mmd", MMDHandler),
            (r"/MMDIntervention", MMDInterventionHandler),
            (r"/questionnaire", QuestionnaireHandler),
            (r"/saveCoordinates", AjaxHandler),
            (r"/resume", ResumeHandler),
            (r"/websocket", WebSocketHandler),

        ]
        # connects to database
        self.conn = sqlite3.connect('database.db')
        # "global variable" to save current UserID of session
        UserID = -1
        # global variable to track start and end times
        start_time = ''
        end_time = ''
        # where to look for the html files
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "application/frontend/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "application/frontend/static"),
            debug=True,
        )
        # initializes web app
        tornado.web.Application.__init__(self, handlers, **settings)


# each ____Handler is associated with a url
# def get is for when a http get request is made to the url
# def post is for when a http post request is made to the url(ex: form is submitted)

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        self.websocket_ping_interval = 0
        self.websocket_ping_timeout = float("inf")
        self.app_state_control = ApplicationStateController(30)
        self.adaptation_loop = AdaptationLoop(self.app_state_control)
        self.adaptation_loop.liveWebSocket = self

        self.tobii_controller = TobiiController()
        self.tobii_controller.waitForFindEyeTracker()
        # self.initialize_detection_components()
        print self.tobii_controller.eyetrackers

        self.tobii_controller.activate(self.tobii_controller.eyetrackers.keys()[0])
        self.tobii_controller.startTracking()
        self.fixation_component = FixationDetector(self.tobii_controller, self.adaptation_loop)

        self.start_detection_components()
        print "tracking started"

    def start_detection_components(self):
        if (params.USE_FIXATION_ALGORITHM):
            self.fixation_component.restart_fixation_algorithm()
            self.fixation_component.start()


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.application.start_time = str(datetime.datetime.now().time())
        # self.application.cur_user = 100
        print 'hello'
        # mmdQuestions = self.loadMMDQuestions()

        # self.render('index.html', mmd="3")
        # self.render('mmd.html', mmd="3")
        # self.render('mmd.html', mmd="3")

        self.render('MMDIntervention.html', mmd="30")
        # self.render('questionnaire.html', mmd="3", questions = mmdQuestions)

    def post(self):

        ##### TODO ######

        # 1)generate userid
        # 2)login with old userid

        q1 = self.get_argument('element_1')
        print q1
        if int(q1) == 1:  # generate new userid
            # query_results = self.application.conn.execute('SELECT * FROM User_data ORDER BY user_id DESC LIMIT 1')
            # rows =  query_results.fetchall()
            # print 'new user id'
            # print int(rows[0][0])+1 # maximum valued ID
            # self.application.cur_user = int(rows[0][0])+1
            self.application.mmd_order = [3, 5, 9, 11, 18, 20, 27, 28, 30, 60, 62, 66, 72, 74, 76]  # removed MMD 73
            # random.shuffle(self.application.mmd_order)
            print self.application.mmd_order
            self.application.mmd_index = 0

            # self.redirect('/mmd')

            self.redirect('/prestudy')
        else:
            self.redirect('/resume')

    def loadMMDQuestions(self):
        conn = sqlite3.connect('database.db')
        query_results = conn.execute('select * from MMD_questions')

        return json.dumps(query_results.fetchall())
        # query_results
        # OR

        # query_results.fetchone()


class ResumeHandler(tornado.web.RequestHandler):
    def get(self):
        users_list = self.loadUsersList()
        print users_list
        self.render('resume.html', users=users_list)

    def loadUsersList(self):
        conn = sqlite3.connect('database.db')
        query_results = conn.execute('select * from user_data ORDER BY user_id DESC')
        user_data = query_results.fetchall()
        user_array = []
        for user in user_data:
            user_array.append(user[0])

        return json.dumps(user_array)

    def post(self):
        userOptions = self.get_argument('userOptions')
        print 'selected user id', userOptions
        self.application.cur_user = int(userOptions)
        query_results = self.application.conn.execute('select * from study_progress where user_id=' + str(userOptions))
        user_data = query_results.fetchall()

        last_page = []
        if len(user_data) > 0:
            last_page = user_data[len(user_data) - 1]

        if last_page[1] == 'prestudy':
            self.redirect('/prestudy')

        if last_page[1] == 'mmd':
            self.application.cur_mmd = int(last_page[2])
            print 'last mmd', self.application.cur_mmd

            # find the mmd order for this user
            query_results = self.application.conn.execute('select * from user_data where user_id=' + str(userOptions))
            user_data = query_results.fetchall()

            if len(user_data) > 0:
                self.application.mmd_order = eval(user_data[0][2])
                print self.application.mmd_order
                counter = 0
                for mmd in self.application.mmd_order:
                    print mmd
                    if int(mmd) == self.application.cur_mmd:
                        self.application.mmd_index = counter + 1
                        print 'mmd_index', self.application.mmd_index
                        self.redirect('/mmd')
                    counter += 1
            else:
                print 'ERROR! Cannot resule this user'


class QuestionnaireHandler(tornado.web.RequestHandler):
    def get(self):
        # displays contents of index.html
        print 'questionnaire handler'
        self.application.start_time = str(datetime.datetime.now().time())
        mmdQuestions = self.loadMMDQuestions()
        noofMMD = len(self.application.mmd_order)
        progress = str(self.application.mmd_index) + ' of ' + str(noofMMD)
        self.render('questionnaire.html', mmd=self.application.cur_mmd, progress=progress, questions=mmdQuestions)

    def post(self):
        print 'post'
        answers = self.get_argument('answers')
        print answers

        answers = json.loads(answers)

        print answers

        self.application.end_time = str(datetime.datetime.now().time())
        questionnaire_data = [
            self.application.cur_user, self.application.cur_mmd, self.application.start_time, self.application.end_time]

        task_data = (self.application.cur_user, self.application.cur_mmd, 'questions', self.application.start_time,
                     self.application.end_time)
        self.application.conn.execute('INSERT INTO MMD_performance VALUES (?,?,?,?,?)', task_data)
        self.application.conn.commit()

        i = 1
        for a in answers:
            # questionnaire_data.append(a)
            answer_data = (self.application.cur_user, self.application.cur_mmd, i, a[0], a[1])
            print 'question results:'
            print answer_data
            self.application.conn.execute('INSERT INTO Questions_results VALUES (?,?,?,?,?)', answer_data)
            i = i + 1

        # print tuple(questionnaire_data)

        self.application.conn.commit()

        self.application.conn.execute('INSERT INTO Study_progress VALUES (?,?,?,?)',
                                      [self.application.cur_user, 'mmd', self.application.cur_mmd,
                                       str(datetime.datetime.now().time())])
        self.application.conn.commit()
        # refers to database connected to in 'class Application'
        # database = self.application.db.database
        # empty entry to insert into database in order to generate a user id
        # entry = {}
        # inserts empty entry and saves it to UserID variable in 'class Application'
        # self.application.UserID = database.insert_one(entry).inserted_id
        # print self.application.UserID

        self.redirect('/mmd')
        # self.redirect('/prestudy')

    def loadMMDQuestions(self):
        conn = sqlite3.connect('database_questions.db')
        query_results = conn.execute('select * from MMD_questions where mmd_id=' + str(self.application.cur_mmd))

        # hard-coded two questions as they appear in all mmds
        questions = []
        questions.append(
            [self.application.cur_mmd, "1", "I am interested in reading the full article.", "Likert", "Subjective"])

        questions.append(
            [self.application.cur_mmd, "2", "The article/snippet was easy to understand.", "Likert", "Subjective"])

        questions.extend(query_results.fetchall())

        return json.dumps(questions)

    #
    # def saveMMDQuestions(self):
    #     self.application.end_time = str(datetime.datetime.now().time())
    #     task_data = (
    #     self.application.cur_user, self.application.cur_mmd, self.application.start_time, self.application.end_time, "")
    #     self.application.conn.execute('INSERT INTO MMD_tasks VALUES (?,?,?,?,?)', task_data)
    #     self.application.conn.commit()


class MMDInterventionHandler(tornado.web.RequestHandler):
    def get(self):
        # displays contents of index.html
        self.application.start_time = str(datetime.datetime.now().time())
        self.render('MMDIntervention.html', mmd="30")

    def post(self):
        # refers to database connected to in 'class Application'
        # database = self.application.db.database
        # empty entry to insert into database in order to generate a user id
        # entry = {}
        # inserts empty entry and saves it to UserID variable in 'class Application'
        # self.application.UserID = database.insert_one(entry).inserted_id
        # print self.application.UserID
        self.redirect('/prestudy')


class MMDHandler(tornado.web.RequestHandler):
    def get(self):
        # displays contents of index.html
        self.application.start_time = str(datetime.datetime.now().time())
        print 'mmd order', self.application.mmd_order, self.application.mmd_index
        if self.application.mmd_index < len(self.application.mmd_order):
            self.application.cur_mmd = self.application.mmd_order[self.application.mmd_index]

            if (self.application.show_question_only):
                self.redirect('/questionnaire')
            else:
                self.render('mmd.html', mmd=str(self.application.cur_mmd))
            self.application.mmd_index += 1
        else:
            self.redirect('/')

    def post(self):
        # refers to database connected to in 'class Application'
        # database = self.application.db.database
        # empty entry to insert into database in order to generate a user id
        # entry = {}
        # inserts empty entry and saves it to UserID variable in 'class Application'
        # self.application.UserID = database.insert_one(entry).inserted_id
        # print self.application.UserID

        # self.application.cur_user = random.randint(0, 1000)  #random number for now
        self.application.end_time = str(datetime.datetime.now().time())
        task_data = (self.application.cur_user, self.application.cur_mmd, 'mmd', self.application.start_time,
                     self.application.end_time)
        self.application.conn.execute('INSERT INTO MMD_performance VALUES (?,?,?,?,?)', task_data)
        self.application.conn.commit()
        self.redirect('/questionnaire')


class AjaxHandler(tornado.web.RequestHandler):
    def post(self):
        jsonobj = json.loads(self.request.body)
        print jsonobj

        print 'Post data received'

        file = open('application/frontend/static/AOICoordinates/' + jsonobj['filename'], 'w')
        file.write(self.request.body)
        file.close()


class PreStudyHandler(tornado.web.RequestHandler):
    def get(self):
        # gets time upon entering form
        self.application.start_time = str(datetime.datetime.now().time())
        # display contents of prestudy.html
        self.application.show_question_only = 0
        self.render("userid.html")

    def post(self):
        # gets time upon completing form
        self.application.end_time = str(datetime.datetime.now().time())
        # get contents submitted in the form for prestudy
        self.application.cur_user = self.get_argument('userID')

        # store the new userID
        user_data = [self.application.cur_user, str(self.application.start_time), str(self.application.mmd_order)]
        self.application.conn.execute('INSERT INTO User_data VALUES (?,?,?)', user_data)

        # age = self.get_argument('age')
        # gender = self.get_argument('gender')
        # occupation = self.get_argument('occupation')
        # field = self.get_argument('field')
        # simple_bar = self.get_argument('simple_bar')
        # complex_bar = self.get_argument('complex_bar')
        #
        # #currently that number value is just a dummy user id
        # #organizes data to insert into table into a tuple
        # prestudy = (self.application.cur_user, age, gender, occupation, field, simple_bar, complex_bar, self.application.start_time, self.application.end_time)
        # self.application.conn.execute('INSERT INTO prestudy VALUES (?,?,?,?,?,?,?,?,?)', prestudy)
        # self.application.conn.commit()

        #####TODO######

        # get database entry with current sessions user id and saves prestudy content
        # database.update({"_id": self.application.UserID}, {'$set': prestudy})
        # self.redirect('/locus')
        self.redirect('/mmd')


class LocusHandler(tornado.web.RequestHandler):
    def get(self):
        # get time upon entering form
        self.application.start_time = str(datetime.datetime.now().time())
        # displays contents of locus.html
        self.render("locus.html", userid=self.application.UserID)

    def post(self):
        # get time upon leaving form
        self.application.end_time = str(datetime.datetime.now().time())
        # gets content submitted in the form for locus
        q1 = self.get_argument('question1')
        q2 = self.get_argument('question2')
        q3 = self.get_argument('question3')
        q4 = self.get_argument('question4')
        q5 = self.get_argument('question5')
        q6 = self.get_argument('question6')
        q7 = self.get_argument('question7')
        q8 = self.get_argument('question8')
        q9 = self.get_argument('question9')
        q10 = self.get_argument('question10')
        q11 = self.get_argument('question11')
        q12 = self.get_argument('question12')
        q13 = self.get_argument('question13')
        q14 = self.get_argument('question14')
        q15 = self.get_argument('question15')
        q16 = self.get_argument('question16')
        q17 = self.get_argument('question17')
        q18 = self.get_argument('question18')
        q19 = self.get_argument('question19')
        q20 = self.get_argument('question20')
        q21 = self.get_argument('question21')
        q22 = self.get_argument('question22')
        q23 = self.get_argument('question23')
        q24 = self.get_argument('question24')
        q25 = self.get_argument('question25')
        q26 = self.get_argument('question26')
        q27 = self.get_argument('question27')
        q28 = self.get_argument('question28')
        q29 = self.get_argument('question29')
        # time = self.get_argument('elapsed_time')

        #####TODO#####

        # gets database entry with current sessions user id and saves locus content
        # database.update({"_id": self.application.UserID}, {'$set': locus})

        # organizes data to be inserted into table as a tuple
        locus = (2, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
                 q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
                 q21, q22, q23, q24, q25, q26, q27, q28, q29,
                 self.application.start_time, self.application.end_time)
        self.application.conn.execute('INSERT INTO locus VALUES (?,?,?,?,?,?,?,?,?,?,' +
                                      '?,?,?,?,?,?,?,?,?,?,' +
                                      '?,?,?,?,?,?,?,?,?,?,?)', locus)
        self.application.conn.commit()

        self.redirect('/mmd')


class FixationHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


# main function is first thing to run when application starts
def main():
    tornado.options.parse_command_line()
    # Application() refers to 'class Application'
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
