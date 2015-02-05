# Load external modules
import pymel.core as pm

# Load internal modules
import cg.maya.selection as selection

MATERIALS = ["lambert",
             "phong",
             "blinn",
             "SurfaceShader",
             "VRayMtl",
             "VRayBlendMtl",
             "VRayMtl2Sided",
             "VRayFastSSS",
             "VRayLightMtl",
             "VRayCarPaintMtl"
             ]


def validateShaderAssignment(obj, *a):
    connections = obj.getShape().listConnections()
    shading_groups = []
    for c in connections:
        if 'shadingEngine' in c.nodeType():
            shading_groups.append(c)
    if len(shading_groups) > 1:
        return (False, obj, shading_groups)
    elif len(shading_groups) == 0:
        return (None, obj, shading_groups)
    elif len(shading_groups) == 1:
        return (True, obj, shading_groups)
    

def generateShaderReport(squelch_valid=False, *a):
    sel = pm.ls(sl=True)
    sel = selection.convert(sel, xf=True)

    diag = pm.confirmDialog(title='Check shaders >>',
                            message='Do you want to select any meshes the script finds problems with?\nNOTE: Instanced meshes always fail, not sure why just yet.',
                            button=['Yes','No'],
                            defaultButton='Yes'
                            )

    problem_objects = []
    for obj in sel:
        sobj = str(obj).ljust(50)
        if not obj.getShape().nodeType() == 'mesh':
            continue
        valid, obj, shading_groups = validateShaderAssignment(obj)
        
        if valid and not squelch_valid:
            mat = getShader(obj, select_result=False)
            pm.warning("Object: " + sobj + " : properly shaded : " + str(mat))
        
        elif valid == False:
            #mat = []
            #for sg in shading_groups:
            #    for m in MATERIALS:
            #        mat += sg.listConnections(s=True, d=False, t=m, et=True)
            problem_objects.append(obj)
            pm.warning("Object: " + sobj + " : multiple materials")#  : " + str(mat))
        
        elif valid == None:
            problem_objects.append(obj)
            pm.warning("Object: " + sobj + " : no materials")
    
    pm.warning("::::::: REPORT COMPLETE :::::::")
    if diag == 'Yes':
        pm.select(problem_objects)
    else:
        pass
    return problem_objects


def getShader(obj=False, select_result=True, *a):
    if not obj:
        obj = selection.single()
        if not obj:
            return False
    
    if not (obj.nodeType() == 'transform'):
        pm.warning('Select the transform node of a mesh.')
        return False
               
    connections = obj.getShape().listConnections()
    validate_pass, null, shading_groups = validateShaderAssignment(obj)
    
    if not validate_pass:
        pm.warning(">>> Selected object has multiple shaders assigned. <<<")
        return False
    sg = shading_groups[0]
    for m in MATERIALS:
        found = sg.listConnections(s=True, d=False, t=m, et=True)
        if len(found):
            shader = found[0]
            if select_result:
                pm.select(shader)
            return shader


def convertColor( rgb_tuple, toFloat=True, toInt=False ):
    ''' Converts a color tuple from 0-255 to 0-1 or vice versa. Converts int to float by default. '''
    def __clamp(value):
        if value < 0: return 0
        if value > 255: return 255

    if toFloat:
        out_r = (1.0/255) * rgb_tuple[0]
        out_g = (1.0/255) * rgb_tuple[1]
        out_b = (1.0/255) * rgb_tuple[2]
        return (out_r, out_g, out_b)
    if toInt:
        out_r = __clamp(int(255 * rgb_tuple[0]))
        out_g = __clamp(int(255 * rgb_tuple[1]))
        out_b = __clamp(int(255 * rgb_tuple[2]))
        return (out_r, out_g, out_b)


def makeLayer( name=None ):
    """ A Layer creation widget that includes custom layer attributes. """

    if not name:
        run = pm.promptDialog(
                title='Create New Layer',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel'
                )
        if run == 'OK':
            name = pm.promptDialog(query=True, text=True)
        else:
            return None

    if pm.PyNode(name):
        pm.warning('Layer (or an object) with that name already exists.  Skipping...')
        return False
    else:
        lyr = pm.createRenderLayer( name=name, number=1, empty=True )

    return lyr


def getAllLayers():
    """ Returns a list of all render layers. """
    return [layer for layer in pm.ls(type='renderLayer') if not 'defaultRenderLayer' in str(layer)]


def enableOverride( attr ):
    ''' Enables the override of a specified attribute on the current render layer. '''
    enabled = pm.editRenderLayerAdjustment( query=True )

    if not enabled or not attr in enabled:
        pm.editRenderLayerAdjustment( attr )

    return True


