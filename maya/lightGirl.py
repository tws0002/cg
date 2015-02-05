import pymel.core as pm

class Light(object):
    """
    This class unifies the naming, behavior, attributes and
    conventions of V-Ray and default maya lights, for use in
    my pipeline tools and LightBuddy lighting utilities.
    """
    class Attr(object):
        """
        An object which maps Light object attributes to maya object attributes.
        """
        def __init__(self, obj, target_attr):
            """
            Declares the mapped target attribute.
            """
            self.reference = target_attr
            self.obj = obj

        def set(self, value):
            """
            Sets the connected Maya attribute's value.
            """
            self.obj.attr(self.reference).set(value)

        def get(self):
            """
            Gets the connected Maya attribute's value.
            Returns the value.
            """
            return self.obj.attr(self.reference).get()

    def __init__(self, obj):
        self.init(obj)

    def __len__(self):
        return False

    def init(self, obj):
        """
        Based on the type of light passed to the class on instantiation, this function
        maps itself to the light's attributes and functions as a wrapper to that light.
        """
        self.type = str(obj.nodeType())
        self.name = str(obj.getParent())

        if not 'Light' in self.type:
            pm.error('Light validation error')
        
        if 'VRay' in self.type:
            # booleans init
            self.enabled = self.Attr(obj, 'enabled')
            self.shadows = self.Attr(obj, 'shadows')
            self.invisible = self.Attr(obj, 'invisible')
            self.noFalloff = self.Attr(obj, 'noDecay')
            self.doubleSided = self.Attr(obj, 'doubleSided')
            # light intensity & color init
            self.intensity = self.Attr(obj, 'intensityMult')
            self.color = self.Attr(obj, 'lightColor')
            # specular settings init
            self.specularEnable = self.Attr(obj, 'affectSpecular')
            self.specularWeight = self.Attr(obj, 'specularContrib')
            # diffuse settings init
            self.diffuseEnable = self.Attr(obj, 'affectDiffuse')
            self.diffuseWeight = self.Attr(obj, 'diffuseContrib')
            # raytracing settings init
            self.reflectionEnable = self.Attr(obj, 'affectReflections')
            self.subdivs = self.Attr(obj, 'subdivs')

        elif 'Light' in self.type:
            # booleans init
            self.shadows = self.Attr(obj, 'useRayTraceShadows')
            # light intensity & color
            self.intensity = self.Attr(obj, 'intensity')
            self.color = self.Attr(obj, 'color')
            # specular settings
            self.specularEnable = self.Attr(obj, 'emitSpecular')
            # diffuse settings
            self.diffuseEnable = self.Attr(obj, 'emitDiffuse')
            # shadow settings
            self.lightAngle = self.Attr(obj, 'lightAngle')
            self.shadowSamples = self.Attr(obj, 'shadowRays')
            self.shadowColor = self.Attr(obj, 'shadowColor')
            # falloff settings (enum 1,2,3,4)
            self.falloff = self.Attr(obj, 'decayRate')

        if 'spot' in self.type:
            # unique spot light attributes
            self.coneAngle = self.Attr(obj, 'coneAngle')
            self.penumbraAngle = self.Attr(obj, 'penumbraAngle')
            self.dropoff = self.Attr(obj, 'dropoff')


class ActiveLights(object):
    def __init__(self):
        self.current = []

    def __len__(self):
        return len(self.current)

    def append(self, *light_obj):
        self.current += list((light_obj))
        return self.current
    
    def clear(self):
        self.current = []
        return self.current
            

class LightInterfaceElement(object):
    """
    A generator object for a UI frameLayout element (and children) to modify 
    lightBuddy lights.
    """

    def __init__(self, light_obj, parent):
        
        self.labelWidth = (1,75)
        # Case 1: A list of light objects, to be made into a group for quick editing
        if len(light_obj):
            self.groupMode = True
            # If the input is a list of light objects,  check that they are
            # all of the same type
            if self.checkTypes(light_obj):
                self.lightList = light_obj
                self.name = [(l.name + ", ") for l in self.lightList]
            else: 
                pm.error('Cannot group lights of different types.')
        
        # Case 2: A single Light object, with a valid .type attribute
        elif light_obj.type:
            self.groupMode = False
            self.light = light_obj
            self.name = light_obj.name

        # The business: build the UI element, either as a single element linked 
        # to multiple identical lights (Case 1: groupMode), 
        # or a single element per light (Case 2: not groupMode)
        if self.groupMode:
            self.build(self.lightList, parent)
        elif not self.groupMode:
            self.build(self.light, parent)


    def build(self, light_obj, parent):
        """
        Generates the frameLayout element, along with its children.
        Returns the element as a pymel object.
        """
        self.element = pm.frameLayout( l=self.name, 
                                       fn='smallBoldLabelFont', 
                                       mh=5, bv=True, ebg=True, 
                                       cll=True, cl=True, 
                                       parent=parent
                                       )
        col = pm.columnLayout()
        
        # light color selector
        slider = pm.colorSliderGrp( label='Light Color',
                                    rgb=light_obj.color.get(),
                                    cw=[self.labelWidth,(2,75),(3,0)],
                                    p=col
                                    )
        pm.colorSliderGrp ( slider,
                            edit=True,
                            cc=lambda *args: light_obj.color.set(pm.colorSliderGrp(slider, q=True, rgbValue=True))
                            )

        # intensity 
        intensity = pm.floatFieldGrp( value=(light_obj.intensity.get(),0,0,0),
                                      label='Intensity',
                                      cw=[self.labelWidth,(2,75)],
                                      nf=1,
                                      p=col
                                      )

        #self.element.redistribute()
        return self.element    


    def checkTypes(self, light_obj_list):
        """
        When a list is passed to the object on instantiation, this function
        checks to make sure that all the Light objects are of the same type.
        """
        try:
            light_type_list = [t.type for t in light_obj_list]
            light_type_list = iter(light_type_list)
            first = next(light_type_list)
            return all(first == rest for rest in light_type_list)
        except StopIteration:
            return True
        except:
            return False


class LightBuddy(object):
    def __init__(self):
        self.activeLights = ActiveLights()
        self.run(self.activeLights)

    # not currently working
    def addLight(self, *a):
        sel = pm.ls(sl=True)
        lights = [Light(lt) for lt in sel if 'Light' in lt.nodeType() or 'Light' in lt.nodeType.getShape()]
        self.activeLights.append(lights)
        self.refresh(self.activeLights)

    def refresh(self, active_lights):
        return self.run(active_lights)

    def run(self, active_lights):
        # window name definitions
        try: pm.deleteUI('lightBuddyUI')
        except: pass
        lightBuddyUI = pm.window('lightBuddyUI',
                                 title = 'Light Buddy',
                                 width = 300,
                                 s = False,
                                 tlb = True
                                 )

        #
        mainBox = pm.formLayout()
        ##
        row = pm.formLayout(p=mainBox)
        addSelBtn = pm.button( label='Add Light(s)',
                               c=self.addLight,
                               p=row)
        addGrpBtn = pm.button(label='Add Lights as Group', p=row)
        clearBtn = pm.button(label='Clear All', p=row)
        row.flip()
        row.redistribute()
        ##
        col = pm.formLayout(p=mainBox)

        # 

        for lt in active_lights.current:
            element = LightInterfaceElement(lt, col)
        
        col.redistribute()
        #
        mainBox.redistribute()

        pm.showWindow(lightBuddyUI)
        return lightBuddyUI

