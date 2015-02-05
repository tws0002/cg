{
    
    function RenderToConsoleSingle()
    {
    
    	var scriptName = "Render to Console (Single Proc)";
		var safeToRunScript = true;
		
		safeToRunScript = (app.project != null);
		if (!app.project) 
        {
			alert ("A project must be open to use this script.", scriptName);
		}
    
		if (safeToRunScript) 
            {
			// Check the render queue and make certain at least one item is queued.
			safeToRunScript = false;
			for (i = 1; i <= app.project.renderQueue.numItems; ++i) {
				if (app.project.renderQueue.item(i).status == RQItemStatus.QUEUED) {
					safeToRunScript = true;
					break;
				}
			}
			if (!safeToRunScript) 
             {
				alert("You do not have any items set to render.", scriptName);
			}
		}
		
		if (safeToRunScript) 
        {
			// Check if we are allowed to access the network.
			var securitySetting = app.preferences.getPrefAsLong("Main Pref Section", "Pref_SCRIPTING_FILE_NETWORK_SECURITY");
			if (securitySetting != 1) 
             {
				alert ("This script requires the scripting security preference to be set.\n" +
					"Go to the \"General\" panel of your application preferences,\n" +
					"and make sure that \"Allow Scripts to Write Files and Access Network\" is checked.", scriptName);
				safeToRunScript = false;
			}
		}
         
         if (safeToRunScript)
         {
             var batString = "cmd /k aerender -project ";
             var curProj = app.project.file.toString();
             var batFile = new File("~/aeTempRenderCmd.bat");
                
             batString += curProj;
                
             batFile.open("w");
             batFile.write(batString);
             batFile.close();
             batFile.execute();
        }
    
    }
    RenderToConsoleSingle();
}