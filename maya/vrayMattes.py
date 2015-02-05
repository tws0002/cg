import pymel.core as pm


######################
### MATTE SELECTOR ###
######################
'''UI: MAIN WINDOW'''
def matteAssignUI( *args, **kwargs ):

    matteUI = ['A','B','C','D','E','F']
    matteUI_dict = {'A':None,'B':None,'C':None,'D':None,'E':None,'F':None}
    
    
    matAssignWin = pm.window( title="Matte Switcher", iconName='MAT', s=False )
    winBox = pm.columnLayout()

    ''' SCENE SETUP '''
    frame = pm.frameLayout(l='Scene Setup', fn='smallBoldLabelFont', cll=True, cl=False, p=winBox)
    subframe = pm.columnLayout( adjustableColumn=False, parent=frame )

    row = pm.rowLayout( parent=subframe, nc=2 )
    setup_btn = pm.button(l="1\ Make Matte REs", w=131, h=50, c=makeMatteRenderElements)
    attrs_btn = pm.button(l="2\ Add Attrs to Geo", w=131, h=50, c=lambda *args: makeUserColorAttrs( convertSel(getSel(), sh=True ) ) )
    

    ''' RGB MATTES '''
    frame = pm.frameLayout(l='Per-object Assignments', fn='smallBoldLabelFont', cll=True, cl=False, p=winBox)
    subframe = pm.columnLayout( adjustableColumn=False, parent=frame )
    
    for matte_id in matteUI:
        matteUI_dict[matte_id] = MatteSelector(matte_id).UIelement()
        

    space = pm.rowLayout(parent=subframe)
    pm.separator(style='in', h=3, p=space)


    ''' RANDOMIZER ''' 
    pm.rowLayout( parent=subframe, nc=3 )
    pm.text(l='matteX  ', align='right', w=50, h=33)
    pm.button(label='Random RGB', width=145, h=33, c=lambda *args: setRandomRGB( convertSel( getSel(), sh=True ) ) )
    pm.button(label='Force', width=63, h=33)

    pm.rowLayout(parent=subframe)
    pm.separator(style='in', h=7)

    pm.rowLayout( parent=subframe, nc=1 )
    setAllBtn = pm.button( label='>>> Assign all >>>', width=261, height=50, c=lambda *args: setAllMattes(matteUI_dict, getSel()) )
    
    pm.showWindow(matAssignWin)

class MatteSelector(object):
    def __init__( self, mat_id, *args ):
        self.matte = mat_id
        self.columnWidths = [(1,50), (2, 52), (3,20)]
        self.defaultColor = (0,0,0)
        
    def UIelement( self ):
        box = pm.rowLayout( nc=4 )
        
        # the color selection slider
        slider = pm.colorSliderGrp( label='matte' + str(self.matte) + '  ',
                                    rgb=self.defaultColor,
                                    cw=self.columnWidths)
        pm.colorSliderGrp(slider, edit=True, 
                                  cc=lambda *args: setMatteColor(slider, getSel()) )
        
        # RGB shortcut assignment buttons
        tritone = pm.gridLayout(numberOfColumns=4, cellWidthHeight=(17,17), p=box)
        #red
        r = pm.button(l='', bgc=(.7,.1,.1), c=lambda *args: updateColor(getSel(), slider, 'r'), p=tritone )
        pm.popupMenu()
        kmenR = pm.menuItem(l='select', c=lambda *args: selectByColorAttr(slider, self.matte, 'r') )
        #green
        g = pm.button(l='', bgc=(.1,.7,.1), c=lambda *args: updateColor(getSel(), slider, 'g'), p=tritone )
        pm.popupMenu()
        kmenG = pm.menuItem(l='select', c=lambda *args: selectByColorAttr(slider, self.matte, 'g') )
        #blue
        b = pm.button(l='', bgc=(.1,.1,.7), c=lambda *args: updateColor(getSel(), slider, 'b'), p=tritone )
        pm.popupMenu()
        kmenB = pm.menuItem(l='select', c=lambda *args: selectByColorAttr(slider, self.matte, 'b') )
        #black
        k = pm.button(l='', bgc=(0.1,0.1,0.1), c=lambda *args: updateColor(convertSel(getSel(), sh=True), slider, 'k'), p=tritone )
        pm.popupMenu()
        kmenK = pm.menuItem(l='select', c=lambda *args: selectByColorAttr(slider, self.matte, 'k') )
        
        #Get current color 
        pm.button( label='Get', width=35, p=box, c=lambda *args: getUserColorAttr(getSel(), slider, self.matte) )
        
        pm.setParent('..')
        pm.setParent('..')
        pm.separator(style='in', h=19, parent=box)
        
        return slider
       
