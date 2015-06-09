var proj = app.project;
var itemTotal = proj.numItems;
var itemAry = new Array();
var curItem, curComp, totalComps, totalLayers, curLayer, curLayerIndex, textDocument;
var fontsUsed = new Array();

// Gets a list of all fonts used in the project
function getFontsUsed(){
    // Iterate over the project window, looking for all comps
    for (var i = 1; i<= itemTotal; i++){
        curItem = proj.item(i);
        if (curItem instanceof CompItem){
            itemAry[itemAry.length]=curItem;
            }
        }
    totalComps = itemAry.length;

    // Iterate over all comps
    for (var c = 0; c < totalComps; c++){
        curComp = itemAry[c];
        totalLayers = itemAry[c].numLayers;
        
        // Iterate over all layers
        for (var l=1; l<=totalLayers; l++){
            curLayer = curComp.layer(l);
            curLayerIndex = curLayer.index;
            
            // If we land on a text layer
            if (curLayer instanceof TextLayer){
                // Get the TextDocument
                textDocument = curLayer.property("Source Text").value
                // .. and add its font to the list
                fontsUsed.push(textDocument.font);
                }
            }
        }
    return fontsUsed;
    }

// Switches every instance of a given font with a different font
function switchFont(oldFont, newFont){
    for (var i = 1; i<= itemTotal; i++){
        curItem = proj.item(i);
        if (curItem instanceof CompItem){
            itemAry[itemAry.length]=curItem;
            }
        }

    totalComps = itemAry.length;

    for (var c = 0; c < totalComps; c++){
        curComp = itemAry[c];
        totalLayers = itemAry[c].numLayers;
        
        for (var l=1; l<=totalLayers; l++){
            curLayer = curComp.layer(l);
            curLayerIndex = curLayer.index;
            
            if (curLayer instanceof TextLayer){
                textDocument = curLayer.property("Source Text").value
                if (textDocument.font == oldFont){
                    textDocument.font = newFont;
                    curLayer.property("Source Text").setValue(textDocument);
                    }
                }
            }
        }
    }

// Gets a list of all fonts installed on the system.
function getFonts(){

    var list = new Array(); // a list

    // loop thru the fonts and add their info in a list
    for (var i = 0; i < app.fonts.length;i++){
            list.push("app.fonts.item("+ String(i) +") --> " +app.fonts[i].name);
        }  // end loop

    }

