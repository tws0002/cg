try: 
    wNode = nuke.selectedNode()
    wFile = wNode.knob('file').getValue()
    wxPos = wNode.xpos()
    wyPos = wNode.ypos()
    
    nRead = nuke.nodes.Read()
    nRead.knob('file').setValue(outFile)
    nRead.setXpos( wxPos )
    nRead.setYpos( wyPos + 50 )

except: 
    nuke.warning(' ')