'''Attach atributes to an object for VRayUserColor id mattes'''
def makeUserColorAttrs( sel=None ):
    
    mattes = ['A','B','C','D','E','F','X']
    
    if sel is None: ## Select all geo in the scene if no selection is specified
        chk = pm.confirmDialog(title='Really?', 
                            message='''Heads up - pressing this with nothing selected will\nadd custom attributes to all the geo in your scene.\nThis won't hurt anything, but it isn't really undoable\nand it might take a while. Continue?''', 
                            button=['Ok', 'Cancel'], 
                            defaultButton='Ok', 
                            cancelButton='Cancel', 
                            dismissString='Cancel')
        if chk == 'Ok': ## Dialog confirms the big operation
            sel = [mesh for mesh in pm.ls(type='mesh')]

    if sel is None: ## Break the operation if the user cancels.
        return False
    
    sel = convertSel(sel, sh=True)
    
    for id in mattes:
        for obj in sel:
            try:
                pm.addAttr( obj, longName=('vrayUserColor_matte' + id), nn=('matte' + id), usedAsColor=True, at='float3' )
                pm.addAttr( obj, longName=('matte'+id+'_R'), attributeType='float', parent='vrayUserColor_matte'+id )
                pm.addAttr( obj, longName=('matte'+id+'_G'), attributeType='float', parent='vrayUserColor_matte'+id )
                pm.addAttr( obj, longName=('matte'+id+'_B'), attributeType='float', parent='vrayUserColor_matte'+id )
            except: ## Checking for the attributes already existing.  Throws a warning for generic failure.
                try:
                    test = obj.attr('VRayUserColor_matte'+id).get()
                    continue
                except:
                    pass#pm.warning('Could not add some attributes')

'''Queries a selection's vrayUserColor attribute and returns it to the UI'''
def getUserColorAttr( sel, ui_obj, mat_id ):
    sel = convertSel(sel, sh=True)
    col_list = set([])
    outColor = (0,0,0)

    for obj in sel:
        try:
            col_list.add(obj.attr('vrayUserColor_matte'+mat_id).get())
        except:
            pass
    
    if len(col_list) == 1:
        outColor = col_list.pop()
    
    elif len(col_list) > 1:
        outColor = (0.27,0.27,0.27)
    
    else:
        pm.warning('Error retrieving matte'+mat_id+' color value.')
        
    pm.colorSliderGrp(ui_obj, edit=True, rgb=outColor)

def selectByColorAttr( ui_obj, mat_id, index=None ):
    meshes = pm.ls(type='mesh')
    result_list = []
    
    for obj in meshes:
        col = obj.attr('vrayUserColor_matte'+mat_id).get()
        if index == 'r' and col == (1,0,0):
            result_list.append(obj)
        if index == 'g' and col == (0,1,0):
            result_list.append(obj)
        if index == 'b' and col == (0,0,1):
            result_list.append(obj)
        if index == 'k' and col == (0,0,0):
            result_list.append(obj)
    
    pm.select(result_list)
        
'''Build matte render elements for the scene'''
def makeMatteRenderElements(*args):
    #sel = pm.ls(sl=True)
    mattes = ['A','B','C','D','E','F','X']

    for i in mattes:
        try:
            pm.PyNode('matte'+i)
        except pm.MayaNodeError:
            uc = makeUserColor(name=('matte'+i))
            exTex = makeExTex(name=('matte'+i), inTex = uc.outColor)
    print mattes
    #pm.select(sel)

'''UI Function that copies a colorSliderGrp.rgbValue to a vrayUserColor attribute'''
def setMatteColor( ui_obj, sel ):
    sel = convertSel(sel, sh=True)
    col = pm.colorSliderGrp(ui_obj, query=True, rgb=True)
    cid = pm.colorSliderGrp(ui_obj, query=True, label=True)
    [obj.attr('vrayUserColor_'+cid).set(col) for obj in sel]

'''UI Function that sets vrayUserColor matte attributes on all objects'''
def setAllMattes( matte_dict, sel ):
    
    for k,v in matte_dict.iteritems():
        col = pm.colorSliderGrp(v, query=True, rgb=True)
        cid = pm.colorSliderGrp(v, query=True, label=True)
        [obj.attr('vrayUserColor_'+cid).set(col) for obj in sel]

''' UI function that sets a random (identity) rgb-color on each object selected'''
def setRandomRGB( sel ):
    sel = convertSel(sel, sh=True)
    
    for obj in sel:
        import random as r
        col = r.randrange(0,3,1)
        if col == 0:
            obj.vrayUserColor_matteX.set(1,0,0)
        elif col == 1:
            obj.vrayUserColor_matteX.set(0,1,0)
        elif col == 2:
            obj.vrayUserColor_matteX.set(0,0,1)
        
