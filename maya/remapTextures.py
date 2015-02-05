import pymel.core as pm
textures = pm.ls(typ='file')

for tex in textures:
    file_name = tex.fileTextureName.get()
    if 'W:/' in file_name:
        tex.fileTextureName.set(file_name.replace('W:/', '\\\\cagenas\\'))
    elif 'Y:/' in file_name:
        tex.fileTextureName.set(file_name.replace('Y:/', '\\\\cagenas\\'))