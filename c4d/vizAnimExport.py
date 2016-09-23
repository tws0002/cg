"""
Export Anim to Viz

Copyright: 2016 ESPN Productions
Compatible with Cinema4D R14, R15, R17
Author: Mark Rohrer (mark.rohrer@espn.com)

Name-US: Export Anim to Viz
Description-US: Exports baked animation to a csv for VizRT.
"""

import c4d
from c4d import gui
from math import degrees

tracks = [
    'Position . X',
    'Position . Y',
    'Position . Z',
    'Rotation . H',
    'Rotation . P',
    'Rotation . B',
    'Scale . X',
    'Scale . Y',
    'Scale . Z',
    'Field of View (Vertical)'
    ]

def format_value_27(num, deg=False):
    if deg:
        return "{:.20f}".format(degrees(num))
    else:
        return "{:.20f}".format(num)

def format_value(num, deg=False):
    if deg:
        return '%30f' % (degrees(num))
    else:
        return '%30f' % (num)

def main():
    key_dict  = {}
    fps       = doc.GetFps()
    obj       = doc.GetActiveObject()
    if not obj:
        msg = 'Please select a baked object first.'
        dlg = gui.MessageDialog(msg)
        return

    trks      = obj.GetCTracks()
    track_len = []

    for trk in trks:
        curve = trk.GetCurve()
        name  = trk.GetName()
        if not name in tracks:
            continue
        key_dict[name] = {}
        
        keycount = curve.GetKeyCount()
        track_len.append(keycount)
        track_len = list(set(track_len))
        if len(track_len) > 1:
            msg = 'Inconsistent track length on parameter: {}. Canceling operation.'.format(name)
            dlg = gui.MessageDialog(msg)
            return
        
        for i in range(keycount):
            key_dict[name][i] = curve.GetKey(i).GetValue()
    
    try:
        with open('H:\\Desktop\\VIZ_ANIM_DATA.csv', 'w') as stream:
            for i in range(track_len[0]):
                line = [
                    format_value(key_dict['Position . X'][i]), 
                    format_value(key_dict['Position . Y'][i]), 
                    format_value(key_dict['Position . Z'][i]),
                    format_value(key_dict['Rotation . H'][i], deg=True),
                    format_value(key_dict['Rotation . P'][i], deg=True),
                    format_value(key_dict['Rotation . B'][i], deg=True),
                    format_value(key_dict['Field of View (Vertical)'][i], deg=True)
                ]
                try:
                    stream.write('%s, %s, %s, %s, %s, %s, %s\n' % (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                    #stream.write('{},{},{},{},{},{}\n'.format(*line))
                    if (fps == 30):
                        stream.write('%s, %s, %s, %s, %s, %s, %s\n' % (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                        #stream.write('{},{},{},{},{},{}\n'.format(*line))    
                except KeyError:
                    msg = 'Required track missing from baked object. Check that \'Clean Tracks\' is unchecked before baking.' 
                    dlg = gui.MessageDialog(msg)   
                    return
    except IndexError:
        msg = 'No animation tracks found on the selected object.'
        dlg = gui.MessageDialog(msg)
        return
    except IOError:
        msg = 'Could not open csv file for writing. Make sure it\'s not already open and try again.'
        dlg = gui.MessageDialog(msg)
        return
    
    msg = 'Successfully exported csv: H:\\Desktop\\VIZ_ANIM_DATA.csv'
    dlg = gui.MessageDialog(msg)

if __name__=='__main__':
    main()
