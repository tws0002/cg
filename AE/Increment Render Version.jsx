{
    var selected = app.project.selection;
    for (i=0; i < selected.length; i++)
    {
        // confirm that the selected objects are footage
        if (selected[i].typeName != "Footage")
        {
            alert("Item " + selected[i].name + " is not footage.  Skipping...");
            continue;
        }
    
        var seq = selected[i].file;
        var path = seq.toString();
        var re = /v[0-9]+/;

        var version = re.exec(path)[0];
        version = version.replace('v', '');
        var padding = version.length;
        version = parseInt(version);
        
        var new_version = version + 1;
        var new_version = 'v' + pad(new_version, padding);
        writeLn(new_version);

        var newPath = path.replace(re, new_version);
        writeLn (newPath);
        var newFile = new File(newPath);
        
        try{
            selected[i].replace(newFile);
        } catch(err) {
            alert("No new version found for " + selected[i].name + " .");
        }

    } // end of loop

    function pad(n, width, z)
    {
        z = z || '0';
        n = n + '';
        return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
    }

}