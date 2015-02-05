import pymel.core as pm

### VISIBILITY KEYFRAMING UTILITIES

## sets a keyframe such that the object turns ON at the specified frame, and is keyed OFF on the previous frame
def vizKeyOn( frame, sel ):
    off_frame = frame - 1
    for obj in sel:
        pm.setKeyframe( obj, at='v', t=off_frame, v=0, s=False )
        pm.setKeyframe( obj, at='v', t=frame, v=1, s=False )
        obj.visibility.set(1)

## sets a keyframe such that the object turns OFF at the specified frame, and is keyed ON on the previous frame
def vizKeyOff(  frame, sel ):
    on_frame = frame - 1
    for obj in sel:
        pm.setKeyframe( obj, at='v', t=on_frame, v=1, s=False )
        pm.setKeyframe( obj, at='v', t=frame, v=0, s=False )
        obj.visibility.set(0)

# Description:  Clears all visibility keyframes from the selected object & sets the object to be (in)visible
# Inputs: A selected object, and a resulting visibility option (0 or 1)
def vizClear( sel, vis ):
    for obj in sel:
        if pm.keyframe( obj, at='v', q=True ):
            pm.cutKey( obj, at='v' )
        else:
            pm.warning("No visibility keys to delete!")
        if vis == 0:
            obj.visibility.set(0)
        elif vis == 1:
            obj.visibility.set(1)
        else:
            pass


def vizBlink( sel, firstFrame, duration, offset=0, inv=False ):
    for obj in sel:
        if not inv:
            pm.cutKey( obj, at='v' )
            onKey = pm.setKeyframe(obj, at='v', t=firstFrame, v=1, s=False )
            offKey = pm.setKeyframe(obj, at='v', t=(firstFrame+duration), v=0, s=False )
            holdkey = pm.setKeyframe(obj, at='v', t=(firstFrame+(2*duration)+offset), v=0, s=False)
            pm.setInfinity( obj.visibility, poi='cycle' )
        elif inv:
            pm.cutKey( obj, at='v' )
            offKey = pm.setKeyframe(obj, at='v', t=firstFrame, v=0, s=False )
            onKey = pm.setKeyframe(obj, at='v', t=(firstFrame+duration), v=1, s=False )
            holdkey = pm.setKeyframe(obj, at='v', t=(firstFrame+(duration*2)+offset), v=1, s=False)
            pm.setInfinity( obj.visibility, poi='cycle' )


def vizCascade( sel, firstFrame, on=True, spacing=0 ):
    doFrame = firstFrame
    for obj in sel:
        if on:
            vizKeyOn(doFrame, obj)
        elif not on:
            vizKeyOff(doFrame, obj)
        doFrame+=(spacing+1)

# Description: Updates a specified intField with the current frame
# Inputs: An intField object
# Outputs: scriptJob ID
def updateFrameJob( int_field ):
    job = pm.scriptJob( e=( 'timeChanged', lambda *args: int_field.setValue( pm.currentTime() ) ) )
    return job


# Description: Returns the value of the specified intField.
# Inputs: An intField object of a window layout.
# Returns: int (specified frame)
def getInt( int_field ):
    user_input = int_field.getValue()
    return user_input

# Description: Returns the current selection as a single maya object (as opposed to a list object.)
# Inputs: None
# Returns: A SINGLE valid object
def getSel( *args ):
    sel = pm.ls( selection=True )[0]
    return sel
