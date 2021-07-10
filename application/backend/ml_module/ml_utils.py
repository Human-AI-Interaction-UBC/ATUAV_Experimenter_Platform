import pandas as pd
import numpy as np
import os


# ----------------------------------------------------------------------------------------------------

def filter_features(df, prediction_type, slice, window_size=1000):

    """
    prediction_type: ['within', 'across]
    window_size: used for within-task predictions (default = 1000 ms)
    slice: current within-task window (number of windows accumulated so far)

    Returns:
        pandas.DataFrame: filtered EMDAT features
    """
    
    aoinames = ['Relevant bars', 'Non-relevant bars', 'Text', 'Refs', 'labels', 'Viz', 'legend']
    
    toremove = [
        'blinknum', 'blinkdurationmax', 'blinktimedistancestd', 'blinktimedistancemin', 
        'blinktimedistancemean', 'blinkdurationmean', 'blinktimedistancemax', 'blinkrate','blinkdurationmin', 
        'blinkdurationtotal', 'blinkdurationstd', 'length', 'numfixations', 'numsegments', 'doubleclicrate', 
        'sumabspathangles', 'sumfixationduration' ,'sumpathdistance' ,'sumrelpathangles', 'sumsaccadedistance', 
        'sumsaccadeduration','numevents', 'numleftclic', 'leftclicrate', 'numrightclic', 'numdoubleclic',
        'numsaccades', 'numsamples', 'numkeypressed', 'rightclicrate', 'keypressedrate','timetofirstdoubleclic',
        'timetofirstkeypressed', 'timetofirstleftclic',
        'timetofirstrightclic', 'timetolastfixation']
    
    aoi_features_toremove = [
        'blinknum', 'doubleclicrate', 'numevents', 'numfixations', 'numleftclic', 'numrightclic',
        'numdoubleclic', 'rightclicrate', 'timetofirstdoubleclic', 'timetofirstrightclic', 'timetofirstleftclic',
        'timetolastdoubleclic', 'timetolastfixation', 'timetolastleftclic', 'timetolastrightclic', 'totaltimespent',
        'enddistance', 'endpupilsize', 'startdistance', 'startpupilsize']

    for aoi in aoinames:
        for aoi_feature in aoi_features_toremove:
            toremove.append('{aoi}_{aoi_feature}'.format(aoi=aoi, aoi_feature=aoi_feature))

    # removing the columns
    df = df[[feature for feature in df.columns if feature not in toremove]]

    # some value modifications
    
    distance_features = ['enddistance', 'maxdistance', 'meandistance', 'mindistance', 'startdistance']

    for distance_feature in distance_features:
        df.loc[(df[df[distance_feature] == -1].index), distance_feature] = 600
        for aoi in aoinames:
            aoi_distance_feature = '{aoi}_{distance_feature}'.format(aoi=aoi, distance_feature=distance_feature)
            if aoi_distance_feature in df.columns:
                df.loc[(df[df[aoi_distance_feature] == -1].index), aoi_distance_feature] = 600

    stddev_other_mean_features = [
        'stddevabspathangles', 'stddevdistance', 'stddevfixationduration', 'stddevpathdistance', 'stddevpupilsize',
        'stddevrelpathangles', 'stddevsaccadedistance', 'stddevsaccadeduration', 'stddevsaccadespeed', 
        'meanabspathangles', 'meanfixationduration', 'meanpathdistance', 'meanpupilsize', 'meanpupilvelocity',
        'meanrelpathangles', 'meansaccadedistance', 'meansaccadeduration', 'meansaccadespeed']

    for aggregate_feature in stddev_other_mean_features:
        df.loc[(df[df[aggregate_feature] == -1].index), aggregate_feature] = 0
        for aoi in aoinames:
            aoi_aggregate_feature = '{aoi}_{aggregate_feature}'.format(aoi=aoi, aggregate_feature=aggregate_feature)
            if aoi_aggregate_feature in df.columns:
                df.loc[(df[df[aoi_aggregate_feature] == -1].index), aoi_aggregate_feature] = 0

    if prediction_type == 'within':
        for feature in ['timetofirstfixation']:
            for aoi in aoinames:
                aoi_feature = '{aoi}_{feature}'.format(aoi=aoi, feature=feature)
                if aoi_feature in df.columns:
                    df.loc[(df[df[aoi_feature] == -1].index), aoi_feature] = window_size * slice
    return df


# ----------------------------------------------------------------------------------------------------

def handle_directory_existence(directory_path):
    """ 
    creates the directory if it does not already exist
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# ----------------------------------------------------------------------------------------------------
