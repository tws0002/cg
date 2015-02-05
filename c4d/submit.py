# Simple script for doing a Find/Replace over all selected object names.
 
import c4d
from c4d import gui
 
# Unique id numbers for each of the GUI elements
LBL_JOB_NAME =      1000
LBL_SCENE_FILE =    1001
LBL_RENDER_PATH =   1002
LBL_FRAME_RANGE =   1003
LBL_NUM_THREADS =   1004
LBL_PRIORITY =      1005
LBL_CLUSTER =       1006
LBL_RESTRICTIONS =  1007
LBL_ALL_THREADS =   1008

GROUP_MAIN =        9999

TXT_JOB_NAME =      10001
TXT_SCENE_FILE =    10002
TXT_RENDER_PATH =   10003
TXT_FRAME_RANGE =   10004

GROUP_NUM_THREADS = 10005 
TXT_NUM_THREADS =   10007
BOOL_ALL_THREADS =  10006

TXT_PRIORITY =      10008
TXT_CLUSTER =       10009
TXT_RESTRICTIONS =  10010

GROUP_BUTTONS =     20000
BTN_SUBMIT =        20001
BTN_CANCEL =        20002
 
# Dialog for renaming objects
class OptionsDialog(gui.GeDialog):
  def CreateLayout(self):
    self.SetTitle('Submit Scene to Qube')

    self.GroupBegin(GROUP_MAIN, c4d.BFH_LEFT, 2, 1)

    # Job name field
    self.AddStaticText(LBL_JOB_NAME, c4d.BFH_LEFT, name='Job Name') 
    self.AddEditText(TXT_JOB_NAME, c4d.BFH_LEFT, 600)
    self.SetString(TXT_JOB_NAME, 'Job Name')
    
    # Job scene path field
    self.AddStaticText(LBL_SCENE_FILE, c4d.BFH_LEFT, name='Scene File') 
    self.AddEditText(TXT_SCENE_FILE, c4d.BFH_LEFT, 600)
    self.SetString(TXT_SCENE_FILE, 'Scene File')
    
    # Job render path field
    self.AddStaticText(LBL_RENDER_PATH, c4d.BFH_LEFT, name='Render Path') 
    self.AddEditText(TXT_RENDER_PATH, c4d.BFH_LEFT, 600)
    self.SetString(TXT_RENDER_PATH, 'Render path')

    # Frame range field
    self.AddStaticText(LBL_FRAME_RANGE, c4d.BFH_LEFT, name='Frame Range') 
    self.AddEditText(TXT_FRAME_RANGE, c4d.BFH_LEFT, 100)
    self.SetString(TXT_FRAME_RANGE, '1-200')

    # Num Threads field
    self.AddStaticText(LBL_NUM_THREADS, c4d.BFH_LEFT, name='Num. Threads') 

    self.GroupBegin(GROUP_NUM_THREADS, c4d.BFH_LEFT, 2, 1)
    self.AddEditText(TXT_NUM_THREADS, c4d.BFH_LEFT, 60)
    self.SetString(TXT_NUM_THREADS, '16')
    self.AddCheckbox(BOOL_ALL_THREADS, c4d.BFH_RIGHT, 0, 0, name='All')
    
    self.Enable(TXT_NUM_THREADS, 0)
    self.SetBool(BOOL_ALL_THREADS, 1)

    self.GroupEnd()

    # Priority field
    self.AddStaticText(LBL_PRIORITY, c4d.BFH_LEFT, name='Priority') 
    self.AddEditText(TXT_PRIORITY, c4d.BFH_LEFT, 100)
    self.SetString(TXT_PRIORITY, '9999')

    # Cluster field
    self.AddStaticText(LBL_CLUSTER, c4d.BFH_LEFT, name='Cluster') 
    self.AddEditText(TXT_CLUSTER, c4d.BFH_LEFT, 100)
    self.SetString(TXT_CLUSTER, '/')

    # Restrictions field
    self.AddStaticText(LBL_RESTRICTIONS, c4d.BFH_LEFT, name='Restrictions') 
    self.AddEditText(TXT_RESTRICTIONS, c4d.BFH_LEFT, 100)
    self.SetString(TXT_RESTRICTIONS, '')
    
    self.GroupEnd()

    # Buttons field
    self.GroupBegin(GROUP_BUTTONS, c4d.BFH_RIGHT, 2, 1)
    self.AddButton(BTN_SUBMIT, c4d.BFH_SCALE, name='Submit to Farm')
    self.AddButton(BTN_CANCEL, c4d.BFH_SCALE, name='Cancel')
    self.GroupEnd()
    
    self.ok = False
    return True
 
  # React to user's input:
  def Command(self, id, msg):
    if id == BOOL_ALL_THREADS:
      i = self.GetBool(BOOL_ALL_THREADS)
      self.Enable(TXT_NUM_THREADS, (1-i))
    elif id==BTN_CANCEL:
      self.Close()
    elif id==BTN_SUBMIT:
      self.ok = True
      #self.option_find_string = self.GetString(TXT_FIND)
      #self.option_replace_string = self.GetString(TXT_REPLACE)
      self.Close()
    return True
 
#This is where the action happens
def main():
  # Get the selected objects, including children.
  selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
 
  if len(selection) <= 0:
    gui.MessageDialog('Must select objects!')
    return
 
  # Open the options dialogue to let users choose their options.
  dlg = OptionsDialog()
  dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
  if not dlg.ok:
    return
 
  doc.StartUndo()  # Start undo block.
  num_renamed = 0
  for i in range(0,len(selection)):
    sel = selection[i]
    new_name = sel.GetName().replace(
        dlg.option_find_string, dlg.option_replace_string, 1)
    if (sel.GetName() != new_name):
      # NOTE: to see print output open: menubar > Script > Console window.
      print ' - ' + sel.GetName() + ' > ' + new_name
      doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, sel)
      sel.SetName(new_name)
      num_renamed += 1
  doc.EndUndo()   # End undo block.
  c4d.EventAdd()  # Update C4D to see changes.
  gui.MessageDialog(str(num_renamed) + ' of ' + str(len(selection)) +
                    ' objects renamed')
 
if __name__=='__main__':
  main()