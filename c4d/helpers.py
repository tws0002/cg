# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 23:30:44 2010

@author: Ludovic Autin - ludovic.autin@gmail.com
"""
#C4d module
import c4d
from c4d.utils.noise import C4DNoise
#standardmodule
import sys
import os
import struct
import string
import types
import math
from math import *
from types import StringType, ListType

POSEMIXER = 100001736
POSEMORPH = 1024237
IK = 1019561
PYTAG = 1022749
Follow_PATH = 5699
LOOKATCAM = 1001001
SUNTAG=5678
DYNAMIC=180000102
CONTRAINT = 1019364 #Tcaconstraint

#OBJECT ID
BONE = 1019362
CYLINDER = 5170
CUBE = c4d.Ocube
CONE = c4d.Ocone
CIRCLE = 5181
RECTANGLE = 5186
FOURSIDE = 5180
LOFTNURBS= 5107
EXTRUDER = 5116
SWEEPNURBS=5118
TEXT = 5178
CLONER = 1018544
MOINSTANCE = 1018957
ATOMARRAY = 1001002
METABALLS = 5125
LIGHT = 5102
CAMERA = 5103
SPRING = 180000010
PATHDEFORM = 1019221
PLATONIC = c4d.Oplatonic
POLYGON = c4d.Opolygon
MESH = c4d.Opolygon
SPLINE = c4d.Ospline
INSTANCE = c4d.Oinstance
SPHERE = c4d.Osphere
EMPTY = c4d.Onull
BONES=1019362
IK=1019362
PARTICLES = 1001381
#PARAMS ID
PRIM_SPHERE_RAD = 1110

#MATERIAL ATTRIB
LAYER=1011123
GRADIANT=1011100
FUSION = 1011109

#COMMAND ID 
OPTIMIZE = 14039
RECORD = 12410
CONNECT = 12144
CONNECT_DEL = 16768
BIND = 1019881
CREATEIKCHAIN = 1019884
DESELECTALL = 12113
SELCHILDREN = 16388
FITTOVIEW = 430000774
#need an axis dictionary

#PARTICULE DATA DIC
CH_DAT_TYPE={"Real":19,"String":130,"Int":15,"Object":400006009}

#dic options
CAM_OPTIONS = {"ortho" : 1,"persp" : 0}
LIGHT_OPTIONS = {"Area" : 0,"Sun" : 3,"Spot":1}
#type of light 0 :omni, 1:spot,2:squarespot,3:infinite,4:parralel,
#5:parrallel spot,6:square parral spot 8:area

#I can record pos/rot/scale and APA for selected object using this commands.
VERBOSE=0
DEBUG=0
host = "c4d"
renderInstance = True

################################################
""" GETTERS """
################################################

### SCENE LEVEL
def getScene():
    ''' Get the active C4D scene as an object.
        usage  : getScene( none )
        returns: C4D scene object '''

    return c4d.documents.GetActiveDocument()

def getSceneName():
    ''' Get the name of the active C4D scene.
        usage  : getSceneName( none )
        returns: string '''

    doc = getCurrentScene()
    return doc.GetDocumentName()


### OBJECT LEVEL
def getName(o):
    ''' Get the name of a C4D object.
        usage  : getName( object )
        returns: string '''

    if type(o) is str:
        o = getObject(o)
    name=""    
    if o is not None :
        try:
            name = o.GetName()
        except: 
            #maybe a DejAvu
            try :
                name = o.name
            except :
                name = ""
        return name
    else :
        return name

def getObjectName(o,**kw):
    return getName(o)
    
def getObjectByName(name):
    ''' Find a C4D object in the scene by its name.
        Usage  : getObjectByName( string )
        Returns: C4D object '''
    obj=None
    if type(name) != str and type(name) != unicode : return name
    try :
        obj=getScene().SearchObject(str(name))
    except : 
        obj=None
    return obj


################################################
""" SETTERS """
################################################

def setName(o,name):
    """ Sets the name of a C4D object
        Usage  : setName( object, string )
        Returns: None """
    if name is None :
        return
    if type(o) is str:
        o = getObject(o)
    o.SetName(name)


################################################
""" DOERS """
################################################

def addObjectToScene(doc,ob,parent=None,centerRoot=True,rePos=None):
    if type(ob) is list:
        obj = ob[0]
    else :
        obj = ob
    if doc is None:
        doc = getScene()
    if self.getObject(obj.GetName()) == None:
        if parent != None : 
            if type(parent) == str : parent = self.getObject(parent)
            doc.InsertObject(obj,parent=parent)
            if centerRoot :
                currentPos = obj.GetAbsPos()         
                if rePos != None : 
                    parentPos = self.FromVec(rePos)          
                else :
                    parentPos = self.GetAbsPosUntilRoot(obj)#parent.GetAbsPos()                            
                obj.SetAbsPos(currentPos-parentPos)                
        else :    doc.InsertObject(obj)
    else :
        if parent != None :
            parent = self.getObject(parent)
            self.reParent(obj,parent)
    #add undo support
    #doc.add_undo(c4d.UNDO_NEW, obj)    
    #doc.end_undo()


################################################
""" DATATYPES """
################################################

def makeVector(points):
    if type(points) == c4d.Vector:
        return points
    else :
        return c4d.Vector(float(points[0]),float(points[1]),float(points[2]))


################################################
""" PRIMITIVES """
################################################

def makeLight(
        name,
        Type='Area',
        rgb=[1.,1.,1.],
        dist=25.0,
        energy=1.0,
        soft=1.0,
        shadow=False,
        center=(0.0,0.0,0.0),
        sc=None,
        **kw
        ):
    
    """
    type of light 0 :omni, 1:spot,2:squarespot,3:infinite,4:parralel,
    5:parrallel spot,6:square parral spot 8:area
    light sun type is an infinite light with a sun tag type
    """
    lamp = c4d.BaseObject(LIGHT)
    lamp.SetName(name)
    lamp.SetAbsPos(makeVector(center))
    lamp[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X] = pi/2.
    lamp[c4d.LIGHT_COLOR]= c4d.Vector(float(rgb[0]), float(rgb[1]), float(rgb[2]))#color
    lamp[c4d.LIGHT_BRIGHTNESS]= float(energy) #intensity
    lamp[c4d.LIGHT_TYPE]= LIGHT_OPTIONS[Type] #type
    if shadow : lamp[c4d.LIGHT_SHADOWTYPE]=1 #soft shadow map
    if Type == "Sun":
        suntag = lamp.MakeTag(SUNTAG)
    addObjectToScene(sc,lamp,centerRoot=False)    
    return lamp

    


       


    
