/**
 * @author Ziheng Sun
 * @date 2018.06.01
 */

edu.gmu.csiss.covali.map = {
		
		getMapBySide: function(side){
			
			var id = "";
			
			if(side=="left"){
				
				id = "openlayers1";
				
			}else if(side=="right"){
				
				id = "openlayers2";
				
			}
			
			return edu.gmu.csiss.gpkg.cmapi.openlayers.getMap(id);
			
		}
		
}