package edu.gmu.csiss;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.XPath;
import org.dom4j.io.SAXReader;

/**
*Class Sweeper.java
*@author Ziheng Sun
*@time Jun 12, 2017 2:42:40 PM
*Original aim is to support CyberConnector.
*/
public class Sweeper {

	String cswurl, lastupdatetime;
	
	
	private Sweeper (){
		
	}
	
	public Sweeper(String cswurl, String lastupdatetime){
		
		this.cswurl = cswurl;
		
		this.lastupdatetime = lastupdatetime;
		
	}
	
	/**
	 * Search CSW
	 * @param lastupdatetime
	 * @return
	 */
	public static String searchCSW(String cswurl, String lastupdatetime, String spos, String maxrec){
		
		int datenum = Integer.parseInt(lastupdatetime);
		
//		int twoweeksago = datenum-14;
		
		String datestr = String.valueOf(datenum);
		
		datestr = datestr.substring(0,4) + "-" + datestr.substring(4,6) + "-" + datestr.substring(6);
		
		String req = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> "+
		"	<GetRecords "+
		"	    xmlns=\"http://www.opengis.net/cat/csw/2.0.2\" "+
		"	    xmlns:ogc=\"http://www.opengis.net/ogc\" "+
		"	    xmlns:gml=\"http://www.opengis.net/gml\" "+
		"	    xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" "+
		"	    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd\" service=\"CSW\" version=\"2.0.2\" resultType=\"results\" outputFormat=\"application/xml\" outputSchema=\"http://www.isotc211.org/2005/gmd\" startPosition=\""+spos+"\" maxRecords=\""+maxrec+"\"> "+
		"	    <Query typeNames=\"gmd:MD_Metadata\">"+
		"	        <ElementSetName>brief</ElementSetName>"+
		"	        <Constraint version=\"1.1.0\">"+
		"	            <ogc:Filter>"+
		"	                <ogc:And>"+
		"	                    <ogc:PropertyIsLessThanOrEqualTo>"+
		"	                        <ogc:PropertyName>apiso:TempExtent_end</ogc:PropertyName>"+
		"	                        <ogc:Literal>"+datestr+"</ogc:Literal>"+
		"	                    </ogc:PropertyIsLessThanOrEqualTo>"+
		"	                    <ogc:BBOX>"+
		"	                        <ogc:PropertyName>ows:BoundingBox</ogc:PropertyName>"+
		"	                        <gml:Envelope>"+
		"	                            <gml:lowerCorner>-90 -180</gml:lowerCorner>"+
		"	                            <gml:upperCorner>90 180</gml:upperCorner>"+
		"	                        </gml:Envelope>"+
		"	                    </ogc:BBOX>"+
		"	                </ogc:And>"+
		"	            </ogc:Filter>"+
		"	        </Constraint>"+
		"	    </Query>"+
		"	</GetRecords>";
		
		String resp = Register.sendPost(cswurl, req);
		
//		System.out.println(resp);
		
		return resp;
		
	}
	
	public static Document parseXMLStr(String xml){
		
		SAXReader reader = new SAXReader();
		
		Document document = null;
		
		try {
			
			InputStream stream = new ByteArrayInputStream(xml.trim().getBytes("UTF-8"));
			
			document = reader.read(stream);
			
		} catch (Exception e) {
			
			e.printStackTrace();
			
		}
		
	    return document;
	}
	
