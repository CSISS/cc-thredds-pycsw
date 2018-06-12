/**
 * Projection Selector Control
 * @author Ziheng Sun
 * @date 05/31/2018
 */

edu.gmu.csiss.covali.projection = {
		
	extent: null,
	
	leftmap: null,
	
	rightmap: null,
		
	init: function(){
		
		edu.gmu.csiss.covali.projection.leftmap = edu.gmu.csiss.gpkg.cmapi.openlayers.getMap("openlayers1");
		
		edu.gmu.csiss.covali.projection.rightmap = edu.gmu.csiss.gpkg.cmapi.openlayers.getMap("openlayers2");
		
		$("#projectionselector").change(function() {
			
			var option = $( "#projectionselector option:selected" ).val();
			
			if(option!="3D"){
				
				edu.gmu.csiss.covali.projection.search(option);
				
			}else{
				
				edu.gmu.csiss.covali.projection.enable3D();
				
			}
			 
//			edu.gmu.csiss.covali.projection.setProjection(option, null, null, null, edu.gmu.csiss.covali.projection.leftmap);
//			
//			edu.gmu.csiss.covali.projection.setProjection(option, null, null, null, edu.gmu.csiss.covali.projection.rightmap);
			
		});
		
	},
	
	enable3D: function(){
		
		
	},
	
	search: function (query) {
//        resultSpan.innerHTML = 'Searching ...';
        
		fetch('http://epsg.io/?format=json&q=' + query).then(function(response) {
         
			return response.json();
        
		}).then(function(json) {
         
			var results = json['results'];
          
			if (results && results.length > 0) {
            
				for (var i = 0, ii = results.length; i < ii; i++) {
              
					var result = results[i];
              
					if (result) {
                
						var code = result['code'], name = result['name'],
						
						proj4def = result['proj4'], bbox = result['bbox'];
						
						if (code && code.length > 0 
								&& proj4def && proj4def.length > 0 
								&&bbox && bbox.length == 4) {
                  
							edu.gmu.csiss.covali.projection.setProjection(code, name, proj4def, bbox);
                  
							return;
                
						}
					}
				}
          }
          
			edu.gmu.csiss.covali.projection.setProjection(null, null, null, null);
		  
        });
		
    },
	
	setProjection: function (code, name, proj4def, bbox) {
        
		if (code === null || name === null || proj4def === null || bbox === null) {
		
//          resultSpan.innerHTML = 'Nothing usable found, using EPSG:3857...';
          
			var defaultview = new ol.View({
	            
	        	  projection: 'EPSG:3857',
	            
	        	  center: [0, 0],
	          
	        	  zoom: 1
	          
	          });
			
			edu.gmu.csiss.covali.projection.leftmap.setView(defaultview);
        	
			edu.gmu.csiss.covali.projection.rightmap.setView(defaultview);
        
        	return;
        
        }

//        resultSpan.innerHTML = '(' + code + ') ' + name;

		var newProjCode = 'EPSG:' + code;
        
		proj4.defs(newProjCode, proj4def);
        
        var newProj = ol.proj.get(newProjCode);
        
        var fromLonLat = ol.proj.getTransform('EPSG:4326', newProj);

        // very approximate calculation of projection extent
        var extent = ol.extent.applyTransform(
            [bbox[1], bbox[2], bbox[3], bbox[0]], fromLonLat);
        
        newProj.setExtent(extent);
        
        var newView = new ol.View({
        
        	projection: newProj
        
        });
        
        edu.gmu.csiss.covali.projection.leftmap.setView(newView);
        
        edu.gmu.csiss.covali.projection.rightmap.setView(newView);
        
        var size = edu.gmu.csiss.covali.projection.leftmap.getSize();
        
        if (size) {
        
        	newView.fit(extent, size);
        
        }
        
      }
		
};
