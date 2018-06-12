/**
 * Menu listeners
 * @author Ziheng Sun
 * @date 2018.05.31
 */
edu.gmu.csiss.covali.menulistener = {
		
		init: function(){
			
			$("#upload").click(this.upload);
			
			$("#tools").click(this.tools);
			
			$("#settings").click(this.settings);
			
			$("#search").click(this.search);
			
		},
		
		search: function(){
			
			BootstrapDialog.show({
	            message: 'Hi Apple!',
	            cssClass: 'dialog-vertical-center',
	            buttons: [{
	                icon: 'glyphicon glyphicon-ban-circle',
	                label: 'Confirm',
	                title: 'Mouse over Button 3',
	                cssClass: 'btn-warning'
	            }, {
	                label: 'Close',
	                action: function(dialogItself){
	                    dialogItself.close();
	                }
	            }]
	        });
			
		},
		
		upload: function(){
			
			BootstrapDialog.show({
	            message: 'Hi Apple!',
	            cssClass: 'dialog-vertical-center',
	            buttons: [{
	                icon: 'glyphicon glyphicon-ban-circle',
	                label: 'Confirm',
	                title: 'Mouse over Button 3',
	                cssClass: 'btn-warning'
	            }, {
	                label: 'Close',
	                action: function(dialogItself){
	                    dialogItself.close();
	                }
	            }]
	        });
			
			
		},
		
		tools: function(){
			
			BootstrapDialog.show({
	            message: 'Hi Apple!',
	            cssClass: 'dialog-vertical-center',
	            buttons: [{
	                label: 'Button 1',
	                title: 'Mouse over Button 1'
	            }, {
	                label: 'Button 2',
	                // no title as it is optional
	                cssClass: 'btn-primary',
	                data: {
	                    js: 'btn-confirm',
	                    'user-id': '3'
	                },
	                action: function(){
	                    alert('Hi Orange!');
	                }
	            }, {
	                icon: 'glyphicon glyphicon-ban-circle',
	                label: 'Button 3',
	                title: 'Mouse over Button 3',
	                cssClass: 'btn-warning'
	            }, {
	                label: 'Close',
	                action: function(dialogItself){
	                    dialogItself.close();
	                }
	            }]
	        });
			
		},
		
		checkLayer: function(side, layername, checked){
			
			var olmap = edu.gmu.csiss.covali.map.getMapBySide(side);
			
//			var checked = this.checked;
			
			olmap.getLayers().forEach(function (layer) {
			    
				if (layer.get('name') == layername) {
			    	
					layer.setVisible(checked);
					
			    }
				
			});
			
		},
		/**
		 * Get layer control of either left or right side
		 */
		getLayerControl: function(side){
			
			var id = "treeview-checkable-"+side;
        
        	$tree = $("<div id=\""+id+"\"></div>");
        	
        	var olmap = edu.gmu.csiss.covali.map.getMapBySide(side);
        	
        	olmap.getLayers().forEach(function(layer,idx){
        		
        		$tree.append("<div class=\"checkbox\">"+
        				"<label><input type=\"checkbox\" checked=\"checked\" onchange=\"edu.gmu.csiss.covali.menulistener.checkLayer('"+
        				side+"', '"+layer.get("name")+"', this.checked)\" value=\"\">"+layer.get("name")+"</label>"+
        				"</div>");
        		
        	});
        	
        	
        	return $tree;
        	
		},
		
		settings: function(){
			
			BootstrapDialog.show({
				
				cssClass: 'dialog-vertical-center',
	            
	            title: "Settings",
	            
	            message: function(dialog) {
	            	
	            	
	            	var $lefttree = edu.gmu.csiss.covali.menulistener.getLayerControl("left");
	            	
	            	var $righttree = edu.gmu.csiss.covali.menulistener.getLayerControl("right");
	                
	            	
	                var $content = $('<div class=\"row\">'+
	    			
					'<div class=\"col-md-12\"><h2>Layer Control</h2></div>'+
					
					'<div class=\"col-md-6\" id=\"left-settings\">'+
					
					'	<h4>Left Map</h4>'+
					
					$lefttree.html()+
					
					'</div>' +
				
					'<div class=\"col-md-6\" id=\"right-settings\" >'+
					
					'	<h4>Right Map</h4>'+
					
					$righttree.html()+
					
					'</div>');
	                
	                return $content;
	            },
	            
	            buttons: [{
	                
	            	icon: 'glyphicon glyphicon-circle',
	                
	                label: 'OK',
	                
	                title: 'OK',
	                
	                cssClass: 'btn-warning',
	                
	                action: function(dialogItself){
	                	
	                	dialogItself.close();
	                	
	                }
	                
	            }, {
	                
	            	label: 'Close',
	                
	                action: function(dialogItself){
	                	
	                    dialogItself.close();
	                    
	                }
	            }]
	        });
			
			
			
		}
		
}