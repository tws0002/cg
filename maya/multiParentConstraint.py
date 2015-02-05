import pymel.core as pm

### parent constraint tool
def multiParentConstraint( mo=True, *args ):
    sel = pm.ls(sl=True)
    
    p = sel[len(sel)-1] #last item in the list is the parent
    
    for obj in sel:
        if obj == p: #if the object is the target
            continue #skip it
        else:
            const = pm.parentConstraint( p, obj, mo=mo ) #parent constrain command
    
    pm.select(sel)


### UI
try: pm.deleteUI('mpcwin')
except: pass
mpcwin = pm.window('mpcwin', title='Multiple pConstraint:', width=75, tlb=True, rtf=True)
col = pm.verticalLayout(width=75)
but = pm.button(
    'but', 
    l='Parent Constrain', 
    c=lambda *args: multiParentConstraint( mo=pm.checkBox('cbox', q=True, v=True) ) 
    )
cbox = pm.checkBox('cbox', l='Maintain offset ')
col.redistribute(1,1)
pm.showWindow(mpcwin)