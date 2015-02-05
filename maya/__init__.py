#import pymel.core as pm

#import rendering
#reload(rendering)
#print 'Loaded renderLayers'

#import selection
#reload(selection)
#print 'Loaded selectionUtils'

#import uvWidget
#reload(uvWidget)
#print 'Loaded uvWidget'

#import visibilityKeyer
#reload(visibilityKeyer)
#print 'Loaded visibilityKeyer'

#import cameraUtils
#reload(cameraUtils)
#print 'Loaded cameraUtils'

#import lightGirl
#reload(lightGirl)
#print 'Loaded LightGirl 2000'


# #####################################################################################################################################
# SIDEBAR USER INTERFACE    ###########################################################################################################
# #####################################################################################################################################
def null (*args):
    pass
    
def sidebar( *args ):
    import rendering
    import selection
    import uvWidget
    import visibilityKeyer
    import cameraUtils
    import vrayUtils.mattes
    import vrayUtils.calculator
    import vrayUtils.utils
    #import lightGirl
    
    ''' Sidebar for wtools utilities '''
    if pm.dockControl('wtoolsDock', query=True, exists=True):
        pm.deleteUI('wtoolsDock')

    allowedAreas = ['right', 'left']

    wtoolsUI = pm.window( title='wtools', iconName='mrB' )

    _mainmr = pm.columnLayout( adjustableColumn=False, w=123 )


    # ###########################################################################################
    """ Interface section """
    # ###########################################################################################


    frame = pm.frameLayout(l='Interface', fn='smallBoldLabelFont', w=123, mh=5, bv=True, ebg=True, cll=True, cl=False, parent=_mainmr)

    grid = pm.gridLayout( nc=1, cellWidthHeight=(120,33))
    hypershade_btn = pm.button( l="hypershade :(",
                                w=120, h=33,
                                c=lambda *args: pm.Mel.eval('HypershadeWindow;') )
    uvEditor_btn = pm.button( l="uvs",
                                w=120, h=33,
                                c=lambda *args: pm.Mel.eval('TextureViewWindow;') )
    scriptEd_btn = pm.button( l="script editor",
                                w=120, h=33,
                                c=lambda *args: pm.Mel.eval('ScriptEditor;') )
    renderGlob_btn = pm.button( l="render globals",
                                w=120, h=33,
                                c=lambda *args: pm.Mel.eval('unifiedRenderGlobalsWindow;') )
    pm.setParent('..')


    grid = pm.gridLayout( nc=2, cellWidthHeight=(60,25))
    vray_vfb_btn = pm.button( l="v-Ray vfb",
                                w=120, h=33,
                                c=lambda *args:pm.Mel.eval('vray showVFB;') )
    renderview_btn = pm.button( l="render view",
                                w=120, h=33,
                                c=lambda *args: pm.Mel.eval('RenderViewWindow;') )
    pm.setParent('..')


    grid = pm.gridLayout( nc=3, cellWidthHeight=(40,40) )
    min_interface_btn = pm.button( l="|", 
                                   bgc=[0.18,0.18,0.18],
                                   c=lambda *args: mr_viewport(2),
                                   ann='Minimum interface.' )
    mid_interface_btn = pm.button( l="(o)", 
                                   bgc=[0.37,0.37,0.37],
                                   c=lambda *args: mr_viewport(1),
                                   ann='Reduced interface.' )
    max_interface_btn = pm.button( l="( o )", 
                                   bgc=[0.8,0.8,0.8],
                                   c=lambda *args: mr_viewport(0),
                                   ann='Full interface.' )
    pm.setParent('..')


    # ###########################################################################################
    """ Selection & Visibility """
    # ###########################################################################################


    frame = pm.frameLayout(l='Select & Visibility', fn='smallBoldLabelFont', width=123, mh=5, bv=True, ebg=True, cll=True, cl=True, parent=_mainmr)

    grid = pm.gridLayout( nc=1, cellWidthHeight=(120,33), p=frame )
    isolate_select_btn = pm.button( l='isolate // view selected',
    								c=lambda *args: selection.isolateSelect( pm.ls(sl=True) ),
    								ann='Toggle isolate select on selection.',
                                    p=grid )
    meshes_btn = pm.button( l="select meshes",
                            c=lambda *args: selection.convert( pm.ls(sl=True), xf=True, do=True ),
                            ann="Convert your selection to geometry-level transforms only.\nRight click for shape nodes.",
                            p=grid )
    pm.popupMenu()
    shapes_btn = pm.menuItem(l='Shapes only...', c=lambda *args: selection.convert( pm.ls(sl=True), sh=True, do=True ) )
    shaders_btn = pm.button( l="shader on selection",
                             c=lambda *args: rendering.getShader(pm.ls(sl=True)[0], select_result=True),
                             ann="Convert your selection to geometry-level transforms only.\nRight click for shape nodes.",
                             p=grid )

                            
    # #### ORGANIZATION SECTION ###
    col = pm.columnLayout( adjustableColumn=True, w=120, p=frame )
    #brk = pm.separator( st='in', h=5, p=col )
    lbl = pm.text(l='-  o r g a n i z a t i o n  -', p=col )
    #brk = pm.separator( st='none', h=5, p=col )

    group_under_btn = pm.button( l="make offset group",
                                 c=lambda *args: selection.createOffsetGrp( pm.ls(sl=True) ),
                                 h=25,
                                 ann='Copy the selection\'s transform matrix to a group and parent the selection under it.',
                                 p=col )

    # #### VISIBILIY KEYER UTILITY ###
    col = pm.columnLayout( adjustableColumn=True, p=frame )
    #brk = pm.separator( st="in", h=5, p=col )
    lbl = pm.text(l='- v i s   k e y e r -', p=col )

    row = pm.rowLayout( nc=4 )
    clear_off_btn = pm.button( l="|", c = lambda *args: visibilityKeyer.vizClear( pm.ls(sl=True), 0 ), w=17, h=40, bgc=[0.1, 0.1, 0.1], p=row )
    key_off_btn = pm.button( l="", c = lambda *args: visibilityKeyer.vizKeyOff( pm.currentTime(), pm.ls(sl=True) ), w=40, h=40, bgc=[0.18, 0.18, 0.18], p=row ) # Clarified lambda: vis_go( intField value, selection )
    key_on_btn = pm.button( l="", c = lambda *args: visibilityKeyer.vizKeyOn( pm.currentTime(), pm.ls(sl=True) ), w=40, h=40, bgc=[0.8, 0.8, 0.8], p=row ) # Clarified lambda: vis_go( intField value, selection )
    clear_on_btn = pm.button( l="O", c = lambda *args: visibilityKeyer.vizClear( pm.ls(sl=True), 1 ), w=17, h=40, bgc=[0.9, 0.9, 0.9], p=row )


    ############################################################################################
    """ Lighting """
    ############################################################################################

    frame = pm.frameLayout(l='Rendering', fn='smallBoldLabelFont', width=123, mh=10, bv=True, ebg=True, cll=True, cl=True, parent=_mainmr)

    col = pm.columnLayout( p=frame )

    #BUTTON - Initial scene setup
    basic_globals_btn = pm.button( l="Initial Scene Setup", 
                                   h=20, w=120,
                                   bgc = [0.76, 0.18, 0.1],
                                   c=lambda *args: vrayUtils.utils.setVrayDefaults(),
                                   ann='Set the basic render globals for this scene, and create a scene controller',
                                   p=col )

    #BUTTON - RENDER                               
    bigass_render_btn = pm.button( l="RENDER", 
                                   h=120, w=120,
                                   bgc = [0.1, 0.54, 0.76],
                                   c=lambda *args: pm.mel.eval('renderIntoNewWindow render;'),
                                   ann='RENDER',
                                   p=col )

    #BUTTON - VFB
    #BUTTON - RenderView
    grid = pm.gridLayout( nc=2, nr=2, cellWidthHeight=(60,15), p=frame )
    GI_bruteForce_btn = pm.button( l="V-Ray FB",
    							   bgc=[0.37, 0.37, 0.37], 
                                   c=lambda *args: pm.PyNode('vraySettings').vfbOn.set(1),
                                   ann='Use V-Ray Framebuffer.',
                                   p=grid )

    GI_irradianceMap_btn = pm.button( l="Maya FB",
    								  bgc=[0.37, 0.37, 0.37],  
                                      c=lambda *args: pm.PyNode('vraySettings').vfbOn.set(0),
                                      ann='Use Maya RenderView',
                                      p=grid )

    use_vray_vfb_btn = pm.button( l="50 %",
    							  bgc=[0.18, 0.18, 0.18], 
                                  c=lambda *args: pm.mel.eval('setTestResolutionVar(4);'),
                                  ann='Use V-Ray Framebuffer.',
                                  p=grid )

    use_maya_fb_btn = pm.button( l="100 %",
    							 bgc=[0.8, 0.8, 0.8],  
                                 c=lambda *args: pm.mel.eval('setTestResolutionVar(1);'),
                                 ann='Use Maya RenderView',
                                 p=grid )

    #BUTTON - SUBMIT TO FARM
    submit_farm_btn = pm.button( l='SUBMIT TO FARM',
                                 h=50, w=120,
                                 bgc=[0.48, 0.76, 0.1],
                                 c=lambda *args: pipeline.submit.run(),
                                 ann='Submit to Qube',
                                 p=col )


    # Lighting utils
    col = pm.columnLayout( adjustableColumn=True, p=frame )
    lbl = pm.text(l='-  l i g h t i n g  -', p=col )

    bgc = [0.27,0.27,0.27]

    grid = pm.gridLayout( nc=1, cellWidthHeight=(120,27), p=frame )
    #BUTTON - Two-sided lighting toggle
    two_sided_lighting_btn = pm.button( l = 'two-sided lighting',
    									bgc = bgc,
    									c = lambda *args: pm.modelEditor(pm.paneLayout('viewPanes', q=True, pane2=True), 
    																	 edit=True, 
    																	 twoSidedLighting=( 1 - pm.modelEditor( pm.paneLayout('viewPanes', q=True, pane2=True), query=True, twoSidedLighting=True) )),
    									ann = 'Toggle two-sided lighting on and off.',
                                        p=grid )

    #BUTTON - VRay Object Properties
    make_object_properties_btn = pm.button( l = 'v-ray geo properties',
    	 									bgc = [0.18,0.18,0.18],
    							 			c = lambda *args: vrayUtils.utils.makeObjectProperties( pm.ls(sl=True) ),
    							 			ann = 'Make a V-Ray object properties group.',
                                            p=grid )
    pm.popupMenu()
    append_geo_menu = pm.menuItem(l='Add to existing ...', c=lambda *args: vrayUtils.utils.addToSet( typ='geo' ) )

    #BUTTON - VRay Light Properties
    make_object_properties_btn = pm.button( l = 'v-ray light set',
    										bgc = [0.18,0.18,0.18],
    							 			c = lambda *args: vrayUtils.utils.makeLightSelectSet( pm.ls(sl=True) ),
    							 			ann = 'Make a V-Ray light select set.',
                                            p=grid )
    pm.popupMenu()
    append_lgt_menu = pm.menuItem(l='Add to existing ...', c=lambda *args: vrayUtils.utils.addToSet( typ='lgt' ) )

    #BUTTON - VRay Displacement Properties
    make_object_properties_btn = pm.button( l = 'v-ray disp / subd set',
    										bgc = [0.18,0.18,0.18],
    							 			c = lambda *args: vrayUtils.utils.makeLightSelectSet( pm.ls(sl=True) ),
    							 			ann = 'Make a V-Ray light select set.',
                                            p=grid )                                        
                                            

    # Rendering utils
    col = pm.columnLayout( adjustableColumn=True, p=frame )
    #brk = pm.separator( st="in", h=5, p=col )
    lbl = pm.text(l='-  r e n d e r i n g  -', p=col)

    col = pm.gridLayout( nc=1, cellWidthHeight=(120,20), p=frame )

    #BUTTON - bake & export camera
    generate_tech_passes_btn = pm.button( l = 'bake + export camera',
    									  bgc = bgc,
    									  c = lambda *args: cameraUtils.bakeScene(),
    									  ann = 'Bake the selected camera and export scene for AE',
                                          p=col )
    pm.popupMenu()
    cameraonly_btn = pm.menuItem(l='Bake camera only', c=lambda *args: cameraUtils.bakeCamera())
    cameraexp_btn =  pm.menuItem(l='Bake camera only (export)', c=lambda *args: cameraUtils.bakeCamera(exp=True))


    #BUTTON - Generate tech passes
    generate_tech_passes_btn = pm.button( l = 'generate tech passes',
    									  bgc = bgc,
    									  c = null,#vrayUtils.utilityRenderElements,
    									  ann = 'Create tech passes for the scene.',
                                          p=col )


    #BUTTON - Open mattes widget
    matte_assign_ui_btn = pm.button( l = 'matte widget',
    								 bgc = [0.8, 0.8, 0.8],
    								 c = vrayUtils.mattes.run,
    								 ann = 'Open the matte assignment utility window',
                                     p=col )

    #BUTTON - Samples calculator
    matte_assign_ui_btn = pm.button( l = 'samples calculator',
    								 bgc = [0.8, 0.8, 0.8],
    								 c = vrayUtils.calculator.run,
    								 ann = 'Open the V-Ray DMC samples calculator.',
                                     p=col )
                                     
                                     
    ############################################################################################
    """ UVs """
    ############################################################################################


    frame = pm.frameLayout(l='UVs', fn='smallBoldLabelFont', width=123, mh=5, bv=True, ebg=True, cll=True, cl=True, parent=_mainmr)

    col = pm.columnLayout( width=120 )
    xfer_btn = pm.button( l="C O P Y   U V s", 
                          w=120, h=33, bgc=[0,0.38,0.52], 
                          c=lambda *args: uvWidget.transfer_uvs, 
                          ann='Select target meshes first, then source mesh.',
                          p=col )
    #pm.separator( st='in', h=5 )
    snap_btn = pm.button( l="S N A P S H O T", 
                          w=120, h=33, bgc=[0.52,0,0], 
                          c=lambda *args: uvWidget.snapshot_uvs( pm.intField( res_int, q=True, v=True ) ),
                          p=col )
                          
    row = pm.rowLayout( nc=2, p=col )
    lbl = pm.text( l="Resolution: ", align='right', fn='smallPlainLabelFont', p=row )
    res_int = pm.intField( v=1024, w=50, p=row )

    frame = pm.frameLayout(l='Notes', fn='smallBoldLabelFont', width=123, mh=5, bv=True, ebg=True, cll=True, cl=True, parent=_mainmr)

    notes_box = pm.scrollField( w=120, h=260, editable=True, wordWrap=True, p=frame )


    dock = pm.dockControl( 'wtoolsDock', label='wtools', area='left', content=wtoolsUI, allowedArea=allowedAreas)



    def mr_viewport(x):
        if x == 0:   
            pm.Mel.eval('setHelpLineVisible true;')
            pm.Mel.eval('setToolboxVisible true;')
            pm.Mel.eval('setStatusLineVisible true;')
            pm.Mel.eval('setShelfVisible true;')
            pm.Mel.eval('setCommandLineVisible true;')
            pm.Mel.eval('setTimeSliderVisible true;')
            pm.Mel.eval('setPlaybackRangeVisible true;')
            x = 1
        elif x == 1:
            pm.Mel.eval('setHelpLineVisible false;')
            pm.Mel.eval('setToolboxVisible false;')
            pm.Mel.eval('setStatusLineVisible true;')
            pm.Mel.eval('setShelfVisible false;')
            pm.Mel.eval('setCommandLineVisible true;')
            pm.Mel.eval('setTimeSliderVisible true;')
            pm.Mel.eval('setPlaybackRangeVisible false;')
            x = 2
        elif x == 2:
            pm.Mel.eval('setHelpLineVisible false;')
            pm.Mel.eval('setToolboxVisible false;')
            pm.Mel.eval('setStatusLineVisible false;')
            pm.Mel.eval('setShelfVisible false;')
            pm.Mel.eval('setCommandLineVisible false;')
            pm.Mel.eval('setTimeSliderVisible true;')
            pm.Mel.eval('setPlaybackRangeVisible false;')
            x = 0


#sidebar()
#main_menu()
