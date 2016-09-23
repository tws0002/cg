{
    // CONTAINERS
    var comp = null;
    var padding_sec = 0;
    // INPUT
    var selected = app.project.selection;
    dlg = prompt("# of frames to pad", "1", "Add Padding to Comp");
    padding = dlg;

    // MAIN SCRIPT BODY
    // confirm that something is selected
    if (selected === "")
    {
        alert("Nothing selected.  Please select one or more comps.");
    }

    for (i=0; i<selected.length; i++)
    {
        // confirm that the selected objects are footage
        if (selected[i].typeName != "Composition")
        {
            alert("Item " + selected[i].name + " is not a comp.  Skipping...");
            continue;
        }
        var padding_sec = (padding / selected[i].frameRate); 

        selected[i].duration += (padding_sec*2);
        layers = selected[i].layers;
        
        for (j=1; j<=layers.length; j++)
        {
            layers[j].startTime = padding_sec;
        }
       
    } // end of loop
  
}
/*
{
    var selected = app.project.selection;
    var new_prefix = "NBA_E_";

    // MAIN SCRIPT BODY
    // confirm that something is selected
    if (selected === "")
    {
        alert("Nothing selected.  Please select one or more comps.");
    }

    for (i=0; i<selected.length; i++)
    {
        selected[i].name = new_prefix + selected[i].name;
    } // end of loop
  
}*/