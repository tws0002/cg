import pymel.core as pm
import shutil
import os


''' Path definitions, specific to project structure '''
def getShotVersion():
    
    project_root = pm.workspace(q=True, rd=True)
    
    split_path = pm.system.sceneName().splitext()[0].split('/')
    
    '''if split_path[0] != 'X:':
        pm.error('Your scene is not mapped to the X: drive. '
            'Please reopen it and try again.')'''
    
    # Declaring output var
    paths = {}   
       
    # Extracting shot from the file path
    shot_str = split_path[6]
    # Extracting filename from the file path
    file_str = split_path[8]
    # Extracting version from the file name
    version_str = file_str.split('_')[2]
    # Versioned output directory
    paths['version_dir'] = project_root + shot_str + '/PLAYBLAST/' + version_str + '/'    
    # (Output 1) Full path of versioned file output, minus file extension
    paths['version_file'] = paths['version_dir'] + shot_str + '_anim_' + version_str
    
    # Prepping copy folders for 'current' version
    # (Output 2) Setting up 'current' folder
    paths['copy_dir'] = project_root + shot_str + '/PLAYBLAST/CURRENT/'
    # Removing version from the file name
    master_file_str = file_str.rstrip('_' + version_str) + '.avi'
    # (Output 3) 'Current' version of the file is the above two lines added together
    paths['copy_file'] = paths['copy_dir'] + master_file_str
    
    return paths

    
''' Playblast configuration '''  
def blastIt( paths, mode='copy', *args ):
    pm.mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')

    fr_start = pm.playbackOptions(
        q=True,
        min=True,
        )
    fr_end = pm.playbackOptions(
        q=True,
        max=True,
        )

    
    pm.playblast(
        startTime = fr_start,
        endTime = fr_end,
        filename = paths['version_file'],
        forceOverwrite = False,
        format = 'avi',
        viewer = True,
        widthHeight = (960,540),
        p=100,
        orn = True,
        c = 'none',
        qlt = 100
        )
        
    pm.mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')

    if mode == 'copy':
        if not os.path.exists( paths['copy_dir'] ):
            os.makedirs( paths['copy_dir'] )
        shutil.copy( paths['version_file'] + '.avi', paths['copy_file'] )
    
    if mode == 'nocopy':
        pm.warning('Because you made an alt version of your playblast, no copy was sent to the /CURRENT/ folder.')
    
    pm.warning('Here is where your file went: ' + paths['version_file'].replace('/', '\\') + '.avi')
    

def run( *args ):
    
    ''' Execute '''   
    paths = getShotVersion()

    # Dealing with existing playblasts 
    if os.path.exists( paths['version_file'] + '.avi' ):
        pm.warning('Existing playblast detected!')
        
        chk = pm.confirmDialog( 
            title='Confirm', 
            message='Overwrite existing playblast?', 
            button=['Ok','Rename Output', 'Cancel'], 
            defaultButton='Ok', 
            cancelButton='Cancel', 
            dismissString='Cancel' 
            )
            
        if chk == 'Ok':
            blastIt( paths )
            
        elif chk == 'Rename Output':
            version_increment = len( os.listdir( paths['version_dir'] ) )
            paths['version_file'] += '_alt_0' + str(version_increment)
            blastIt( paths, mode='nocopy' )
        
        elif chk == 'Cancel':
            pass
            
    else: blastIt( paths )
