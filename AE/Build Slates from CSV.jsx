{
    #target aftereffects

    //var TEST_CSV     = "Y:/Workspace/SCRIPTS/AE/assets/MNF_Deliverables.csv";
    var ASSET_FOLDER = "Y:/Workspace/SCRIPTS/AE/assets/";

    var SLATE_COMP   = "SLATE_COMP";

    var FRAMERATE    = 59.94;
    var PADDING      = 3 / FRAMERATE;

    var FONT         = "Helvetica";
    var FONT_SIZE    = 33;
    var FONT_TRACKING= 11;
    

	////  BUILDERS      ////////////////////////////////////////////////////////////////////////////
    function buildSlates(){
    /*  Runs buildSlatedComp() on all selected items in the project window and adds them to the render 
    	queue.  Includes basic pre-flight checks. */

        // Get user selection from project window
        var selected = app.project.selection;
        // Exit out if nothing is selected.
        if (selected === ""){
            alert("Nothing selected.  Please select one or more footage files.");
        }

        // Build or get an existing slate BG comp
        var slate_comp = buildSlate();

        var csv = getCsv();

        // ITERATE OVER SELECTED PROJECT ITEMS
        for (i=0; i<selected.length; i++){

            // Skip non-footage elements
            if (selected[i].typeName != "Footage"){
                alert("Item " + selected[i].name + " is not footage. Skipping ... ");
                continue;
            }

            var rgb_out = buildSlatedComp(selected[i], slate_comp, csv, false);
            var mat_out = buildSlatedComp(selected[i], slate_comp, csv, true);

            app.project.renderQueue.items.add(rgb_out);
            app.project.renderQueue.items.add(mat_out);

        }
    }

    function getCsv(){
        var csv_file = File.openDialog('Select a CSV file', '*.csv', false);
        return csv_file
    }

	function buildSlatedComp(quicktime, slate_comp, csv, matte){
	/*  This is the primary workhorse function.  Given a quicktime, a database entry, and a flag
		for creating a separate matte output, this function will create a slated version of that
		quicktime. */

        // Gather data about footage
        xres  = quicktime.width;
        yres  = quicktime.height;
        dur   = quicktime.duration;
        frate = quicktime.frameRate;
        name  = quicktime.name.replace('.mov','');

        // Make an output comp
        slated_comp   = app.project.items.addComp((quicktime.name.replace('.mov','')), 1920, 1080, 1.0, dur + PADDING, FRAMERATE);
        // Add the footage to the comp
        element_layer = slated_comp.layers.add(quicktime);
        // Offset the footage by the padding amount
        element_layer.startTime = PADDING;

        // Add the slate background to the comp
        slate_layer = slated_comp.layers.add(slate_comp);

        ///// POPULATE TEXT LAYERS /////
        // Find the deliverable in the database
        slate_info = getDeliverable(quicktime.name, csv);

        // production name, contact name, deliverable array
        prod_text        = slate_info[0];
        contact_text     = slate_info[1];
        csv_row          = slate_info[2];
        // parse deliverable array
        date_text        = csv_row[6];
        deliverable_text = csv_row[1];
        filename_text    = csv_row[2];
        notes_text       = csv_row[5];

        if (matte == true){
            shift_channels = element_layer.property("Effects").addProperty("Shift Channels");
            shift_channels.property("Take Alpha From").setValue(9);
            shift_channels.property("Take Red From").setValue(1);
            shift_channels.property("Take Green From").setValue(1);
            shift_channels.property("Take Blue From").setValue(1);
            slated_comp.name = slated_comp.name + "_ALPHA";
            deliverable_text = deliverable_text + "_ALPHA";
            filename_array = filename_text.split("");
            filename_array.splice(3, 0, "a");
            filename_text = filename_array.join("");
        } else {}

         // Convert information into our preferred units where needed
        // Duration to proper timecode
        dur = Math.round(dur * FRAMERATE);
        dur = frameToTimecode(dur, FRAMERATE);
        // Audio yes/no
        if ((element_layer.hasAudio == true) && (matte == false)){
            audio = 'Yes';
        }    else {
            audio = 'No';
        }

        // Make Text layers (with placeholder data)
        date_layer        = buildTextLayer(date_text, 173, slated_comp, slate_layer)
        production_layer  = buildTextLayer(prod_text, 271, slated_comp, slate_layer)
        deliverable_layer = buildTextLayer(deliverable_text, 364, slated_comp, slate_layer)
        filename_layer    = buildTextLayer(filename_text, 459, slated_comp, slate_layer)
        runtime_layer     = buildTextLayer(dur, 555, slated_comp, slate_layer)
        audio_layer       = buildTextLayer(audio, 653, slated_comp, slate_layer)
        notes_layer       = buildTextLayer(notes_text, 748, slated_comp, slate_layer)
        //contact_layer     = buildTextLayer(contact_text, 743, slated_comp, slate_layer)

        // Add EVS code to front of comp name
        slated_comp.name = filename_text + '___' + slated_comp.name;

        // Scale & position adjustments for 720p elements
        if (xres == 1280){
            slated_comp.width = 1280;
            slated_comp.height = 720;

            slate_layer.scale.setValue([66.666, 66.666]);
            slate_layer.position.setValue([640, 360]);
            element_layer.position.setValue([640, 360]);
        }

        return slated_comp;
    }

    function buildSlate(){
    /*  Creates a comp to use as a background for slates. */
    	var exists = getItemByName(SLATE_COMP);

    	if (exists != -1){
    		return exists;
    	}

        var xres         = 1920;
        var yres         = 1080;
        var par          = 1.0;

        slate_comp = app.project.items.addComp(SLATE_COMP, xres, yres, par, PADDING, FRAMERATE.toString());
        slate_back = app.project.importFile(new ImportOptions(File(ASSET_FOLDER + "SLATE_BG.png")));

        slate_folder = app.project.items.addFolder('SLATE');
        slate_comp.parentFolder = slate_folder;
        slate_back.parentFolder = slate_folder;

        slate_layer = slate_comp.layers.add(slate_back);
        slate_layer.outPoint = 1 / FRAMERATE;

        return slate_comp;
    }

    function buildTextLayer(text, ypos, comp, parent){
    /*  A shortcut helper function for creating text layers for slates. */

    	// Create text layer
        var text_layer = comp.layers.addText(text);
        // Create text document (AE's "formatting" object)      
        var text_properties = text_layer.property("ADBE Text Properties").property("ADBE Text Document");
        var text_document = text_properties.value;
        
        text_document.fontSize = FONT_SIZE;
        text_document.font     = FONT;
        text_document.tracking = FONT_TRACKING;

        // Assign the formatting to the layer
        text_properties.setValue(text_document);

        // set the position for the text
        text_layer.position.setValue([726, ypos, 0])
        // assign it to a parent for scaling
        text_layer.parent = parent;
        // make it 1 frame long
        text_layer.outPoint = 1 / FRAMERATE;

        return text_layer;
    }


    ////  GETTERS       ////////////////////////////////////////////////////////////////////////////
    function getDeliverable(quicktime, csv){
    /*  A fetch function for finding a quicktime in a deliverables database. */

        var deliverables = csvToArray(csv);

        var production = deliverables[1][0];
        var contact    = deliverables[1][1];

        for (var i=0; i<deliverables.length; i++){
            if (deliverables[i][1] + '.mov' == quicktime){
                found_deliverable = deliverables[i];
                break;
            } else {
                found_deliverable = -1;
            }
        }
        return [production, contact, found_deliverable];
    }

    function getItemByName(name_){
    /*  A fetch function for finding an AVItem in an AE project window. */

        var items_ = app.project.items;
        var found = false;

        for (i=1; i<items_.length+1; i++){
            if (items_[i].name === name_){
            	found = items_[i];
            } 
        }
        if (!found) {
        	return -1;
        } else {
        	return found;
        }
    }


    ////  CONVERTERS    ////////////////////////////////////////////////////////////////////////////    
    function csvToArray(csv){
    /*  Converts a csv file to a 2D array.  */

        var csv_array = [];
        var csv_stream = new File(csv);

        // CSV read block
        csv_stream.open('r');
        while(!csv_stream.eof){
            csv_array[csv_array.length] = csv_stream.readln();
        }
        // CSV close
        csv_stream.close();

        for (var i=0; i<csv_array.length; i++){
            csv_array[i] = csv_array[i].split(",");
        }

        return csv_array;
    }

    function frameToTimecode(framenumber, framerate){
    /* Converts a frame number to timecode (string).  Works for 24, 25, 30, 23.98, 29.97, and 59.94
       Code borrowed from David Heidelberger
       http://www.davidheidelberger.com/blog/?p=29  */

        var d = 0;
        var m = 0;

        var dropFrames = Math.round(framerate * 0.066666);
        var framesPerHour = Math.round(framerate * 60 * 60);
        var framesPer24Hours = framesPerHour * 24;
        var framesPer10Minutes = Math.round(framerate * 60 * 10);
        var framesPerMinute = (Math.round(framerate) * 60) - dropFrames;

        if (framenumber<0){
            framenumber = framesPer24Hours + framenumber;
        }

        framenumber = framenumber % framesPer24Hours;

        d = Math.floor(framenumber / framesPer10Minutes);
        m = framenumber % framesPer10Minutes;

        if (m > dropFrames){
            framenumber = framenumber + (dropFrames * 9 * d) + dropFrames * Math.floor((m - dropFrames) / framesPerMinute);
        }

        else{
            framenumber = framenumber + dropframes * 9 * d;
        }

        var frRound = Math.round(framerate);
        var frames = framenumber % frRound;
        var seconds = Math.floor(framenumber / frRound) % 60;
        var minutes = Math.floor(Math.floor(framenumber / frRound) / 60) % 60;
        var hours = Math.floor(Math.floor(Math.floor(framenumber / frRound) / 60) / 60);

        // modify frame padding
        var frames = String("00" + frames).slice(-2);
        var seconds = String("00" + seconds).slice(-2);
        var minutes = String("00" + minutes).slice(-2);
        var hours = String("00" + hours).slice(-2);

        var timecode = hours + ':' + minutes + ':' + seconds + ':' + frames;

        return timecode;
    }

    // Run!
    buildSlates();
}