	public void run(){
		
		int startpos = 1;
		
		int num = 0;
		
		while(true){
			
			String resp = Sweeper.searchCSW(cswurl, lastupdatetime, String.valueOf(startpos), "1000");
			
			//parse the results
			
			Document document= Sweeper.parseXMLStr(resp);

			Map<String, String> map = new HashMap<String, String>();
			
			map.put("csw", "http://www.opengis.net/cat/csw/2.0.2");
			
			map.put("gmd", "http://www.isotc211.org/2005/gmd");
			
			map.put("gml", "http://www.opengis.net/gml");
			
			map.put("gmi", "http://www.isotc211.org/2005/gmi");
			
			map.put("gco", "http://www.isotc211.org/2005/gco");
			
			map.put("srv", "http://www.isotc211.org/2005/srv");
			
			
			
			XPath xpath = DocumentHelper.createXPath("//csw:GetRecordsResponse/csw:SearchResults/gmd:MD_Metadata"); //list all the records
			
			//for gmd
			XPath accessoptions = DocumentHelper.createXPath("gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine");
			
			XPath accesslink = DocumentHelper.createXPath("gmd:CI_OnlineResource/gmd:linkage/gmd:URL");
			
			XPath accessinfo = DocumentHelper.createXPath("gmd:CI_OnlineResource/gmd:name/gco:CharacterString");
			
			XPath identifierpath = DocumentHelper.createXPath("gmd:fileIdentifier/gco:CharacterString"); 
			
			xpath.setNamespaceURIs(map);
			
			List list = xpath.selectNodes(document);
			
			Iterator it = list.iterator();
			
			int offset = 0;
			
			while(it.hasNext()){
				
				Element ele = (Element)it.next();
				
				String identifier = identifierpath.selectSingleNode(ele).getText();
				
				//check its online resource URL. 
				
				List onlinenodes = accessoptions.selectNodes(ele);
				
				for(int i=0, len =onlinenodes.size() ; i<len; i++){
					
					String acsname = accessinfo.selectSingleNode(onlinenodes.get(i)).getText();
					
					if(acsname.toUpperCase().contains("HTTP")){
						
						String acslink =  accesslink.selectSingleNode(onlinenodes.get(i)).getText();
						
//						System.out.println(acslink);
						
						if(!Sweeper.isValid(acslink)){
							
							System.out.println("Remove dataset " + identifier);
							
							String rmreq = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> "+
							"<csw:Transaction xmlns:csw=\"http://www.opengis.net/cat/csw/2.0.2\" service=\"CSW\" "+
					 "                version=\"2.0.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "+
					 "                xmlns:gco=\"http://www.isotc211.org/2005/gco\" "+
					 "                xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" "+
					 "                xmlns:gmi=\"http://www.isotc211.org/2005/gmi\" "+
					 "                xmlns:srv=\"http://www.isotc211.org/2005/srv\" "+
					 "	              xmlns:ogc=\"http://www.opengis.net/ogc\" "+
					 "                xmlns:gmx=\"http://www.isotc211.org/2005/gmx\" "+
					 "                xmlns:gsr=\"http://www.isotc211.org/2005/gsr\" "+
					 "                xmlns:gss=\"http://www.isotc211.org/2005/gss\" "+
					 "                xmlns:gts=\"http://www.isotc211.org/2005/gts\" "+
					 "                xmlns:gml=\"http://www.opengis.net/gml/3.2\" "+
					 "                xmlns:xlink=\"http://www.w3.org/1999/xlink\" "+
					 "                xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" "+
					 " 				  xmlns:apiso=\"http://www.opengis.net/cat/csw/apiso/1.0\" "+
					 "                xsi:schemaLocation=\"http://www.isotc211.org/2005/gmi http://www.ngdc.noaa.gov/metadata/published/xsd/schema.xsd\"> "+
							"  <csw:Delete> "+
							"    <csw:Constraint version=\"1.1.0\"> "+
							"      <ogc:Filter> "+
							"        <ogc:PropertyIsEqualTo> "+
							"          <ogc:PropertyName>apiso:Identifier</ogc:PropertyName> "+
							"          <ogc:Literal>"+identifier+"</ogc:Literal> "+
							"        </ogc:PropertyIsEqualTo> "+
							"      </ogc:Filter> "+
							"    </csw:Constraint> "+
							"  </csw:Delete> "+
							"</csw:Transaction>";
							
							Register.sendPost(cswurl, rmreq);
							
							num++;
							
							offset++;
							
						}
						
						break;
						
					}
					
				}
				
			}
			
			
			XPath nextrecordpath = DocumentHelper.createXPath("//csw:GetRecordsResponse/csw:SearchResults/@nextRecord");
			
			int nextrecordindex = ((Double)nextrecordpath.numberValueOf(document)).intValue();
			
			XPath numberOfRecordsMatchedPath = DocumentHelper.createXPath("//csw:GetRecordsResponse/csw:SearchResults/@numberOfRecordsMatched");
			
			int numberOfRecordsMatched = ((Double)numberOfRecordsMatchedPath.numberValueOf(document)).intValue();
			
			XPath numberOfRecordsReturnedPath = DocumentHelper.createXPath("//csw:GetRecordsResponse/csw:SearchResults/@numberOfRecordsReturned");
			
			int numberOfRecordsReturned = ((Double)numberOfRecordsReturnedPath.numberValueOf(document)).intValue();
			
//			System.out.println("NextRecord:" + nextrecordindex + "\nNumber of Records Matched :" + numberOfRecordsMatched + "\nNumber of Records Returned : " + numberOfRecordsReturned);
			
			if((nextrecordindex+numberOfRecordsReturned)>=numberOfRecordsMatched){
				
				break;
				
			}else{
				
//				System.out.println("Current location: " + startpos);

				startpos = nextrecordindex - offset;
				
			}
			
		}
		
		System.out.println("Totally removed " + num + " records.");
		
		
	}
	/**
	 * Check if a URL is valid (return 404 if not)
	 * @param url
	 * @return
	 */
	public static boolean isValid(String url){
		
		boolean isvalid = false;
		
		try {
			
			URL u = new URL(url);
			
			HttpURLConnection huc = (HttpURLConnection) u.openConnection();
			
			huc.setRequestMethod("HEAD");
			
			int responseCode = huc.getResponseCode();

			if (responseCode != 404) {
			
				isvalid = true;
			
			} else {
			
				isvalid = false;
			
			}
			
		} catch (Exception e) {

			e.printStackTrace();
			
		}
		
		
		
		return isvalid;
		
	}
	
	public static void main(String[] args) {
		
//		Sweeper.searchCSW("http://cube.csiss.gmu.edu/srv/csw", "20170611", "1", "100");
		Sweeper sweeper = new Sweeper("http://cube.csiss.gmu.edu/srv/csw", "20170611");
		sweeper.run();
		
//		System.out.println(Sweeper.isValid("http://thredds.ucar.edu/thredds/fileServer/station/soundings/PROFILER_20170516_0000.bufr"));
		
	}

}