def calibrationGeo(ren='vray', toggle=True):
    ''' Creates objects to assist in lighting calibration for photometric and VFX workflows. '''
    ####: REN
    # 1 : mentalRay
    # 2 : V-ray

    ####: ARGS
    # 1 : create
    # 2 : delete

    if toggle is True:
        
        # cleanup check
        if pm.objExists('LGT_REF_OBJ') | pm.objExists('diff_18SG') | pm.objExists('diff_18'):
            pm.delete('diff_80', 'diff_18', 'refl_100', 'refl_75', 'diff_18SG', 'diff_80SG', 'refl_01SG', 'refl_02SG', 'LGT_REF_OBJ')
        
        # create four spheres & a plane
        tmp1 = pm.polySphere(r = 1, n = "fBall_D1", ch = 0)
        diff01 = tmp1[0]
        tmp1 = pm.polySphere(r = 1, n = "fBall_D2", ch = 0)
        diff02 = tmp1[0]
        tmp1 = pm.polySphere(r = 1, n = "fBall_R1", ch = 0)
        refl01 = tmp1[0]
        tmp1 = pm.polySphere(r = 1, n = "fBall_R2", ch = 0)
        refl02 = tmp1[0]
        tmp1 = pm.polyPlane (n = "fGround", ch = 1)
        grid01 = tmp1[0]
        objs = [diff01, diff02, refl01, refl02, grid01]
        
        #shds = [shd_diff_80, shd_diff_18, shd_refl_01, shd_refl_02]
        #shgs = [shg_diff_80, shg_diff_18, shg_refl_01, shg_refl_02]
        
        # group them
        pm.group(diff01, diff02, refl01, refl02, grid01, n = "LGT_REF_OBJ")
        
        # move them around
        offset = 4.5
        
        for o in objs:
            o.translateX.set(offset)
            offset = offset -3
            
        grid01.scaleX.set(50)
        grid01.scaleZ.set(50)
        grid01.translateX.set(0)
        grid01.translateY.set(-10)
        
        # create shaders
        # 80% diffuse goes to mesh diff01
        shg_diff_80 = pm.sets(n = "diff_80SG", renderable = 1, empty = 1)
        shd_diff_80 = pm.shadingNode('lambert', asShader = 1, n = "diff_80")
        shd_diff_80.diffuse.set(0.8)
        shd_diff_80.color.set(1, 1, 1)
        pm.surfaceShaderList(shd_diff_80, add = shg_diff_80)
        pm.sets(shg_diff_80, e = 1, forceElement = diff01)
        
        # 18% diffuse goes to mesh diff02
        shg_diff_18 = pm.sets(n = "diff_18SG", renderable = 1, empty = 1)
        shd_diff_18 = pm.shadingNode('lambert', asShader = 1, n = "diff_18")
        shd_diff_18.diffuse.set(0.18)
        shd_diff_18.color.set(1, 1, 1)
        pm.surfaceShaderList(shd_diff_18, add = shg_diff_18)
        pm.sets(shg_diff_18, e = 1, forceElement = diff02)
        
        
        ### REFLECTION SPHERES DEPEND ON DIFFERENT SHADERS FOR MENTALRAY / VRAY ###
        
        if ren is 'mray':
        
            # (MENTALRAY) 100% glossy mia goes to mesh refl01
            shg_refl_01 = pm.sets(n = "refl_01SG", renderable = 1, empty = 1)
            shd_refl_01 = pm.shadingNode('mia_material_x_passes', asShader = 1, n = "refl_100")
            shd_refl_01.diffuse_weight.set(0)
            shd_refl_01.reflectivity.set(1)
            pm.disconnectAttr('lambert1.outColor', shg_refl_01.surfaceShader)
            pm.connectAttr(shd_refl_01.message, shg_refl_01.miMaterialShader)
            pm.sets(shg_refl_01, e = 1, forceElement = refl01)
            
            # (MENTALRAY) 75% glossy mia goes to mesh refl02
            shg_refl_02 = pm.sets(n = "refl_02SG", renderable = 1, empty = 1)
            shd_refl_02 = pm.shadingNode('mia_material_x_passes', asShader = 1, n = "refl_75")
            shd_refl_02.diffuse_weight.set(0)
            shd_refl_02.reflectivity.set(1)
            shd_refl_02.refl_gloss.set(0.75)
            pm.disconnectAttr('lambert1.outColor', shg_refl_02.surfaceShader)
            pm.connectAttr(shd_refl_02.message, shg_refl_02.miMaterialShader)
            pm.sets(shg_refl_02, e = 1, forceElement = refl02)
        
        if ren is 'vray':
            
            # (VRAY) 100% glossy vraymtl goes to mesh refl01
            shg_refl_01 = pm.sets(n = "refl_01SG", renderable = 1, empty = 1)
            shd_refl_01 = pm.shadingNode('VRayMtl', asShader = 1, n = "refl_100")
            shd_refl_01.diffuseColorAmount.set(0)
            shd_refl_01.reflectionColor.set(1,1,1)
            pm.surfaceShaderList(shd_refl_01, add = shg_refl_01)
            pm.sets(shg_refl_01, e = 1, forceElement = refl01)
            
            # (VRAY) 75% glossy vraymtl goes to mesh refl02
            shg_refl_02 = pm.sets(n = "refl_02SG", renderable = 1, empty = 1)
            shd_refl_02 = pm.shadingNode('VRayMtl', asShader = 1, n = "refl_75")
            shd_refl_02.diffuseColorAmount.set(0)
            shd_refl_02.reflectionColor.set(1,1,1)
            pm.surfaceShaderList(shd_refl_02, add = shg_refl_02)
            pm.sets(shg_refl_02, e = 1, forceElement = refl02)


    if toggle is False:
        pm.delete('diff_80', 'diff_18', 'refl_100', 'refl_75', 'diff_18SG', 'diff_80SG', 'refl_01SG', 'refl_02SG', 'LGT_REF_OBJ')

