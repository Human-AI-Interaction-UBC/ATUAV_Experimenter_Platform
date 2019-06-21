import math
import geometry
import ast

def merge_fixation_features(part_features, accumulator_features):
    """
		Merges fixation features (for whole screen) from part_features into accumulator_features
    """
    numfixations = sumfeat(part_features, accumulator_features, "['numfixations']")

    accumulator_features['fixationrate']                = float(numfixations) / (accumulator_features['length'] - accumulator_features['length_invalid'])
    if numfixations > 0:
        meanfixationduration                            = weightedmeanfeat(part_features, accumulator_features, "['numfixations']","['meanfixationduration']")
        accumulator_features['stddevfixationduration']  = aggregatestddevfeat(part_features, accumulator_features,
                      "['numfixations']", "['stddevfixationduration']", "['meanfixationduration']", meanfixationduration)
        accumulator_features['sumfixationduration']     = sumfeat(part_features, accumulator_features, "['sumfixationduration']")
        accumulator_features['meanfixationduration']    = meanfixationduration
        accumulator_features['numfixations']            = numfixations

def merge_path_angle_features(part_features, accumulator_features):
    """
        Merges path and angle features (for whole screen) from part_features into accumulator_features
    """
    numfixdistances            = sumfeat(part_features, accumulator_features, "['numfixdistances']")
    numabsangles               = sumfeat(part_features, accumulator_features, "['numabsangles']")
    numrelangles               = sumfeat(part_features, accumulator_features, "['numrelangles']")

    if numfixdistances > 1:
        meanpathdistance                                = weightedmeanfeat(part_features, accumulator_features,"['numfixdistances']","['meanpathdistance']")
        accumulator_features['sumpathdistance']         = sumfeat(part_features, accumulator_features, "['sumpathdistance']")
        accumulator_features['stddevpathdistance']      = aggregatestddevfeat(part_features, accumulator_features, "['numfixdistances']",
                                        "['stddevpathdistance']", "['meanpathdistance']", meanpathdistance)
        accumulator_features['eyemovementvelocity']     = accumulator_features['sumpathdistance']/(accumulator_features['length'] - accumulator_features['length_invalid'])
        accumulator_features['sumabspathangles']        = sumfeat(part_features, accumulator_features, "['sumabspathangles']")
        meanabspathangles                               = weightedmeanfeat(part_features, accumulator_features,"['numabsangles']","['meanabspathangles']")
        accumulator_features['abspathanglesrate']       = accumulator_features['sumabspathangles']/(accumulator_features['length'] - accumulator_features['length_invalid'])
        accumulator_features['stddevabspathangles']     = aggregatestddevfeat(part_features, accumulator_features, "['numabsangles']",
                                "['stddevabspathangles']", "['meanabspathangles']", meanabspathangles)
        accumulator_features['sumrelpathangles']        = sumfeat(part_features, accumulator_features, "['sumrelpathangles']")
        meanrelpathangles                               = weightedmeanfeat(part_features, accumulator_features,"['numrelangles']","['meanrelpathangles']")
        accumulator_features['relpathanglesrate']       = accumulator_features['sumrelpathangles']/(accumulator_features['length'] - accumulator_features['length_invalid'])
        accumulator_features['stddevrelpathangles']     = aggregatestddevfeat(part_features, accumulator_features, "['numrelangles']", "['stddevrelpathangles']",
                                "['meanrelpathangles']", meanrelpathangles)
        accumulator_features['meanpathdistance']        = meanpathdistance
        accumulator_features['meanabspathangles']       = meanabspathangles
        accumulator_features['meanrelpathangles']       = meanrelpathangles
        accumulator_features['numfixdistances']         = numfixdistances
        accumulator_features['numabsangles']            = numabsangles
        accumulator_features['numrelangles']            = numrelangles

