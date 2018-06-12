package edu.gmu.csiss.earthcube.cyberconnector.utils;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Properties;

/**
 *Class SysDir.java
 *@author ziheng
 *@time Aug 10, 2015 4:18:19 PM
 *Original aim is to support iGFDS.
 */
public class SysDir {
	
	public static int worknumber = 1;
	public static String instantiationservletaddress0 = null; //WorkflowCore instantiation servlet 0 - bind LogicProcess to MessageType
	public static String instantiationservletaddress = null; //WorkflowCore instantiation servlet 1 - Transform LogicProcess and MessageType to BPEL Workflow
	public static String executionservletaddress = null;
	public static String registrationaddress = null;
	public static String NOTIFICATION_EMAIL  = null;
    public static String NOTIFICATION_EMAIL_SERVICE_URL = null;
    public static String CACHE_OPERATION = null;
    public static String CACHE_SERVICE_URL = null;
    public static String CACHE_DATA_URLPREFIX = null;
    public static String CSISS_CSW_URL = null;
    public static String PREFIXURL = null;
	
	static{
		//initialize from config file
		try {
			BaseTool t = new BaseTool();
			String configfile = t.getClassPath()+File.separator+"config.properties";
			FileInputStream ferr;
			ferr = new FileInputStream(configfile);
			Properties p = new Properties();	
			p.load(ferr);
			ferr.close();
			String number = p.getProperty("workernumber");
			SysDir.worknumber = Integer.parseInt(number);
			instantiationservletaddress0 = p.getProperty("instantiationservletaddress0");
			instantiationservletaddress = p.getProperty("instantiationservletaddress");
			executionservletaddress = p.getProperty("executionservletaddress");
			registrationaddress = p.getProperty("registrationaddress");
			NOTIFICATION_EMAIL = p.getProperty("notify");
			NOTIFICATION_EMAIL_SERVICE_URL = p.getProperty("notificationserviceaddress");
			CACHE_OPERATION = p.getProperty("datacacheoperation");
			CACHE_SERVICE_URL = p.getProperty("datacacheserviceaddress");
			CSISS_CSW_URL = p.getProperty("csisscswurl");
			CACHE_DATA_URLPREFIX = p.getProperty("datacacheprefix");
			PREFIXURL = p.getProperty("prefixurl");
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}

}
