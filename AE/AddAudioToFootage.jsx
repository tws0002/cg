{
    #target aftereffects

    var selected = app.project.selection;
    
    // CONTAINERS
    // footage attribute placeholders
    var xres = 0;          // x-resolution
    var yres = 0;          // y-resolution
    var dur = 0;           // duration
    var par = 1.0;         // pixel aspect ratio
    var frate = 0;     // frame rate

    // MAIN SCRIPT BODY
    // confirm that something is selected
    if (selected === "")
    {
        alert("Nothing selected.  Please select one or more footage files.");
    }

    var audio = selected[0]

    // iterate over the selected items, 
        // check that each item is valid,
        // make a comp matching its attributes, 
        // add a levels adjustment to clamp the alpha, 
        // add it to the render queue, 
        // set the output module
        // set the output name
        
    for (i=1; i < selected.length; i++)
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
        output_comp = app.project.items.addComp(selected[i].name.replace('.mov',''), xres, yres, par, dur, frate);
        footage_layer = output_comp.layers.add(selected[i]);
        footage_layer.audioEnabled = false;
        audio_layer = output_comp.layers.add(audio)
        
        // clamp the output to 16-235
        //setClamp(footage_layer);
        //setClamp(footage_layer, "rgb");

        // add the comp to the queue
        queue_item = app.project.renderQueue.items.add(output_comp);

        
    } // end of loop
    
  
}