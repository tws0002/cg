# Utilities for baking and exporting cameras from Maya.  Typically used
# to get camera data to compositors, but can also be used to bake the
# camera for lighting scenes.

import pymel.core as pm
import os.path as path

####################
### CAMERA UTILS ###
####################

def bakeCamera( exp=False, *args, **kwargs ):
    """Bakes the first camera found below an arbitrary selection in Maya.
       Uses the current frame slider values as its range, and bakes on every frame.
       Optional boolean flag 'exp' will open an export window for convenience."""
    
    sel = pm.ls(sl=True)   
    # Parse the selection to find the camera
    cam = __findCamera( sel )
    # Frame range
    frange = ( pm.playbackOptions( q=True, min=True ), pm.playbackOptions( q=True, max=True ) )
    # Duplicate the camera
    dup_cam = pm.duplicate( cam, name=(cam.name() + '_Baked') )[0]
    # Parent new camera to world.
    try: pm.parent(dup_cam, w=True)
    except RuntimeError: pass
    # Constrain new camera to old
    const = pm.parentConstraint( cam, dup_cam, mo=True )
    # Bake it
    pm.bakeResults( dup_cam, t=frange )
    # Delete the constraint
    pm.delete(const)
    # Lazy export dialog
    if exp:
        pm.select(dup_cam)
        pm.mel.eval('ExportSelection;')

    return dup_cam


def bakeScene():
    
    sel=pm.ls(sl=True)
    new_nulls = pm.confirmDialog( 
        title='Rebake nulls?',
        message='Do you want to rebake your scene nulls?',
        button=['Yes','No'],
        defaultButton = 'Yes',
        cancelButton = 'No',
        dismissString = 'Cancel'
        )

    # Break operation on user cancel
    if new_nulls == 'Cancel':
        return None
    
    # Cleanup lists
    constraints = []
    exports = []

    # Generate export objects
    export_camera, src_cam = __createExportCamera()
    if new_nulls == 'Yes':
        nulls = __createNulls()
    elif new_nulls == 'No':
        nulls = __createNullList()

    # List of objects to be baked
    exports = nulls
    exports.append(export_camera)

    # Frame range
    range = ( pm.playbackOptions( q=True, min=True ), pm.playbackOptions( q=True, max=True ) )
    # Bake it
    pm.cycleCheck(e=False)
    pm.bakeResults( exports, t=range )
    
    # Clear the constraints from the exported objects
    __clearConstraints( exports )

    export_list = ""
    for obj in exports:
        export_list += ( str(obj) + "\n" )

    # Confirm the export before proceeding
    do_export = pm.confirmDialog( 
        title='Confirm Export',
        message='The following objects will be exported:\n' + str(export_list),
        button=['Looks Good','Oops'],
        defaultButton = 'Looks Good',
        cancelButton = 'Oops',
        dismissString = 'Oops'
        )

    if do_export == 'Looks Good':
        try:
            out_file = __createOutputFile( src_cam )
            pm.select(exports)
            pm.exportSelected( out_file )
            pm.warning('File exported to: ' + str(out_file))
        except: return False

    elif do_export == 'Oops':
        pm.delete(exports)
        return False

    pm.delete(exports)
    pm.select(sel)
    return True


def __getSceneUserCameras():
    default_cameras = ['topShape', 'sideShape', 'frontShape', 'perspShape']
    cams = [cam.getParent() for cam in pm.ls(typ='camera') if cam not in default_cameras]
    if len(cams) > 0:
        return cams
    else: return False


def __createExportCamera():
    """ Prepares a camera for export.  Function will attempt to find the first camera
        below the current selection.  If no selection is present, it will parse the scene
        for user cameras, and take the first it finds."""
    
    sel=pm.ls(sl=True)

    if sel is None:
        sel = __getSceneUserCameras()
    #split_path = pm.system.sceneName().splitext()[0].split('/')
       
    # Extracting shot from the file path
    #shot_str = split_path[6]
    
    # Parse the selection to find the camera
    cam = __findCamera( sel )
    # Duplicate the camera
    dup_cam = pm.duplicate( cam, name=(cam + '_BAKE_CAM') )[0]
    # Parent new camera to world.
    try: pm.parent(dup_cam, w=True)
    except RuntimeError: pass
    dup_cam.rotateOrder.set(0)
    # Constrain new camera to old
    const = pm.parentConstraint( cam, dup_cam, mo=True )
    
    return dup_cam, cam


def __findCamera( sel, *args, **kwargs ):
    """Useful for parsing an arbitrary selection to find a camera node.
       Note: This will only return the first camera found below the selection."""
       
    def getCam( obj ):
        try: 
            # Is the object a camera shape node?
            assert obj.nodeType() == 'camera'
            return obj.getParent()
        except AssertionError: 
            try: 
                # Is the object a camera transform node?
                assert obj.getShape().nodeType() == 'camera'
                return obj
            # Will throw AttributeError if the object has no shape node.    
            except AttributeError: return False
    
    if len(sel):
        sel=sel[0]

    c = getCam(sel)
    
    # Camera is already selected.  Return it.
    if c: return c
    # Check the children & grandchildren for cameras also
    elif not c:
        children = sel.listRelatives( ad=True )
        for obj in children:
            c = getCam(obj)
            if c: 
                return c
    # Cleanup handling
    elif not c:
        pm.warning('No cameras found below selection.')


def __createOutputFile( cam, *args ):
    """ Prepare an output camera file path and filename. """
    out_path = pm.system.sceneName()
    out_dir = out_path.dirname()
    out_file = out_path.basename().split('.')[0]+"_"+str(cam)+"."+out_path.basename().split('.')[1]
    out_file = out_file.replace(".mb",".ma")
    
    return out_dir + "/" + out_file


def __createNulls():
    """ Create export nulls and parent them to existing scene nulls. """
    exp_nulls = []
    constraints = []
    for null in pm.ls(typ='locator'):
        if null.nodeType() != 'locator':
            continue
        null = null.getParent()
        dup_null = pm.duplicate( null, name="Null_0" )[0]
        
        try: pm.parent(dup_null, w=True)
        except RuntimeError: pass
        
        null_const = pm.parentConstraint( null, dup_null, mo=True )
        exp_nulls.append(dup_null)
        constraints.append(null_const)
        
    return exp_nulls


def __createNullList():
    """ Create a list of already prepared locators, named 'Null_*' """
    exp_nulls = pm.ls(regex='Null.*', typ='locator')
    exp_nulls[:] = [loc.getParent() for loc in exp_nulls]

    return exp_nulls


def __clearConstraints( obj_list ):
    try: len(obj_list)
    except: obj_list = [obj_list]
    
    def __clear( obj ):
        children = obj.getChildren(typ='transform')
        for chd in children:
            if chd.nodeType() == 'parentConstraint':
                pm.delete(chd)
    
    for obj in obj_list:
        __clear( obj )
    
    return True

