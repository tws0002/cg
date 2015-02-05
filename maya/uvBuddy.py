import pymel.core as pm

#function to propagate uvs from one object to many
def transfer_uvs( *args ):
    c=0
    sel = pm.ls(selection=True)
    src_obj = sel[(len(sel)-1)]
    sel.remove( src_obj )
    for m in sel:
        pm.select( clear=True )
        pm.select( src_obj )
        pm.select( sel[c], tgl=True )
        pm.transferAttributes( transferPositions=0,
                               transferNormals=0,
                               transferUVs=2,
                               transferColors=0,
                               sampleSpace=5,
                               sourceUvSpace='map1',
                               targetUvSpace='map1',
                               searchMethod=3,
                               flipUVs=0,
                               colorBorders=1 )
        c+=1
    if pm.confirmDialog( m='Delete history on these?', 
                        title='Delete history?', 
                        button=['Yes', 'No'], 
                        defaultButton='Yes', 
                        cancelButton='No' ):
        for m in sel:
            pm.delete( pm.PyNode(m), ch=True )
    pm.select( sel )
    pm.select( src_obj, tgl=True )
    pm.warning( "Copied UVs from " + str(src_obj.name()) + " to " + str(len(sel)) + " meshes." )

#function to export a uv snapshot to the open file's folder
def snapshot_uvs( res, *args ):
    fformat = 'png'
    sel = pm.ls( selection=True )[0]
    scene_path = pm.system.sceneName().dirname()
    file_out = str(scene_path) + "/" + str(sel) + "." + str(fformat)
    pm.uvSnapshot( n=file_out, 
                   xr=res, 
                   yr=res, 
                   r=0, 
                   g=0, 
                   b=0, 
                   ff=fformat, 
                   o=True )
    pm.warning( 'Here is where your UVs went: ' + str(pm.mel.toNativePath(file_out)) )

#UI

if 'uvWizWin' in locals():
    pm.deleteUI( uvWizWin )
uvWizWin = pm.window( title=",.·'`·.,.·UVs·.,.·`'·.,", iconName='UV_WIZ', widthHeight=(100, 68), s=False, tlb=True )
pm.columnLayout( adjustableColumn=True )
xfer_btn = pm.button( l="C O P Y   U V s", h=45, bgc=[0,0.38,0.52], c=transfer_uvs, ann='Select target meshes first, then source mesh.' )
pm.separator( st='in', h=5 )
snap_btn = pm.button( l="S N A P S H O T", h=45, bgc=[0.52,0,0], c=lambda *args: snapshot_uvs( pm.intField(res_int, query=True, v=True) ) )
pm.rowLayout( nc=2 )
pm.text( l="Resolution: ", align='right', fn='smallPlainLabelFont' )
res_int = pm.intField( v=1024, w=50 )
pm.setParent( '..' )
pm.setParent( '..' )
pm.showWindow( uvWizWin )
