import pymel.core as pm
     
# Description: Sets visibility keyframes on the selected object such that it turns on or off at the specified frame.
# Inputs: A frame number and a selection
# Returns: Function object
def key_on( frame, sel ):
    off_frame = frame - 1
    pm.setKeyframe( sel, at='v', t=off_frame, v=0, s=False )
    pm.setKeyframe( sel, at='v', t=frame, v=1, s=False )

def key_off( frame, sel ):
    on_frame = frame - 1
    pm.setKeyframe( sel, at='v', t=on_frame, v=1, s=False )
    pm.setKeyframe( sel, at='v', t=frame, v=0, s=False )

# Description:  Clears all visibility keyframes from the selected object & sets the object to be (in)visible
# Inputs: A selected object, and a resulting visibility option (0 or 1)
# Outputs: Function object    
def clear_vis( sel, vis ):
    if pm.keyframe( sel, at='v', q=True ):
        pm.cutKey( sel, at='v' )
    else:
        pm.warning("No visibility keys to delete!")
    if vis == 0:
        sel.visibility.set(0)
    elif vis == 1:
        sel.visibility.set(1)
    else:
        pass

# Description: Updates a specified intField with the current frame
# Inputs: An intField object
# Outputs: scriptJob ID
def update_frame_job( int_field ):
    job = pm.scriptJob( e=( 'timeChanged', lambda *args: int_field.setValue( pm.currentTime() ) ) )
    return job
    
# Description: Returns the value of the specified intField.
# Inputs: An intField object of a window layout.
# Returns: int (specified frame)
def get_int( int_field ):
    user_input = int_field.getValue()
    return user_input

# Description: Returns the current selection as a single maya object (as opposed to a list object.)
# Inputs: None
# Returns: A SINGLE valid object
def get_sel( *args ):
    sel = pm.ls( selection=True )[0]
    return sel

    ## EXECUTE THIS FUNCTION TO RUN THE SCRIPT (((((    vis.go()   )))))
       
if 'visKeyWin' in locals():
    pm.deleteUI( visKeyWin )
    
visKeyWin = pm.window( title="VIZ WIZ", iconName='VIZ', widthHeight=(100, 68), s=False, tlb=True )

pm.columnLayout( adjustableColumn=True )
int_field = pm.intField( v=pm.currentTime() )

pm.separator( st="in", h=5 )

pm.rowLayout( nc=4 )
clear_off_btn = pm.button( l="|", c = lambda *args: clear_vis( get_sel(), 0 ), w=20, h=55, bgc=[0.1, 0.1, 0.1] )
key_off_btn = pm.button( l="", c = lambda *args: key_off( get_int(int_field), get_sel() ), w=55, h=55, bgc=[0.18, 0.18, 0.18] ) # Clarified lambda: vis_go( intField value, selection )
key_on_btn = pm.button( l="", c = lambda *args: key_on( get_int(int_field), get_sel() ), w=55, h=55, bgc=[0.8, 0.8, 0.8] ) # Clarified lambda: vis_go( intField value, selection )
clear_on_btn = pm.button( l="O", c = lambda *args: clear_vis( get_sel(), 1 ), w=20, h=55, bgc=[0.9, 0.9, 0.9] )
pm.setParent( '..' )

#pm.rowLayout( nc=2 )
#scrubby_btn = pm.button( l="update frame", c = lambda *args: self.scrub_btn( int_field ), w=158, h=15, bgc=[0.25, 0.25, 0.25] )
#typey_btn = pm.button( l="input mode", w=78, h=15 )
#pm.setParent( '..' )

#pm.setParent( '..' )
pm.showWindow( visKeyWin )
update_frame_job( int_field )
