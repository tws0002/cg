{
    #target aftereffects

    // base path for wallpaper graphics
    //var ims_base_path = new Folder ("\\\\cagenas.bst.espn.pvt\\Workspace\\Show_Production\\SC14\\review\\team_wallpaper\\");
    var ims_base_path = new Folder ("\\c\\users\\rastermancer\\desktop\\team_wallpaper\\");

    // main dialog window
    var teamSelectWin = new Window ("dialog", "Pick a new team!");
    
    // dropdown elements for window
    var dd_league = teamSelectWin.add("dropdownlist");
    var dd_team = teamSelectWin.add("dropdownlist");
    dd_league.bounds = [0,0,128,20];
    dd_team.bounds = [0,0,128,20];
    
    // execute button for window
    var do_swap = teamSelectWin.add("button", [0,0,128,35], "Swap team");
    do_swap.name = "ok";
    do_swap.onClick = swapTeamGraphics;

    populateDropdown(dd_league, ims_base_path);
    dd_league.onChange = refresh;    
    teamSelectWin.show();


function swapTeamGraphics()
    {
        all_items = app.project.items;
        
        new_team = "none";
        new_league = "none";
        
        // get the new LEAGUE and TEAM selected from the UI
        e = "null is not an object"
        try
        {
            // new league, queried from UI            
            new_league = dd_league.selection.toString();  
            // new team name, queried from UI            
            new_team = dd_team.selection.toString();
        }
        catch(e) { alert("Please select a team"); }
        

        if (new_league !== "none" && new_team !== "none")
        {
            // the path to pull the new wallpapers from
            new_folder = Folder (ims_base_path.toString() + "\\" + new_league + "\\" + new_team + "\\");


            // do some magic to get the CITY from the selection
            // this may be a big assumption, but it works for now
            tmp_list = new_folder.getFiles()
            for (i=0; i<tmp_list.length; i++)
            {
                tmp_file = tmp_list[i].name.split("_");
                if (tmp_file.length < 5)  continue;
                // city name will be in the next-to-last spot in the file name
                else new_city = tmp_file[tmp_file.length-2]; 
            }


            // do the replacing:
            // iterate over every item in the project window
            for (i=1; i<=all_items.length; i++)
            {
                // get the current wallpaper .PNG file as a string and split it with an underscore
                file_name = all_items[i].name;
                file_name_split = file_name.split("_");
                
                // skip the file if it doesn't match the convention
                if (file_name_split.length < 5) continue;
            
                // swap the league, city, and team in the name of that file
                new_file = file_name_split;
                new_file[new_file.length-3] = new_league;
                new_file[new_file.length-2] = new_city;
                new_file[new_file.length-1] = new_team;            
                // rejoin the string
                new_file = unSplit(new_file, "_");
                
                // make the new wallpaper string into a full path
                new_path = new Folder( new_folder.toString() + "\\" + new_file + ".png");
                
                all_items[i].replace(new_path);
            }
        } 
        else{}
    }

    // utility to unsplit arrays that have been string.split()
    function unSplit( split_array, combine_char )
    {
        unsplit_string = "";
        for (j=0; j < split_array.length; j++)
        {
            if (j === 0) unsplit_string += split_array[j];
            else unsplit_string = unsplit_string + combine_char + split_array[j];
        }
        return unsplit_string;
    }

    // Builds a dropdown menu populated with folders in filesystem folders
    function populateDropdown ( dropdown, start_path )
    {
        var items = [];
        var items_full_path = start_path.getFiles();
        
        for (i = 0; i < items_full_path.length; i++)
        {
            var path_split = items_full_path[i].toString().split("/");
            if (path_split[path_split.length-1].indexOf(".") === -1)
            {
                items.push(path_split[path_split.length-1]);
                dropdown.add('item',items[items.length-1]);
            }
            else continue;
        }
    }
    
    // refreshes the Teams dropdown 
    function refresh()
    {
        var new_path = new Folder (ims_base_path.fullName + "\\" + dd_league.selection.toString() + "\\");
        dd_team.removeAll();
        populateDropdown(dd_team, new_path);
    }
}