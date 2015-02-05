import os
import sys

def psource( module, typ='py' ):

	if typ == 'py':
		pyfile = os.path.basename( module )
		pydir = os.path.dirname( module )

		toks = pyfile.split( '.' )
		modname = toks[0]

	elif typ == 'dir':
		pydir = os.path.dirname( module )

		toks = pydir.split( '/' )
		modname = toks[len(toks)-1]
		
		pydir = os.path.abspath(os.path.join(dir, os.pardir))
		
	# Check if directory is really a directory
	if( os.path.exists( pydir ) ):

		# Check if the file directory already exists in the sys.path list
		pathfound = 0
		for path in sys.path:
			if(pydir == path): pathfound = 1
		if not pathfound:
			sys.path.append( pydir )
		exec( 'import ' + modname ) in globals()
		exec( 'reload( ' + modname + ' )' ) in globals()

		return modname

