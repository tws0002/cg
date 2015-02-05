import pymel.core as pm

#######################
### SELECTION UTILS ###
#######################

def shapes( sel, xf=False, do=False, *args, **kwargs ):
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

def single( *a ):
    sel = pm.ls(sl=True)
    if len(sel) > 1 or sel == None:
        pm.warning('Invalid selection.')
        return False
    else:
        return sel[0]
   
def convert( sel, xf=False, sh=False, do=False ):
    '''Switches a mesh selection to its transforms and vice versa.  do=True selects the result.  **Applies shapesInSel() to any group node selections.'''

    result = []
    for node in sel:
        if node.nodeType() == 'transform' and not node.getShape():
            if xf:
                result += ( shapes( sel, xf=True ) )
            elif sh:
                result += ( shapes( sel ) )

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

def get(*a):
    '''Slightly faster than typing pm.ls(sl=True)'''

    return pm.ls(sl=True)

def createOffsetGrp( sel, *args, **kwargs ):
   
    #if len(sel) > 1:
    #    pm.error('This command only works on single selections, not multiple selections.')
    
    for obj in sel:   
        #sel = sel[0]
        try: par = obj.getParent()
        except: par = None

        pos = obj.getTranslation( space='world' )
        rot = obj.getRotation( space='world' )
        name = obj.name()
        
        grp = pm.createNode( 'transform', n=(name + '_OffsetGrp') )
        
        grp.translate.set(pos)
        grp.rotate.set(rot)
        
        pm.parent( obj, grp )
        if par:
            pm.parent( grp, par )
        pm.warning('Successfully placed ' + obj + ' into group: ' + grp + '.')
    
    return grp, sel
    
def isolateSelect( sel, *args, **kwargs ):
	view = pm.paneLayout('viewPanes', q=True, pane1=True)
	# inverting a query of the current boolean state returns the toggled value
	new_state = 1-int(pm.isolateSelect( view, q=True, state=True) )
	pm.isolateSelect( view, state= new_state )
	
	if new_state == 1: # when toggling on....
		pm.isolateSelect( view, u=True )  # update with the current selection
		pm.mel.eval('enableIsolateSelect ' + view + ' true;') # and use this MEL script for some reason