def merge_pupil_features(part_features, accumulator_features):
    """
	    Merges pupil features (for whole screen and AOIs) from part_features into accumulator_features
    """
    numpupilsizes    = sumfeat(part_features, accumulator_features, "['numpupilsizes']")
    numpupilvelocity = sumfeat(part_features, accumulator_features, "['numpupilvelocity']")

    if numpupilsizes > 0: # check if scene has any pupil data
        mean_pupilsize = weightedmeanfeat(part_features, accumulator_features, "['numpupilsizes']", "['meanpupilsize']")
        accumulator_features['stddevpupilsize']    = aggregatestddevfeat(part_features, accumulator_features,
                                                                            "['numpupilsizes']", "['stddevpupilsize']",
                                                                            "['meanpupilsize']", mean_pupilsize)
        accumulator_features['maxpupilsize']       = maxfeat(part_features, accumulator_features, "['maxpupilsize']")
        accumulator_features['minpupilsize']       = minfeat(part_features, accumulator_features, "['minpupilsize']", -1)
        accumulator_features['meanpupilsize']      = mean_pupilsize
        accumulator_features['numpupilsizes']      = numpupilsizes
        if (accumulator_features['startpupilsize'] == -1):
            accumulator_features['startpupilsize'] = part_features['startpupilsize']
        if (part_features['endpupilsize'] != -1):
            accumulator_features['endpupilsize'] = part_features['endpupilsize']

    if numpupilvelocity > 0: # check if scene has any pupil velocity data
        mean_velocity                                           = weightedmeanfeat(part_features, accumulator_features, "['numpupilvelocity']", "['meanpupilvelocity']")
        accumulator_features['stddevpupilvelocity']             = aggregatestddevfeat(part_features, accumulator_features, "['numpupilvelocity']", "['stddevpupilvelocity']", "['meanpupilvelocity']", mean_velocity)
        accumulator_features['maxpupilvelocity']                = maxfeat(part_features, accumulator_features, "['maxpupilvelocity']")

        accumulator_features['minpupilvelocity']                = minfeat(part_features, accumulator_features, "['minpupilvelocity']", -1)
        accumulator_features['meanpupilvelocity']               = mean_velocity
        accumulator_features['numpupilvelocity']                = numpupilvelocity
        if (accumulator_features['startpupilvelocity'] == -1):
            accumulator_features['startpupilvelocity'] = part_features['startpupilvelocity']
        if (part_features['endpupilvelocity'] != -1):
            accumulator_features['endpupilvelocity'] = part_features['endpupilvelocity']

def merge_distance_features(part_features, accumulator_features):
    """
        Merges distance features (for whole screen and AOIs) from part_features into accumulator_features
    """
    numdistancedata = sumfeat(part_features, accumulator_features,"['numdistancedata']")
    if numdistancedata > 0:
        mean_distance                                           = weightedmeanfeat(part_features, accumulator_features, "['numdistancedata']", "['meandistance']")
        accumulator_features['stddevdistance']                  = aggregatestddevfeat(part_features, accumulator_features, "['numdistancedata']", "['stddevdistance']", "['meandistance']", mean_distance)
        accumulator_features['maxdistance']                     = maxfeat(part_features, accumulator_features, "['maxdistance']")

        accumulator_features['mindistance']                     = minfeat(part_features, accumulator_features, "['mindistance']", -1)
        accumulator_features['meandistance']                    = mean_distance
        accumulator_features['numdistancedata']                 = numdistancedata
        if (accumulator_features['startdistance'] == -1):
            accumulator_features['startdistance'] = part_features['startdistance']
        if (part_features['enddistance'] != -1):
            accumulator_features['enddistance'] = part_features['enddistance']

def merge_event_data(part_features, accumulator_features):
    """
        Merges event features (for whole screen and AOIs) from part_features into accumulator_features
    """
    numevents = sumfeat(part_features, accumulator_features,"['numevents']")

    if numevents > 0:
        accumulator_features['numevents'] = numevents
        accumulator_features['numleftclic'] = sumfeat(part_features, accumulator_features, "['numleftclic']")
        accumulator_features['numrightclic'] = sumfeat(part_features, accumulator_features,  "['numrightclic']")
