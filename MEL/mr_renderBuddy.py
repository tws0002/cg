import pymel.core as pm

def renderBuddy(ren, arg=1):

####: REN
# 1 : mentalRay
# 2 : V-ray

####: ARGS
# 1 : create
# 2 : delete

    if arg is 1:
        
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
        grp = pm.group(diff01, diff02, refl01, refl02, grid01, n = "LGT_REF_OBJ")
        grp.translateY.set(10)
        
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
        
        if ren is 1:
        
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
        
        if ren is 2:
            
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


    if arg is 2:
        pm.delete('diff_80', 'diff_18', 'refl_100', 'refl_75', 'diff_18SG', 'diff_80SG', 'refl_01SG', 'refl_02SG', 'LGT_REF_OBJ')