 {
    #include "core.jsx"

    function buildHomeAwayComps()
    {
        element = 'NBA_E_REG_MATCHUP_ROLLOUT_';
        footage_prefix = "08A_RegMatchRoll_";
        sides = ["HOME", "AWAY"];
        extra_element = "BARS";
        //matte_comps = ["Team_B", "Team_A"];
        matte_comps = ["4_LumaBottomTeam_Level2", "2_LumaTopTeam_Level2"]

        teams = [
            'ATL',
            'BKN',
            'BOS',
            'CHA',
            'CHI',
            'CLE',
            'DAL',
            'DEN',
            'DET',
            'GSW',
            'HOU',
            'IND',
            'LAC',
            'LAL',
            'MEM',
            'MIA',
            'MIL',
            'MIN',
            'NOLA',
            'NYK',
            'OKC',
            'ORL',
            'POR',
            'PHI',
            'PHX',
            'SAC',
            'SAS',
            'TOR',
            'UTAH',
            'WAS'
            ];

        sel_item = app.project.selection[0];
        xres  = 1920;
        yres  = 1080;
        par   = 1.0;
        dur   = sel_item.duration;
        frate = sel_item.frameRate;

        for (j=0; j<sides.length; j++){
            folder_item = getItem((sides[j] + "_TEAMS"), FolderItem);
            matte_comp = getItem(matte_comps[j], CompItem);
                
            for (i=0; i<teams.length; i++){
                comp_name = element + teams[i] + "_" + sides[j];
                output_comp = app.project.items.addComp(comp_name, xres, yres, par, dur, frate);

                footage = getItem(footage_prefix + teams[i] + ".mov", FootageItem);

                footage_layer = output_comp.layers.add(footage);
                matte_layer = output_comp.layers.add(matte_comp);
                if (extra_element !== ""){
                    extra_layer = getItem(extra_element + "_" + sides[j]);
                    output_comp.layers.add(extra_layer);
                }

                footage_layer.trackMatteType = TrackMatteType.LUMA;
                output_comp.parentFolder = folder_item;
            }
        }
    }
    buildHomeAwayComps();
}