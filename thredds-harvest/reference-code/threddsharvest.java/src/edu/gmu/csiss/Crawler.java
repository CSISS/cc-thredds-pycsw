package edu.gmu.csiss;

import java.io.FileWriter;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.XPath;
import org.dom4j.io.SAXReader;

/**
*Class Crawler.java
*@author Ziheng Sun
*@time Jun 7, 2017 5:52:43 PM
*Original aim is to support CyberConnector.
*/
public class Crawler {
	
	String cachefilepath = null;
	
	String mode = null;
	
	String baseurl = null;
	
	String lastupdatetime = null;
	
	FileWriter out = null;
	
	private Crawler(){
		
	}
	
	public Crawler(String cachefile, String m, String lastut){		
		
		cachefilepath = cachefile;
		
		mode = m;
		
		lastupdatetime = lastut;
		
		 try {
			out = new FileWriter (cachefilepath, false);
		} catch (IOException e) {
			e.printStackTrace();
			throw new RuntimeException("Fail to open the cache index file.");
		}
		
	}
	
	public static Document parse(String url) 
    {
		
		URL myURL;
	       
        SAXReader reader = new SAXReader();
        Document document = null;
		try {

		    myURL = new URL(url);
			document = reader.read(myURL);
		} catch (Exception e) {
			System.err.println("Fail to open the URL: " + url);
			e.printStackTrace();
		}
        return document;
    }
	
	public static String getBaseURL(String url){
		
		URL u = null;
		String base = null;
		try {
			u = new URL(url);

			//String path = u.getFile().substring(0, u.getFile().lastIndexOf('/'));
			base = u.getProtocol() + "://" + u.getHost();
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
		
		return base;
		
	}
	
	public static String getRelativeBaseURL(String url){
		
		int lastin = url.lastIndexOf("/");
		
		String baseurl = url.substring(0, lastin);
		
		return baseurl;
		
	}
	/**
	 * Use regexpr
	 * @param in
	 * @return
	 */
	public static String extractDigits(String in) {
		   final Pattern p = Pattern.compile( "(\\d{8})" );
		   final Matcher m = p.matcher( in );
		   if ( m.find() ) {
		     return m.group( 0 );
		   }
		   return "";
    }
	
	public void leave(){
		
		try {
			out.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	/**
	 * Run to crawl the thredds catalog and save all the ISO metadata links to the index file
	 */
	public void run(String currentthreddsurl){
		System.out.println("Crawler#run url=" + currentthreddsurl);
		
//		long b = System.currentTimeMillis();
		
		if(baseurl == null){
			
			baseurl = Crawler.getBaseURL(currentthreddsurl);
			
			System.out.println("Base URL:" + baseurl);
		}
		
		if(mode.equals("update")&&lastupdatetime!=null){
			
			String currentdate =  Crawler.extractDigits(currentthreddsurl);
			
			if(currentdate!=null&&currentdate!=""){
				
				int difference = Integer.parseInt(currentdate) - Integer.parseInt(lastupdatetime);
				
				if(difference<=0){
					
//					System.out.println(">> The dataset is older than last update time. Going to be ignored...");
					
					return;
					
				}
				
			}
			
			
		}
		
		Document document= Crawler.parse(currentthreddsurl);
		
		if(document==null){
			return;
		}
		
		Map<String, String> map = new HashMap<String, String>();
		
		map.put("ts", "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0");
		
		map.put("xlink", "http://www.w3.org/1999/xlink");
		
		XPath xpath = DocumentHelper.createXPath("//ts:catalog//ts:dataset/ts:catalogRef"); //list all the subdataset
		
		xpath.setNamespaceURIs(map);
		
		List list = xpath.selectNodes(document);
		
		Iterator it = list.iterator();
		
		while (it.hasNext()) {  
		
			Element elt = (Element) it.next();  
			
			String subdatasetloc = elt.attributeValue("href");
			
			String subdataseturl = null;
			
			if(subdatasetloc.startsWith("/")){
				
				subdataseturl = baseurl + subdatasetloc;
				
			}else{
				
				subdataseturl = Crawler.getRelativeBaseURL(currentthreddsurl) + "/" + subdatasetloc;
				
			}
			
//			System.out.println("New Dataset URL: " + subdataseturl);
			
			run(subdataseturl); //crawl in
		    
		}
		
		//get the data ISO links
		
		XPath xpath2 = DocumentHelper.createXPath("//ts:catalog//ts:dataset"); //list all the subdataset
		
		XPath datepath = DocumentHelper.createXPath("ts:date"); //date
		
		XPath startpath = DocumentHelper.createXPath("ts:timeCoverage/ts:start"); //start
		
		XPath durationpath = DocumentHelper.createXPath("ts:timeCoverage/ts:duration"); //end
		
		xpath2.setNamespaceURIs(map);
		
		datepath.setNamespaceURIs(map);
		
		startpath.setNamespaceURIs(map);
		
		durationpath.setNamespaceURIs(map);
		
		List list2 = xpath2.selectNodes(document);
		
		try {
			
			it = list2.iterator();
			
			while (it.hasNext()) {  
				
				Element elt = (Element) it.next(); 
				
				//judge if the dataset is a file or a parent folder
				
				String datasetid = elt.attributeValue("ID");
				
				if(datasetid==null||datasetid.indexOf(".") == -1){
					
					//a folder
					continue;
					
				}
				
				StringBuffer line = new StringBuffer(currentthreddsurl.replace(".xml", ".html"));
				
				if(datepath.selectSingleNode(elt)!=null
							&&startpath.selectSingleNode(elt)!=null
							&&durationpath.selectSingleNode(elt)!=null){
					
					String moddate = datepath.selectSingleNode(elt).getText();
					
					String starttime = startpath.selectSingleNode(elt).getText();
					
					String duration = durationpath.selectSingleNode(elt).getText();
					
					line.append("?dataset=").append(datasetid)
							.append(" ").append(moddate)
							.append(" ").append(starttime)
							.append(" ").append(duration.replace(" ", "-"));
					
				}else{
					
					//a file - write the link to the index file
					
					//e.g. http://thredds.ucar.edu/thredds/catalog/nexrad/level3/PTA/YUX/20170608/catalog.html?dataset=NWS/NEXRAD3/PTA/YUX/20170608/Level3_YUX_PTA_20170608_1445.nids
					
//					String fileurl = baseurl + "/thredds/iso/" + dataurlpath;
					
					line.append("?dataset=").append(datasetid);
					
					
				}
				
				out.write(line + "\n");
			
			}
			
			
		} catch (Exception e) {
			
			e.printStackTrace();
			
		}
		
//		long e = System.currentTimeMillis();
		
//		System.out.println("Crawler takes " + (e-b ) + "ms");
		
		
	}
	
}