#        accumulator_features['numdoubleclic'] = sumfeat(part_features, accumulator_features,  "['numdoubleclic']")
#        accumulator_features['numdragdrop'] = sumfeat(part_features, accumulator_features,  "['numdragdrop']")
        accumulator_features['numkeypressed'] = sumfeat(part_features, accumulator_features,  "['numkeypressed']")
        accumulator_features['leftclicrate'] = float(accumulator_features['numleftclic'])/(accumulator_features['length'] - accumulator_features['length_invalid'])
        accumulator_features['rightclicrate'] = float(accumulator_features['numrightclic'])/(accumulator_features['length'] - accumulator_features['length_invalid'])
#        accumulator_features['doubleclicrate'] = float(accumulator_features['numdoubleclic'])/(self.accumulator_features['length'] - accumulator_features['length_invalid'])
#        accumulator_features['dragdroprate'] = float(accumulator_features['numdragdrop'])/(accumulator_features['length'] - accumulator_features['length_invalid'])
        accumulator_features['keypressedrate'] = float(accumulator_features['numkeypressed'])/(accumulator_features['length'] - accumulator_features['length_invalid'])
#        accumulator_features['timetofirstleftclic'] = self.firstseg.features['timetofirstleftclic']
#        accumulator_features['timetofirstrightclic'] = self.firstseg.features['timetofirstrightclic']
#        accumulator_features['timetofirstdoubleclic'] = self.firstseg.features['timetofirstdoubleclic']
#        accumulator_features['timetofirstkeypressed'] = self.firstseg.features['timetofirstkeypressed']

def merge_aoi_fixations(part_features, accumulator_features, length, total_numfixations_accumulator):
    """
	   Merges fixation AOI features from part_features into accumulator_features
    """
    if accumulator_features['numfixations'] == 0:
        accumulator_features['numfixations']            = part_features['numfixations']
        accumulator_features['meanfixationduration']    = part_features['meanfixationduration']
        accumulator_features['stddevfixationduration']  = part_features['stddevfixationduration']
        accumulator_features['longestfixation']         = part_features['longestfixation']
        accumulator_features['fixationrate']            = part_features['fixationrate']
        accumulator_features['totaltimespent']          = part_features['totaltimespent']
        accumulator_features['proportiontime']          = part_features['proportiontime']
        accumulator_features['proportionnum']           = part_features['proportionnum']
    else:
        if part_features['numfixations'] > 1:
            total_numfixations = accumulator_features['numfixations'] + part_features['numfixations']
            accumulator_features['longestfixation']       = max(accumulator_features['longestfixation'], part_features['longestfixation'])
            accumulator_features['totaltimespent']        += part_features['totaltimespent']
            aggregate_meanfixationduration = accumulator_features['totaltimespent'] / total_numfixations
            accumulator_features['stddevfixationduration']      = pow(((accumulator_features['numfixations'] - 1) * pow(accumulator_features['stddevfixationduration'], 2) + \
                                                                 (part_features['numfixations'] - 1) * pow(part_features['stddevfixationduration'], 2) + \
                                                                 accumulator_features['numfixations'] * pow(accumulator_features['meanfixationduration'] - aggregate_meanfixationduration , 2) + \
                                                                 part_features['numfixations'] * pow(part_features['meanfixationduration'] - aggregate_meanfixationduration, 2)) / (total_numfixations - 1), 0.5)
            accumulator_features['numfixations']          = total_numfixations
            accumulator_features['meanfixationduration']  = aggregate_meanfixationduration
            accumulator_features['proportiontime']        = float(accumulator_features['totaltimespent']) / length
            accumulator_features['proportionnum']         = float(accumulator_features['numfixations']) / total_numfixations_accumulator

            if accumulator_features['totaltimespent'] > 0:
                accumulator_features['fixationrate']      = float(accumulator_features['numfixations']) / accumulator_features['totaltimespent']
    #if part_features['timetofirstfixation'] != -1:
    #    accumulator_features['timetofirstfixation']       = min(accumulator_features['timetofirstfixation'], deepcopy(part_features['timetofirstfixation']) + part_features['starttime'] - sc_start)
    #if part_features['timetolastfixation']  != -1:
    #    accumulator_features['timetolastfixation']        = max(accumulator_features['timetolastfixation'], deepcopy(part_features['timetolastfixation']) + part_features['starttime'] - sc_start)


