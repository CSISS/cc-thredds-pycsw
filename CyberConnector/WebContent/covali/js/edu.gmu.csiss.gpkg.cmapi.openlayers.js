/**
* 
* OpenLayers Map Manager 
*
* Created by Ziheng Sun on 3/31/2016
* 
*/

edu.gmu.csiss.gpkg.cmapi.openlayers = {

	map: {},
	
	maplist: [],
	
	
	
	getMap: function(divid){
		
		var map = null;
		
		for(var i=0;i<this.maplist.length;i++){
			
			if(this.maplist[i].getTarget() == divid){
				
				map = this.maplist[i];
				
				break;
				
			}
			
		}
		
		return map;
		
	},
	
	addMap: function(map){
		
		this.maplist.push(map);
		
	},
	
	init: function(divid){
		this.loadMap(divid);
	},
	
	resize: function(){
		this.map.updateSize();
	},
	
	centerBounds: function(bounds){
		//call openlayers api to center bounds
		//.....
		
		//trigger event
		edu.gmu.csiss.gpkg.cmapi.openlayers.event.triggerEvent("map.view.center.bounds", bounds);
	},

	centerFeature: function(feature){
		//call openlayers api to center feature
		//.....
		
		//trigger event
		edu.gmu.csiss.gpkg.cmapi.openlayers.event.triggerEvent("map.view.center.feature", feature);
	},

	centerOverlay: function(overlay){
		//call openlayers api to center overlay
		//.....
		
		//trigger event
		edu.gmu.csiss.gpkg.cmapi.openlayers.event.triggerEvent("map.view.center.overlay", overlay);
	},
	
	/**
	* Test it. Some problems here.
	**/
	getOverlayById: function(overlayId){
		//simply return the layer with Id the same as input
		var layers = this.map.getLayers();
		var thel = null;
		for(var i=0;i<layers.getLength();i++){
			var l = layers.item(i); //this function should work
			if(overlayId == l.overlayId){
				thel = l;
				break;
			}
		}
		return thel;
	},
	
	loadMap: function(divid){
	
		// Declare a Tile layer with an OSM source
        var osmLayer = new ol.layer.Tile({
          source: new ol.source.OSM(),
          name: "osm-basemap"
        });
        // Create latitude and longitude and convert them to default projection
//        var birmingham = ol.proj.transform([-1.81185, 52.44314], 'EPSG:4326', 'EPSG:3857');
        var usCenter = ol.proj.transform([-95.067385, 36.380028], 'EPSG:4326', 'EPSG:3857');
        // Create a View, set it center and zoom level
        var view = new ol.View({
//          center: birmingham,
          center: usCenter,
          zoom: 4
        });
        // Instanciate a Map, set the object target to the map DOM id
        this.map = new ol.Map({
          target: divid,
          controls: []
        });
//        this.map.removeControl();
        
        // Add the created layer to the Map
        this.map.addLayer(osmLayer);
        // Set the view for the map
        this.map.setView(view);
        // Add map to the map list
        this.addMap(this.map);
		
	},
	
	/***********************************************************************************/
	/**add these methods for overlay channels**/
	/***********************************************************************************/
	hideOveraly: function(message){
		var onelayer = this.getOverlayById(message.overlayId);
		onelayer.setVisible(false);
	},
	
	showOverlay: function(message){
		var onelayer = this.getOverlayById(message.overlayId);
		onelayer.setVisible(true);
	},
	
	createOverlay: function(message){
		/**
		 * default the content of geopackage is vector. The raster tiles are not taken into consideration here. 
		 * annotated by Ziheng Sun on 6/2/2016
		 */
		var newoverlay = new ol.layer.Vector({
			
			overlayId: message.overlayId,
			
			overlayName : message.name
			
		});
		this.addLayer(newoverlay); //if want get the overlay, use the OpenLayers API method: map.getLayer
	},
	
	removeOverlay: function(message){
		var onelayer = this.getOverlayById(message.overlayId);
		this.map.removeLayer(onelayer);
	},
	
	//update the name or parent id of the overlay
	updateOverlay: function(message){
		var onelayer = this.getOverlayById(message.overlayId);
		onelayer.name = message.name;
		onelyaer.parentId = message.parentId;
	}
	
}