import pymel.core as pm
import pymel.core.datatypes as dt



"""Description: Builds a local rotation / translation matrix based on specified vertices and a vector defining the origin."""

def mk_xform( vtx_X, vtx_Z, local_origin ):

    X_axis = dt.Vector(vtx_X.getPosition('object')) - local_origin
    Z_axis = dt.Vector(vtx_Z.getPosition('object')) - local_origin
    Y_axis = dt.cross(Z_axis, X_axis) # Cross product gets the Y
    X_axis = dt.cross(Y_axis, Z_axis) # X is recalculated for perfect orthogonality.  X gets the least respect in this method.

    return dt.Matrix(X_axis.normal(), Y_axis.normal(), Z_axis.normal(), local_origin) # Scale / shear is tossed out here.


"""
Description: Uses mk_xform() to build a new rotation / translation matrix which is then: a) inversely applied to the vertices 
and b) applied to the transform node, effectively restoring a valid transformation matrix. Scale / shear are not considered.
"""
def unfreeze_xform( vtx_X, vtx_Z, test=False ):

    obj = vtx_Z.node() # Get the object the vertex belongs to -- should probably add some error checking here at some point.
    user_pivot = obj.getParent().getPivots()[0] # Get the rotate pivot from the object, 0 index is object/local
    user_matrix = mk_xform( vtx_X, vtx_Z, user_pivot ) # Make the user-defined rotate / translate matrix
    
    if test: # Special case flag for testing the user matrix on an object before executing
        loc = pm.createNode('locator', n='pivotTestLocShape')
        loc.getParent().setMatrix( user_matrix )

    else: # Do the business
        for verts in obj.verts:
            verts.setPosition( verts.getPosition() * user_matrix.inverse() ) # Invert the matrix transform on every vert

        obj.getParent().centerPivots() # Set the object pivot to the new object origin
        obj.getParent().setMatrix( user_matrix ) # Reapply the matrix transform
   

"""Description:  Just a ui function for storing / reading text fields"""
def ui_vtx_sel( txt_field, edit=False, query=False ):

    if edit: # mode for editing the text field input with a new selection
        sel = pm.ls(sl=True)[0]
        pm.textField( txt_field, edit=True, tx=sel )
    else: pass
    
    if query: # mode for querying the text field input and returning the named node
        node = pm.PyNode( pm.textField( txt_field, query=True, tx=True ) )
        return node
    else: pass


"""
UI
"""
if 'ufXformWin' in locals():
    del ufXformWin
ufXformWin = pm.window( title="Unfreeze Xform", iconName='UNFXFORM', widthHeight=(200, 68), s=False, tlb=True )

pm.columnLayout( adjustableColumn=True)
pm.text( l="Verts to define X & Z axis: ", align='right', fn='smallPlainLabelFont' )
pm.setParent( '..' )

pm.rowColumnLayout( nc=2 )
txt_az = pm.textField( tx='', w=150 )
btn_az = pm.button( l="Z - a x i s", h=17, bgc=[0,0.38,0.52], c=lambda *args: ui_vtx_sel( txt_az, edit=True ) )
txt_ax = pm.textField( tx='', w=150 )
btn_ax = pm.button( l="X - a x i s", h=17, bgc=[0.52,0,0], c=lambda *args: ui_vtx_sel( txt_ax, edit=True ) )
pm.setParent( '..' )

pm.separator( style='in', h=5 )

pm.rowLayout( nc=2 )
btn_unf = pm.button( l="U n f r e e z e",
                     h=25, 
                     w=100, 
                     bgc=[0.18, 0.18, 0.18], 
                     c=lambda *args: unfreeze_xform( ui_vtx_sel( txt_ax, query=True ), ui_vtx_sel( txt_az, query=True ) ) )
btn_test = pm.button( l="T e s t   P i v o t", 
                      h=25, 
                      w=100, 
                      bgc=[0.18, 0.18, 0.18], 
                      c=lambda *args: unfreeze_xform( ui_vtx_sel( txt_ax, query=True ), ui_vtx_sel( txt_az, query=True ), test=True ) )
pm.setParent( '..' )

pm.showWindow( ufXformWin )


"""
take the two vertex strings in the boxes
strip off the shape name and store the vertex ids
for each object selected
    slap the vertex id onto the end of the name
    store those vert objects
    run unfreeze_xform() on that object


debug code

vx = pm.PyNode('pSphereShape1.vtx[199]')
vz = pm.PyNode('pSphereShape1.vtx[381]')
"""
