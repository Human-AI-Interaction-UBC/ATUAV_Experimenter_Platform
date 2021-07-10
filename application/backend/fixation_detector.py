from detection_component import DetectionComponent
from tornado import gen
import time
import ast
import params
import utils

class FixationDetector(DetectionComponent):
    """
        Implementation of DetectionComponent used to detect fixations from raw gaze data
        stored in TobiiController. Once called, runs indefinitely.
    """
    def __init__(self, tobii_controller, adaptation_loop):
        """
            See __init__ in DetectionComponent
        """
        DetectionComponent.__init__(self, tobii_controller, adaptation_loop)
        self.restart_fixation_algorithm()

    def restart_fixation_algorithm(self):
        self.runOnlineFix = True
        self.cur_fix_id = 0
        self.AOIS = self.application_state_controller.getFixAoiMapping()


    def notify_app_state_controller(self, aoi, fix_start_time, fix_end_time, fix_dur):
        self.application_state_controller.updateFixTable(aoi, self.cur_fix_id, fix_start_time, fix_end_time, fix_dur)
        self.adaptation_loop.evaluateRules(aoi, fix_end_time)

    def stop(self):
        self.runOnlineFix = False
    #Preetpal's Online/Realtime fixation algorithm
    @gen.coroutine
    def run(self):
        """
            Concurrently detects fixations, defined as consecutive samples with an inter-sample
            distance of less than a set amount of pixels (disregarding missing data). Uses params.MAXDIST
            and params.MINDUR for respectively the distance and the smallest possible time length of a fixation.
            The method is a coroutine, which means that it can pause its execution and give control to other components of the platform.
        """
        print(self.AOIS, "Started fixation algorithm")

        # added
        # print('getFixAoiMapping: ', self.application_state_controller.getEmdatAoiMapping())

        #list of lists, each containing [starttime, endtime, duration, endx, endy]
        self.EndFixations = []
        #Keep track of index in x,y,time array
        array_index = 0
        #Used to get segments of size 7
        array_iterator = 7
        newX = []
        newY = []
        newTime = []
        newValid = []
        while(self.runOnlineFix):
            yield self.wait_for_new_data(array_index, array_iterator)
            if (not self.runOnlineFix):
                break
            #Get segments of size 7
            curX, curY, curTime, curValid = self.get_data_batch(array_index, array_iterator)
            newX = curX
            newY = curY
            newTime = curTime
            newValid = curValid
            Sfix, Efix = self.fixation_detection(curX, curY, curTime, curValid, params.FIX_MAXDIST, params.FIX_MINDUR)
            #When there is no end fixation detected yet
            while(1):
                #If start of fixation has not been detected yet
                if(Sfix == []):
                    array_index += array_iterator
                    #Wait till array has filled with enough data
                    yield self.wait_for_new_data(array_index, array_iterator)
                    if (not self.runOnlineFix):
                        break
                    #Get next 7 element chunk of data
                    nextX, nextY, nextTime, nextValid = self.get_data_batch(array_index, array_iterator)
                    #Append next segment with current arrays of interest
                    #If no more curX we can just newX.extend(nextX)
                    newX = curX + nextX
                    newY = curY + nextY
                    newTime = curTime + nextTime
                    newValid = curValid + nextValid
                    #Run fixation algorithm again with extended array
                    Sfix, Efix = self.fixation_detection(newX, newY, newTime, newValid, params.FIX_MAXDIST, params.FIX_MINDUR)
                    #If no start detected, then we can use this to drop the first |array_iterator| items
                    curX = nextX
                    curY = nextY
                    curTime = nextTime
                    curValid = nextValid
                else:
                    #Get that start fixation x and y values to display on front end
                    SfixTime = Sfix[0]
                    fixIndex = newTime.index(SfixTime)
                    xVal = newX[fixIndex]
                    yVal = newY[fixIndex]
                    break
            #We are here because start fixation was detected
            while(1):
                if(Efix == []):
                    array_index = array_index + array_iterator
                    #Wait till array has enough data
                    yield self.wait_for_new_data(array_index, array_iterator)
                    if (not self.runOnlineFix):
                        break
                    #Get next segment of data to append to current array of interest
                    nextX, nextY, nextTime, nextValid = self.get_data_batch(array_index, array_iterator)
                    newX.extend(nextX)
                    newY.extend(nextY)
                    newTime.extend(nextTime)
                    newValid.extend(nextValid)
                    Sfix, Efix = self.fixation_detection(newX, newY, newTime, newValid, params.FIX_MAXDIST, params.FIX_MINDUR)
                #a genuine end fixation has been found!
                else:
                    #Add the newly found end fixation to our collection of end fixations
                    #Get time stamp for newly found end fixation
                    EfixEndTime = Efix[0][1]
                    #Update index to data points after newly found end fixation
                    start_fix = self.tobii_controller.time.index(Sfix[0])
                    array_index = self.tobii_controller.time.index(EfixEndTime) + 1
                    points_in_fixation = array_index - 1 - start_fix
                    x_fixation = 0
                    y_fixation = 0
                    arr_size = points_in_fixation
                    for i in range(arr_size):
                        if (self.tobii_controller.x[start_fix + i] > 0):
                            x_fixation += self.tobii_controller.x[start_fix + i]
                            y_fixation += self.tobii_controller.y[start_fix + i]
                        else:
                            points_in_fixation -= 1
                    # If for some reason detected fixation is outside of the screen
                    if (points_in_fixation == 0):
                        Efix = []
                        Sfix = []
                        break

                    x_fixation /= points_in_fixation
                    y_fixation /= points_in_fixation
                    self.tobii_controller.add_fixation(Efix[0][3], Efix[0][4], Efix[0][2], Sfix[0])
                    #####
                    for aoi in self.AOIS:
                        if (utils.point_inside_polygon(x_fixation, y_fixation, self.AOIS[aoi])):
                            self.cur_fix_id += 1
                            self.notify_app_state_controller(aoi, int(Sfix[0]), int(EfixEndTime), int(EfixEndTime - Sfix[0]))
                    break

    @gen.coroutine
    def wait_for_new_data(self, array_index, array_iterator):
        """
    	   Coroutine which yields the control when there are no new datapoints available from Tobii. Called   from run()
           Args:
                Array_index - The position of first unused datapoint in raw data arrays so far
                Array_iterator - The number of new datapoints needed to run fixation_detection() method
        """
        while(1):
            if(len(self.tobii_controller.x) > array_index + array_iterator):
                break
            else:
                if (not self.runOnlineFix):
                    break
                yield

    def get_data_batch(self, array_index, array_iterator):
        """
            Returns array_iterator number of points from data arrays starting at the index array_index. Used by run() method.
        """
        return (self.tobii_controller.x[array_index : (array_index + array_iterator)],
                self.tobii_controller.y[array_index : (array_index + array_iterator)],
                self.tobii_controller.time[array_index : (array_index + array_iterator)],
                self.tobii_controller.validity[array_index : (array_index + array_iterator)])

    def fixation_detection(self, x, y, time, validity, maxdist=35, mindur=100000):
        """
        #Detects fixations, defined as consecutive samples with an inter-sample
        #distance of less than a set amount of pixels (disregarding missing data)

        #arguments
        #x        -	 array of x positions
        #y        -	 array of y positions
        #time        - array of timestamps

        #keyword arguments
        #maxdist	-	maximal inter sample distance in pixels (default = 25)
        #mindur	-	minimal duration of a fixation in milliseconds; detected
                    #fixation candidates will be disregarded if they are below
                    #this duration (default = 100)
        #returns
        #Sfix, Efix
                    #Sfix	-	list of lists, each containing [starttime]
                    #Efix	-	list of lists, each containing [starttime, endtime, duration, endx, endy]
        """
        # empty list to contain data
        Sfix = []
        Efix = []
        # loop through all coordinates
        si = 0
        invalid_count = 0
        last_valid = 0
        fixstart = False
        for i in range(1, len(x)):
        	# calculate Euclidean distance from the current fixation coordinate
        	# to the next coordinate
            dist = ((x[si] - x[i])**2 + (y[si] - y[i])**2)**0.5
            # check if the next coordinate is below maximal distance
            if dist <= maxdist and not fixstart:
                # if point is not valid, don't treat it as start of a fixation
                if not validity[i]:
                    si += 1
                    continue
                # start a new fixation
                fixstart = True
                Sfix.append(time[si])
                # Currently last valid point
                last_valid = i
                invalid_count = 0
            # If the fixation started before and the distance between
            # fixation start and current point is too big
            elif dist > maxdist and fixstart:
                fixstart = False
                if not validity[i]:
                    # if no more than 9 consequtive invalid points
                    if (invalid_count <= 9):
                    	invalid_count += 1
                    	fixstart = True
                    	continue
                    # if more than 9: last valid point is fixation end
                    else:
                    	duration = time[last_valid] - Sfix[-1]
                    	if duration >= mindur:
                            Efix.append((Sfix[-1], time[last_valid], time[last_valid] - Sfix[-1], x[last_valid], y[last_valid]))
                            break
                    	else:
                            Sfix.pop(-1)
                            si = i
                            invalid_count = 0
                            continue
                elif not validity[i-1]:
                    duration = time[last_valid] - Sfix[-1]
                    if duration >= mindur:
                    	Efix.append((Sfix[-1], time[last_valid], time[last_valid] - Sfix[-1], x[last_valid], y[last_valid]))
                    	break
                    else:
                    	Sfix.pop(-1)
                    	si = i
                    	invalid_count = 0
                        last_valid = i
                    	continue
                # only store the fixation if the duration is ok
                if time[i-1] - Sfix[-1] >= mindur:
                    Efix.append((Sfix[-1], time[i - 1], time[i - 1] - Sfix[-1], x[i - 1], y[i - 1]))
                    break
                # delete the last fixation start if it was too short
                Sfix.pop(-1)
                si = self.find_new_start(x, y, maxdist, i, si)
                if (si != i):
                    fixstart = True
                    Sfix.append(time[si])
                last_valid = i
                invalid_count = 0
            elif not fixstart:
                si += 1
                if validity[i]:
                    last_valid = i
        	# If within a fixation and within distance,
        	# current point should be valid.
            elif fixstart:
                last_valid = i
                invalid_count = 0
        return Sfix, Efix

    def find_new_start(self, x, y, maxdist, i, si):
        """
        Helper method for fixation_detection(): when it was detected that fixation is too short,
        it finds another starting point for the next fixation.
        """
        j = si + 1
        while(j < i):
            dist_i_j = ((x[i] - x[j])**2 + (y[i] - y[j])**2)**0.5
            if (dist_i_j <= maxdist):
                break
            j += 1
        return j