'''UI Function that shortcuts color selection.  Updates the color selector and the custom attrs on selected objects with RGB preset buttons.'''
def updateColor( sel, ui_obj, col=None ):
    sel = convertSel(sel, sh=True)
    if col == 'R' or col == 'r':
        pm.colorSliderGrp(ui_obj, edit=True, rgb=(1,0,0))
    elif col == 'G' or col == 'g':
        pm.colorSliderGrp(ui_obj, edit=True, rgb=(0,1,0))
    elif col == 'B' or col == 'b':
        pm.colorSliderGrp(ui_obj, edit=True, rgb=(0,0,1))
    elif col == 'K' or col == 'k':
        pm.colorSliderGrp(ui_obj, edit=True, rgb=(0,0,0))

    col = pm.colorSliderGrp(ui_obj, query=True, rgb=True)
    cid = pm.colorSliderGrp(ui_obj, query=True, label=True)
    
    [obj.attr('vrayUserColor_'+cid).set(col) for obj in sel]

#####################
### PASSES UTILS ####
#####################

def makeExTex( name=None, inTex=None ):
    ''' Make an extraTex framebuffer.  Optional flags for naming (node and 
        channel) and for an incoming 3D color/vector attribute.'''
    
    pm.mel.eval('vrayAddRenderElement ExtraTexElement;')
    _fb = getLast()
    _fb.vray_considerforaa_extratex.set(0)
    if inTex:
        inTex >> _fb.vray_texture_extratex
    if name:
        _fb.vray_name_extratex.set(name)
        _fb.vray_explicit_name_extratex.set(name)
        pm.rename(_fb, name)
    return _fb


def makeUserColor( name=None ):
    ''' Make a VRay User Color node. '''

    _uc = pm.PyNode( pm.mel.eval('shadingNode -asUtility VRayUserColor;') )
    if name:
        pm.rename(_uc, 'colorNode_' + name)
    _uc.color.set(0,0,0)
    _uc.userAttribute.set(name)
    return _uc
    

#######################
### SELECTION UTILS ###
#######################

def shapesInSel( sel, xf=False, do=False, *args, **kwargs ):
    '''Finds all the shape nodes that are children/grandchildren of the current selection (or an optional specified selection).  Optional switch to get their transforms instead.'''

    result = []
    for node in sel:
        new_result = []
        new_result += node.listRelatives(ad=True, shapes=True) # getting the shapes
        if xf:
            new_result[:] = [n.getParent() for n in new_result] # swapping the list for itself, replacing with transforms
        result += new_result
    if do:
        pm.select(result)

    return result
   

def convertSel( sel, xf=False, sh=False, do=False ):
    '''Switches a mesh selection to its transforms and vice versa.  do=True selects the result.  **Applies shapesInSel() to any group node selections.'''

    result = []
    for node in sel:
        if node.nodeType() == 'transform' and not node.getShape():
            if xf:
                result += ( shapesInSel( sel, xf=True ) )
            elif sh:
                result += ( shapesInSel( sel ) )

        elif node.nodeType() == 'transform' and node.getShape():
            if xf:
                result += [ node ]
            elif sh:
                result += [ node.getShape() ]

        elif node.nodeType() == 'mesh':
            if xf:
                result += [ node.getParent() ]
            elif sh:
                result += [ node ]
            
        else: return None

    if do:
        pm.select(result)

    #try:
    #    len(result)
    #except TypeError:    
    #    result = [result]
    #    print result

    return result

def getSel():
    '''Slightly faster than typing pm.ls(sl=True)'''

    return pm.ls(sl=True)


def createOffsetGrp( sel, *args, **kwargs ):
   
    if len(sel) > 1:
        pm.error('This command only works on single selections, not multiple selections.')
        
    sel = sel[0]
    pos = sel.getTranslation( space='world' )
    rot = sel.getRotation( space='world' )
    name = sel.name()
    
    grp = pm.createNode( 'transform', n=(name + '_OffsetGrp') )
    
    grp.translate.set(pos)
    grp.rotate.set(rot)
    
    pm.parent( sel, grp )
    pm.warning('Successfully placed ' + sel + ' into group: ' + grp + '.')
    
    return grp, sel
    
def isolateSelect( sel, *args, **kwargs ):
    view = pm.paneLayout('viewPanes', q=True, pane1=True)
    # inverting a query of the current boolean state returns the toggled value
    new_state = 1-int(pm.isolateSelect( view, q=True, state=True) )
    pm.isolateSelect( view, state= new_state )
    
    if new_state == 1: # when toggling on....
        pm.isolateSelect( view, u=True )  # update with the current selection
        pm.mel.eval('enableIsolateSelect ' + view + ' true;') # and use this MEL script for some reaso

def getLast(): # stupid hacks.  (python does not return a string when using the vray command.)
    _filter = pm.itemFilter(byType='VRayRenderElement')
    _list = pm.lsThroughFilter( _filter, sort='byTime', reverse=False)
    _result = _list[len(_list)-1]
    return _result


matteAssignUI()