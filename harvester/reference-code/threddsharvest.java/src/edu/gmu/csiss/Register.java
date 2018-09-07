package edu.gmu.csiss;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

import org.dom4j.Document;

import sun.net.www.protocol.http.HttpURLConnection;

/**
*Class Register.java
*@author Ziheng Sun
*@time Jun 7, 2017 5:58:56 PM
*Original aim is to support CyberConnector.
*/
public class Register {

	String cswurl = null;
	
	String indexfilepath = null;
	
	String baseurl = null;
	
	private  String basecatalogurl = null;
	
	private String basedatasetid = null;
	
	private String basedate = null;
	
	private String basestart = null;
	
	private String baseduration = null;
	
	private  String isocache = null;
	
	private StringBuffer cswreqcache = new StringBuffer();
	
	private int cacheCSWMd = 0;
	
	private int rounds = 0;
	
	private final int roundloads = 5; //two long will cause 413 response
	
	private boolean lastround = false;
	
	private String currentdatasetid = null;
	
	public Register(String cu, String ifp){
		
		cswurl = cu;
		
		indexfilepath = ifp;
		
	}
	/**
	 * Get string from url
	 * @param url
	 * @return
	 * @throws Exception
	 */
	public static String getURLText(String url) {
		 StringBuilder response = new StringBuilder();
		try {
			 URL website = new URL(url);
			URLConnection connection = website.openConnection();
	        BufferedReader in = new BufferedReader(
	                                new InputStreamReader(
	                                    connection.getInputStream()));
	        
	        String inputLine;

	        while ((inputLine = in.readLine()) != null) 
	            response.append(inputLine);

	        in.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
        return response.toString();
    }
	/**
	 * no round way
	 * @param isolink
	 */
	public void registerCSW(String isolink){
		
		String isometadata = Register.getURLText(isolink);
		
		if(isometadata==null){
			System.err.print("Can read string from the ISO link : " + isolink);
			return;
		}
		
		isometadata = isometadata.trim();
		
		isometadata = isometadata.substring("<?xml version=\"1.0\" encoding=\"UTF-8\"?>".length());
		
		isometadata = isometadata.replace("UCAR/UCP:East CONUS", this.currentdatasetid); //this is for http://thredds.ucar.edu/thredds/catalog/nexrad/composite/gini/catalog.html
		
		String insertreq = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> "+
				 " <csw:Transaction xmlns:csw=\"http://www.opengis.net/cat/csw/2.0.2\" service=\"CSW\" "+
				 "                version=\"2.0.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "+
				 "                xmlns:gco=\"http://www.isotc211.org/2005/gco\" "+
				 "                xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" "+
				 "                xmlns:gmi=\"http://www.isotc211.org/2005/gmi\" "+
				 "                xmlns:srv=\"http://www.isotc211.org/2005/srv\" "+
				 "                xmlns:gmx=\"http://www.isotc211.org/2005/gmx\" "+
				 "                xmlns:gsr=\"http://www.isotc211.org/2005/gsr\" "+
				 "                xmlns:gss=\"http://www.isotc211.org/2005/gss\" "+
				 "                xmlns:gts=\"http://www.isotc211.org/2005/gts\" "+
				 "                xmlns:gml=\"http://www.opengis.net/gml/3.2\" "+
				 "                xmlns:xlink=\"http://www.w3.org/1999/xlink\" "+
				 "                xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" "+
				 "                xsi:schemaLocation=\"http://www.isotc211.org/2005/gmi http://www.ngdc.noaa.gov/metadata/published/xsd/schema.xsd\"> "+
				 " 					<csw:Insert>" +
				 isometadata + 
				 "                  </csw:Insert>" +
				 " </csw:Transaction>";
						
		String resp = Register.sendPost(cswurl, insertreq);
		
		System.out.println(resp);
		
	}
	
	public void registerCSW(){
		
		if(this.cacheCSWMd>=this.roundloads || this.lastround){
			
//			System.out.println("Round "+this.rounds++);
			
			String insertreq = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> "+
					 " <csw:Transaction xmlns:csw=\"http://www.opengis.net/cat/csw/2.0.2\" service=\"CSW\" "+
					 "                version=\"2.0.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "+
					 "                xmlns:gco=\"http://www.isotc211.org/2005/gco\" "+
					 "                xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" "+
					 "                xmlns:gmi=\"http://www.isotc211.org/2005/gmi\" "+
					 "                xmlns:srv=\"http://www.isotc211.org/2005/srv\" "+
					 "                xmlns:gmx=\"http://www.isotc211.org/2005/gmx\" "+
					 "                xmlns:gsr=\"http://www.isotc211.org/2005/gsr\" "+
					 "                xmlns:gss=\"http://www.isotc211.org/2005/gss\" "+
					 "                xmlns:gts=\"http://www.isotc211.org/2005/gts\" "+
					 "                xmlns:gml=\"http://www.opengis.net/gml/3.2\" "+
					 "                xmlns:xlink=\"http://www.w3.org/1999/xlink\" "+
					 "                xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" "+
					 "                xsi:schemaLocation=\"http://www.isotc211.org/2005/gmi http://www.ngdc.noaa.gov/metadata/published/xsd/schema.xsd\"> "+
					 " 					<csw:Insert>" +
					 				this.cswreqcache + 
					 "                  </csw:Insert>" +
					 " </csw:Transaction>";
							
			Register.sendPost(cswurl, insertreq);
			
			this.cswreqcache = new StringBuffer();
			
			this.cacheCSWMd = 0;
			
		}
		
	}
	
	public void registerNewISO(String isolink){
		System.out.println("registerNewISO " + isolink);

		String isometadata = Register.getURLText(isolink);
		
		if(isometadata==null){
			System.err.print("Can read string from the ISO link : " + isolink);
			return;
		}
		
		isometadata = isometadata.trim();
		
		isometadata = isometadata.substring("<?xml version=\"1.0\" encoding=\"UTF-8\"?>".length());

		this.isocache = isometadata;
		
		this.cswreqcache.append(isometadata);
		
		this.cacheCSWMd++;
		
		this.registerCSW();
		
	}
	
	public void registerISO2CSW(String line){
		System.out.println("registerISO2CSW " + line);
		
		//extract ISO link from the data html page
		
//		String datahtml = Register.getURLText(htmllink);
//		
//		int index = datahtml.indexOf("<li> <b>ISO:</b> <a href='");
//		
//		if(index==-1){
//			
//			return;
//			
//		}
//		
//		datahtml = datahtml.substring(index+"<li> <b>ISO:</b> <a href='".length());
//		
//		String isolink = baseurl + datahtml.substring(0, datahtml.indexOf("'")).replace("&amp;", "&");
		
		String[] cols = line.split("\\ ");
		
		if(cols.length==1){
			
			//traditional method
			
			String isolink = this.turnHTML2ISOLINK(line);
			
			this.registerNewISO(isolink);
			
		}else{
			
			//time-saving method
			
			//new method: only download one iso for each folder.
			
			String currentcatalog= line.substring(0, line.indexOf("?"));
			
					
			if(baseurl == null){
				
				baseurl = Crawler.getBaseURL(cols[0]);
				
				System.out.println("Base URL:" + baseurl);
				
			}
			
			if(currentcatalog.equals(this.basecatalogurl)){
				
//				System.out.println("use existing iso");
				
				//create a ISO based on the cached template
				
				String newiso = createNewISOMetadata(cols[0], cols[1], cols[2], cols[3]);
				
//				System.out.println("New ISO:\n" + cols[0]);
				
				this.cswreqcache.append(newiso);
				
				this.cacheCSWMd++;
				
				this.registerCSW();
				
				
			}else{
				
//				System.out.println("create new iso");
				
//				long b = System.currentTimeMillis();
				
				//download a ISO file
				
				String isolink = this.turnHTML2ISOLINK(cols[0]);
				
//				System.out.println("ISO LINK : " + cols[0]);
				
				this.registerNewISO(isolink);
				
				this.basedatasetid = cols[0].split("\\=")[1];
				
				this.basedate = cols[1];
				
				this.basestart = cols[2];
				
				this.baseduration = cols[3];
				
				String basecaurl = cols[0].substring(0, cols[0].indexOf("?"));
				
				this.basecatalogurl=basecaurl;
				
//				long e = System.currentTimeMillis();
				
//				System.out.println("Read new iso from URL takes " + (e-b) + " ms.");
				
				System.out.println(basecaurl);
				
			}
			
		}
		
		
		System.exit(1);
	}
	
	/**
	 * Create a new ISO metadata based on a template to reduce the time cost
	 * @param date
	 * @param start
	 * @param duration
	 * @return
	 */
	public String createNewISOMetadata(String url, String date, String start, String duration){
		
		System.out.println("createNewISOMetadata " + url);
		//there are 14 differences between each pair
		
		String datasetid = url.split("\\?")[1].split("=")[1];
		
		String newiso = this.isocache.replaceAll(this.basedatasetid, datasetid)
								
								.replaceAll(this.basedate, date)
				
								.replaceAll(this.basestart, start);
		
		//find the old endposition
		
		String endpos = newiso.substring(newiso.indexOf("<gml:endPosition>")+"<gml:endPosition>".length());
		
		endpos = endpos.substring(0, endpos.indexOf("<"));
		
//		2017-06-13T21:24:00Z
		
		newiso = newiso.replaceAll(endpos, Register.addMins2Date(start, duration.substring(0, duration.indexOf("-"))));
		
		return newiso;
		
	}
	
	public static String addMins2Date(String start, String duration){
		
		int mins = Integer.parseInt(duration);
		
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		
		SimpleDateFormat sdf1 = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
		
		Date startdate = null;
		try {
			startdate = sdf.parse(start);
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		Calendar datems = Calendar.getInstance();
		
		datems.setTime(startdate);
		
		Date afterAddingMins=new Date(datems.getTimeInMillis() + mins*60000);
		
		return sdf1.format(afterAddingMins);
		
	}
	
	// HTTP POST request
	public static String sendPost(String url, String content) {

	
			StringBuffer response = new StringBuffer();
			try {
				URL obj = new URL(url);
				
				HttpURLConnection con = (HttpURLConnection) obj.openConnection();

				//add reuqest header
				con.setRequestMethod("POST");
				con.setRequestProperty("User-Agent", "Mozilla/5.0");
				con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

//				String urlParameters = "sn=C02G8416DRJM&cn=&locale=&caller=&num=12345";

				// Send post request
				con.setDoOutput(true);
				DataOutputStream wr = new DataOutputStream(con.getOutputStream());
				wr.writeBytes(content);
				wr.flush();
				wr.close();

				int responseCode = con.getResponseCode();
//				System.out.println("\nSending 'POST' request to URL : " + url);
//				System.out.println("Post parameters : " + content);
//				System.out.println("Response Code : " + responseCode);

				BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
				String inputLine;

				while ((inputLine = in.readLine()) != null) {
					response.append(inputLine);
				}
				in.close();
			} catch (Exception e) {
				
				e.printStackTrace();
			}
			

			//print result
//			System.out.println(response.toString());
			
			return response.toString();

		}
	
	public String turnHTML2ISOLINK(String htmlurl){
		
//		http://thredds.ucar.edu/thredds/catalog/nexrad/level3/PTA/YUX/20170608/catalog.html?dataset=NWS/NEXRAD3/PTA/YUX/20170608/Level3_YUX_PTA_20170608_1445.nids
		
//		http://thredds.ucar.edu/thredds/iso/nexrad/level3/PTA/YUX/20170613/Level3_YUX_PTA_20170613_1452.nids?catalog=http%3A%2F%2Fthredds.ucar.edu%2Fthredds%2Fcatalog%2Fnexrad%2Flevel3%2FPTA%2FYUX%2F20170613%2Fcatalog.html&dataset=NWS%2FNEXRAD3%2FPTA%2FYUX%2F20170613%2FLevel3_YUX_PTA_20170613_1452.nids
		
//		http://thredds.ucar.edu/thredds/iso/nexrad/level3/PTA/YUX/20170608/Level3_YUX_PTA_20170608_1445.nids?catalog=http://thredds.ucar.edu/thredds/catalog/nexrad/level3/PTA/YUX/20170608/catalog.html&dataset=dataset=NWS/NEXRAD3/PTA/YUX/20170608/Level3_YUX_PTA_20170608_1445.nids
		
		
		String isolink = null;
		try {

			String[] preval = htmlurl.split("\\?");
			
			String[] dataset = preval[1].split("\\=");
			
			String datasetpath = dataset[1];
			
			this.currentdatasetid = datasetpath;
			
			String filename = dataset[1].substring(dataset[1].lastIndexOf("/"));
			
			String isobase = preval[0].replace("catalog", "iso");
			
			isobase = isobase.substring(0, isobase.lastIndexOf("/")) + filename;
			
			isolink = isobase+ "?catalog="  + java.net.URLEncoder.encode( preval[0] , "UTF-8") + "&dataset=" + java.net.URLEncoder.encode( datasetpath, "UTF-8");
			
		} catch (UnsupportedEncodingException e) {
			
			e.printStackTrace();
			
		};
		
		return isolink;
		
	}
	
	public void run(){
		
		//read index file path
		
		try {
			
			FileInputStream inputStream = null;
			Scanner sc = null;
			try {
			    inputStream = new FileInputStream(indexfilepath);
			    
			    sc = new Scanner(inputStream, "UTF-8");
			    
			    while (sc.hasNextLine()) {
			        
			    	String line = sc.nextLine();
//			        System.out.println(line);
			        try{
			        	 this.registerISO2CSW(line);
			         }catch(Exception e){
			        	 e.printStackTrace();
			         }
			        
			    }
			    //last round
			    this.lastround = true;
			    this.registerCSW();
			    // note that Scanner suppresses exceptions
			    if (sc.ioException() != null) {
			        throw sc.ioException();
			    }
			} finally {
			    if (inputStream != null) {
			        inputStream.close();
			    }
			    if (sc != null) {
			        sc.close();
			    }
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public static void main(String[] args){
		
		//test registration
		
//		Register reg = new Register("http://cube.csiss.gmu.edu/srv/csw", "init");
//		
////		reg.registerISO2CSW("http://thredds.ucar.edu/thredds/iso/nexrad/level3/PTA/YUX/20170608/Level3_YUX_PTA_20170608_1445.nids");
//		
//		long startTime = System.currentTimeMillis();
//		
//		for(int i=0;i<50;i++){
//			
//			reg.registerISO2CSW("http://thredds.ucar.edu/thredds/catalog/nexrad/level3/PTA/YUX/20170608/catalog.html?dataset=NWS/NEXRAD3/PTA/YUX/20170608/Level3_YUX_PTA_20170608_1445.nids");
//			
//		}
//		
//		
//		long endTime = System.currentTimeMillis();
//		
//		System.out.println("The duration is:" + (endTime-startTime) + " ms");
		
//		String iso = reg.turnHTML2ISOLINK("http://thredds.ucar.edu/thredds/catalog/nexrad/level3/PTA/YUX/20170608/catalog.html?dataset=NWS/NEXRAD3/PTA/YUX/20170608/Level3_YUX_PTA_20170608_1445.nids");
		
//		System.out.println(iso);
		
//		System.out.println(Register.addMins2Date("2017-06-13T21:24:00", "2"));

		String x = "UCAR/UCP:East CONUS sdfdsfdsfds";
		
		System.out.println(x.replaceAll("UCAR/UCP:East CONUS", "y"));
		
	}
	
}
