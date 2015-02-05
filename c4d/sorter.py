import c4d
from c4d import gui

rd = doc.GetActiveRenderData()
mpass = rd.GetFirstMultipass()



def generateNameSwapLists():
    """ Generates two corresponding lists, one of the user multipass names, the other of the 
        default system multipass names.
        Returns: ([str], [str])."""

    def __getMpassNames(mpass):
        """ Gets both names of a multipass: the name the user chose, and the default system name.
            Returns: (str,str) """
        user_name = mpass.GetName()
        full_str = mpass.__str__()
        sys_name = full_str.split('called ')[1].split('/')[1].split('\'')[0]
        return user_name, sys_name
        
    user_names, sys_names = []

    while(True):
        names = __getMpassNames(mpass)
        user_names.append(names[0])
        sys_names.append(names[1])
        next = mpass.GetNext()
        if mpass.__eq__(next):
            break
        else:
            mpass = next_mpass

    return user_names, sys_names


# Get the output paths and file names of the render

# Prepare two lists:
	# 1- The current (default) names of output multipasses
	# 2- The new (desired) names of output multipasses

# Run sorting algorithm on those folders
    # While sorting, check for the old names, and rename them to the new names.