def merge_aoi_transitions(part_features, accumulator_features):
    """
        Merges transition AOI features from part_features into accumulator_features
    """
    part_features_transition_aois = filter(lambda x: x.startswith('numtransfrom_'), part_features.keys())
    accumulator_features['total_trans_from'] += part_features['total_trans_from']   #updating the total number of transition from this AOI
    for feat in part_features_transition_aois:
        if feat in accumulator_features:
            accumulator_features[feat] += part_features[feat]
        else:
            accumulator_features[feat] = part_features[feat]
    # updating the proportion tansition features based on new transitions to and from this AOI
    accumulator_features_transition_aois = filter(lambda x: x.startswith('numtransfrom_'), accumulator_features.keys()) #all the transition features for this AOI should be updated even if they are not active for this segment
    for feat in accumulator_features_transition_aois:
        aid = feat[len('numtransfrom_'):]
        if accumulator_features['total_trans_from'] > 0:
            accumulator_features['proptransfrom_%s'%(aid)] = float(accumulator_features[feat]) / accumulator_features['total_trans_from']
        else:
            accumulator_features['proptransfrom_%s'%(aid)] = 0

def calc_distances(fixdata):
    """returns the Euclidean distances between a sequence of "Fixation"s

    Args:
        fixdata: a list of fixation datapoints
    """
    distances = []
    lastx = fixdata[0][0]
    lasty = fixdata[0][1]

    for i in xrange(1, len(fixdata)):
        x = fixdata[i][0]
        y = fixdata[i][1]
        dist = math.sqrt((x - lastx)**2 + (y - lasty)**2)
        distances.append(dist)
        lastx = x
        lasty = y

    return distances

def calc_abs_angles(fixdata):
    """returns the absolute angles between a sequence of "Fixation"s that build a scan path.

    Abosolute angle for each saccade is the angle between that saccade and the horizental axis

    Args:
        fixdata: a list of fixation datapoints

    Returns:
        a list of absolute angles for the saccades formed by the given sequence of "Fixation"s in Radiant
    """
    abs_angles = []
    lastx = fixdata[0][0]
    lasty = fixdata[0][1]

    for i in xrange(1,len(fixdata)):
        x = fixdata[i][0]
        y = fixdata[i][1]
        (dist, theta) = geometry.vector_difference((lastx,lasty), (x, y))
        abs_angles.append(abs(theta))
        lastx = x
        lasty = y

    return abs_angles

def calc_rel_angles(fixdata):
    """returns the relative angles between a sequence of "Fixation"s that build a scan path in Radiant

    Relative angle for each saccade is the angle between that saccade and the previous saccade.

    Defined as: angle = acos(v1 dot v2)  such that v1 and v2 are normalized vector2coord

    Args:
        fixdata: a list of fixation datapoints

    Returns:
        a list of relative angles for the saccades formed by the given sequence of "Fixation"s in Radiant
    """
    rel_angles = []
    lastx = fixdata[0][0]
    lasty = fixdata[0][1]

    for i in xrange(1, len(fixdata) - 1):
        x = fixdata[i][0]
        y = fixdata[i][1]
        nextx = fixdata[i + 1][0]
        nexty = fixdata[i + 1][1]
        v1 = (lastx - x, lasty - y)
        v2 = (nextx - x, nexty - y)

        if v1 != (0.0, 0.0) and v2 != (0.0, 0.0):
            v1_dot = math.sqrt(geometry.simpledotproduct(v1, v1))
            v2_dot = math.sqrt(geometry.simpledotproduct(v2, v2))
            normv1 = ((lastx - x) / v1_dot, (lasty - y) / v1_dot)
            normv2 = ((nextx - x) / v2_dot, (nexty - y) / v2_dot)
            dotproduct = geometry.simpledotproduct(normv1, normv2)
            if dotproduct < -1:
                dotproduct = -1.0
            if dotproduct > 1:
                dotproduct = 1.0
            theta = math.acos(dotproduct)
            rel_angles.append(theta)
        else:
            rel_angles.append(0.0)
        lastx = x
        lasty = y

    return rel_angles

