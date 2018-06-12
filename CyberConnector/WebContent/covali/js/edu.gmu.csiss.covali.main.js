/**
 * Main file of COVALI
 * @author Ziheng Sun
 * @date 2018.05.29
 */
edu.gmu.csiss.covali.main = {
	
	init: function(){
		
		this.initheight();
		
		edu.gmu.csiss.gpkg.cmapi.openlayers.init("openlayers1");
		
		edu.gmu.csiss.gpkg.cmapi.openlayers.init("openlayers2");
		
		edu.gmu.csiss.gpkg.cmapi.initialize.init();
		
//		this.addTestWMS();
		
		edu.gmu.csiss.covali.projection.init();
		
		edu.gmu.csiss.covali.menulistener.init();
		
	},
	
	addTestWMS: function(){
		
		var leftmap = edu.gmu.csiss.gpkg.cmapi.openlayers.getMap("openlayers1");
		
		var rightmap = edu.gmu.csiss.gpkg.cmapi.openlayers.getMap("openlayers2");
		
		var myLayer1303 = new ol.layer.Tile({
			  //extent: [2033814, 6414547, 2037302, 6420952],
			  //preload: Infinity,
			  visible: true,
			  source: new ol.source.TileWMS(({
//				  LAYERS=IR&ELEVATION=0&TIME=2018-05-31T02%3A00%3A19.000Z&TRANSPARENT=true&STYLES=boxfill%2Frainbow&COLORSCALERANGE=-50%2C50&NUMCOLORBANDS=20&LOGSCALE=false&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT=image%2Fpng&SRS=EPSG%3A4326&BBOX=-101.47971029369,19.92840558883,-85.775652352431,35.632463530092&WIDTH=256&HEIGHT=256
			    url: 'http://thredds.ucar.edu/thredds/wms/grib/NCEP/GEFS/Global_1p0deg_Ensemble/members-analysis/GEFS_Global_1p0deg_Ensemble_ana_20180520_0600.grib2',
			    params: {'LAYERS': 'Convective_available_potential_energy_pressure_difference_layer_ens', 
			    	'TILED': true, 'VERSION': '1.3.0',
			    	'STYLES':'boxfill/Frainbow'}
			    }))
		});
		leftmap.addLayer(myLayer1303);
		var myLayer1304 = new ol.layer.Tile({
			  //extent: [2033814, 6414547, 2037302, 6420952],
			  //preload: Infinity,
			  visible: true,
			  source: new ol.source.TileWMS(({
//				  LAYERS=IR&ELEVATION=0&TIME=2018-05-31T02%3A00%3A19.000Z&TRANSPARENT=true&STYLES=boxfill%2Frainbow&COLORSCALERANGE=-50%2C50&NUMCOLORBANDS=20&LOGSCALE=false&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT=image%2Fpng&SRS=EPSG%3A4326&BBOX=-101.47971029369,19.92840558883,-85.775652352431,35.632463530092&WIDTH=256&HEIGHT=256
			    url: 'http://thredds.ucar.edu/thredds/wms/grib/NCEP/GEFS/Global_1p0deg_Ensemble/members-analysis/GEFS_Global_1p0deg_Ensemble_ana_20180520_0600.grib2',
			    params: {'LAYERS': 'Convective_inhibition_pressure_difference_layer_ens', 
			    	'TILED': true, 'VERSION': '1.3.0',
			    	'STYLES':'boxfill/Frainbow'}
			    }))
		});
		rightmap.addLayer(myLayer1304);
		
	},
	
	initheight: function(){
		
		edu.gmu.csiss.covali.main.htmlbodyHeightUpdate()
		
		$( window ).resize(function() {
		
			edu.gmu.csiss.covali.main.htmlbodyHeightUpdate()
		
		});
		
		$( window ).scroll(function() {
		
			height2 = $('.main').height()
			
			edu.gmu.csiss.covali.main.htmlbodyHeightUpdate()
		
		});
		
		
	},
	
	htmlbodyHeightUpdate: function (){
		
		var height3 = $( window ).height()
		
		var height1 = $('.nav').height()+50
		
		height2 = $('.main').height()
		
		if(height2 > height3){
		
			$('html').height(Math.max(height1,height3,height2)+10);
			
			$('body').height(Math.max(height1,height3,height2)+10);
		
		}
		else
		{
		
			$('html').height(Math.max(height1,height3,height2));
			
			$('body').height(Math.max(height1,height3,height2));
			
		}
		
	}
	
}

$(document).ready(function () {
	
	edu.gmu.csiss.covali.main.init();

});



