{
    #target aftereffects

    var selected = app.project.selection;

    // CONSTANTS
    // sRGB -> rec709 clamps & adjustments
    var lo_clamp = 0.0627;
    var hi_clamp = 0.92156862745;
    var gamma = 1.0;
    // Output Module template name
    var om_name = "K2_rec709";
    // Output Module template .AEP project
    om_source = new ImportOptions (File("\\\\cagenas.bst.espn.pvt\\Workspace\\TEMPLATES\\AE_rec709\\outputModuleImport.aep"));
    
    // CONTAINERS
    // footage attribute placeholders
    var xres = 0;          // x-resolution
    var yres = 0;          // y-resolution
    var dur = 0;           // duration
    var par = 1.0;         // pixel aspect ratio
    var frate = 59.97;     // frame rate


    // Checks for the existence of an output module template on a render queue item
    function checkOutputModule(RQitem, module_name)
    {
        var exists = false;
        
        for (i=1; i < RQitem.outputModules[1].templates.length; i++)
        {
            if (RQitem.outputModules[1].templates[i] == module_name)
            {
                exists = true;
            }
        }   
        return exists;
    }


    // Creates an output module template from a master .aep file
    function createOutputModule(om_source, module_name)
    {
        om_template = app.project.importFile(om_source);
        temp_RQitem = app.project.renderQueue.item(app.project.renderQueue.numItems);
        temp_RQitem.outputModules[1].saveAsTemplate(module_name);
        om_template.remove();
    }


    // Sets an output module template on all render queue items
    function setOutputModule(module_name)
    {
        RQitems = app.project.renderQueue.items;
        for (i=1; i<=RQitems.length; i++)
        {
            RQitem = RQitems[i];
            RQitem.outputModules[1].applyTemplate(module_name);
            
            mov_name = RQitem.comp.name.split('.')[0] + "_rec709";
            path = RQitem.comp.layer(1).source.file.path.toString() + "//";
            RQitem.outputModules[1].file = new File(path + mov_name);
            
        }
    }
    
    // clamps the output values of a layer using a Levels effect
    function setClamp(layer, channels)
    {
        if (typeof(channels) === 'undefined') channels = "alpha";
        
        if (channels === "alpha")
        {
            //put a levels effect on the layer
            a_levels_effect = layer.property("Effects").addProperty("Levels"); 
            // set the values
            a_levels_effect.property("Channel:").setValue(5);    // enum value 5 sets the effect to only affect the alpha channel
            a_levels_effect.property("Output Black").setValue(lo_clamp);
            a_levels_effect.property("Output White").setValue(hi_clamp);
            a_levels_effect.property("Gamma").setValue(gamma);
        }
    
        if (channels === "rgb")
        {
            // add the levels adjustments to the layer
            rgb_levels_effect = layer.property("Effects").addProperty("Levels");
            // set the values
            rgb_levels_effect.property("Output Black").setValue(lo_clamp);
            rgb_levels_effect.property("Output White").setValue(hi_clamp);
            rgb_levels_effect.property("Gamma").setValue(gamma);    
        }
    }


    // MAIN SCRIPT BODY
    // confirm that something is selected
    if (selected === "")
    {
        alert("Nothing selected.  Please select one or more footage files.");
    }

    // iterate over the selected items, 
        // check that each item is valid,
        // make a comp matching its attributes, 
        // add a levels adjustment to clamp the alpha, 
        // add it to the render queue, 
        // set the output module
        // set the output name
        
    for (i=0; i < selected.length; i++)
    {
        // confirm that the selected objects are footage
        if (selected[i].typeName != "Footage")
        {
            alert("Item " + selected[i].name + " is not footage.  Skipping...");
            continue;
        }
    
        // populate footage attributes
        xres = selected[i].width;
        yres = selected[i].height;
        dur = selected[i].duration;
        par = selected[i].pixelAspect;
        frate = selected[i].frameRate;
        
        
        // confirm that frame rate is 59.94
        //if (frate !== 59.94)
        //{
        //    conf_dialog = confirm("Frame rate of " + selected[i].name + " is not 59.94.\nHit 'Yes' to make the output comp 59.94.\nHit 'No' to skip.", false, "(>'-')> Frame rate override? <('-'<)");
        //    if (conf_dialog) frate = 59.94;
        //    else continue;
        //}
        
        // create the comp and add the footage as a layer
        output_comp = app.project.items.addComp(selected[i].name, xres, yres, par, dur, frate);
        footage_layer = output_comp.layers.add(selected[i]);
        
        // clamp the output to 16-235
        setClamp(footage_layer);
        setClamp(footage_layer, "rgb");

        // add the comp to the queue
        queue_item = app.project.renderQueue.items.add(output_comp);

        
    } // end of loop
    
    // Check the first item in the RQ to see if the selected output module template is available
    if (!checkOutputModule(app.project.renderQueue.item(1), om_name))
    {
        // if not, create it by importing the output module source template .AEP file
        createOutputModule(om_source, om_name);
    }
    
    // set the output module for all RQ items created by this script
    setOutputModule(om_name);
    
}