def minfeat(part_features, accumulator_features, feat, nonevalue = None):
    """a helper method that calculates the min of a target feature over two feature dictionaries

    Returns:
        the min of the target feature over the given list of objects
    """
    part_feat = eval('part_features' + feat)
    acc_feat =  eval('accumulator_features' + feat)
    if (part_feat != nonevalue and acc_feat != nonevalue):
        return min(eval('part_features'+feat), eval('accumulator_features'+feat))
    elif (part_feat != nonevalue):
        return part_feat
    else:
        return nonevalue

def maxfeat(part_features, accumulator_features, feat):
    """a helper method that calculates the max of a target feature over a list of objects

    Returns:
        the max of the target feature over the given list of objects
    """
    return max(eval('part_features'+feat), eval('accumulator_features'+feat))

def weightedmeanfeat(part_features, accumulator_features, totalfeat, ratefeat):
    """a helper method that calculates the weighted average of a target feature over a list of Segments

    Returns:
        the weighted average of the ratefeat over the Segments
    """

    num_valid = float(0)
    num = 0

    t = eval('part_features' + totalfeat)
    num_valid += t * eval('part_features' + ratefeat)
    num += t
    t = eval('accumulator_features'+totalfeat)
    num_valid += t * eval('accumulator_features' + ratefeat)
    num += t
    if num != 0:
        return num_valid / num
    return 0

def aggregatestddevfeat(part_features, accumulator_features, totalfeat, sdfeat, meanfeat, meanscene):
    """a helper method that calculates the aggregated standard deviation of a target feature over a list of Segments

    Returns:
        the weighted average of the ratefeat over the Segments
    """
    num = float(0)
    den = float(0)


    t = eval('part_features' + totalfeat)
    if t > 0:
        sd = eval('part_features' + sdfeat)
        if math.isnan(sd): sd = 0
        meanobj = eval('part_features' + meanfeat)

        num += (t-1) * sd ** 2 + t * (meanobj - meanscene) ** 2
        den += t

    t = eval('accumulator_features'+totalfeat)
    if t > 0:
        sd = eval('accumulator_features'+sdfeat)
        if math.isnan(sd): sd = 0
        meanobj = eval('accumulator_features'+meanfeat)

        num += (t - 1) * sd ** 2 + t * (meanobj-meanscene) ** 2
        den += t
    if den > 1:
        return math.sqrt(float(num)/(den-1))
    return 0

def sumfeat(part_features, accumulator_features, feat):
    """a helper method that calculates the sum of a target feature over a list of objects

    Returns:
        the sum of the target feature over the given list of objects
    """
    sum = 0
    sum += eval('part_features'+feat)
    if (eval('accumulator_features'+feat) != -1):
        sum += eval('accumulator_features'+feat)
    return sum

def generate_event_lists(event_data):
    """Returns separate list per type of events. Format:
    Args:
        event_data: a list of events
    Returns:
        lists of left clics, right clics, double clics and keys pressed
    """
    leftc = []
    rightc = []
    doublec = []
    drag_drop = []
    keyp = []
    for e in event_data:
        if instanceof(e, KeyboardEvent):
            keyp.append(e)
#        elif instanceof(e, DragDropMouseEvent):
#            drag_drop.append(e)
#        elif instanceof(e, DoubleClickMouseEvent):
#            double_click.append(e)
        elif instanceof(e, BasicMouseEvent) and e.left_click:
            leftc.append(e)
        else:
            rightc.append(e)

    return (leftc, rightc, keyp)# doublec, drag_drop, keyp)
