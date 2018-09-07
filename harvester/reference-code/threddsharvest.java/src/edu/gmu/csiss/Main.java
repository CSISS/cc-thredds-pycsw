package edu.gmu.csiss;
/**
*Class Main.java
*@author Ziheng Sun
*@time Jun 7, 2017 5:16:44 PM
*Original aim is to support CyberConnector.
*/
public class Main {

	public static void run(String cswurl, String threddsurl, String indexfile, String mode, String crawlonly, String registeronly, String lastupdatetime){
		
		long start = System.currentTimeMillis();
		
		if(mode.equals("init")||mode.equals("update")){
			
			if(!"true".equals(registeronly)){
				
				System.out.println("Create new Crawler");
				Crawler crawler = new Crawler(indexfile, mode,  lastupdatetime);
				
				crawler.run(threddsurl);
				
				crawler.leave();
				
				System.out.println("++++++++++++++++++");
				
				System.out.println("Thredds crawling is over.");
				
				System.out.println("++++++++++++++++++");
				
			}
			
			if(!"true".equals(crawlonly)){
				
				Register register = new Register(cswurl, indexfile);
				
				register.run();
				
				System.out.println("++++++++++++++++++");
				
				System.out.println("The ISO links are registered into CSW.");
				
				System.out.println("++++++++++++++++++");
			}
			
		}else if(mode.equals("sweep")){			
			
			Sweeper sweeper = new Sweeper(cswurl, lastupdatetime);
			
			sweeper.run();
			
		}
		
		long end = System.currentTimeMillis();
		
		System.out.println("The program taks " + (end-start) + " ms.");
		
	}
	
	public static void showHelp(){
		
		System.out.println("usage of ThreddsHavester: ");
		System.out.println("	-c [csw url, e.g. http://cube.csiss.gmu.edu/srv/csw]");
		System.out.println("	-t  [thredds url, e.g. http://thredds.ucar.edu/thredds/catalog.xml]");
		System.out.println("	-m [mode, three options: init, update or sweep]");
		System.out.println("	-co [only crawl to generate the index file]");
		System.out.println("	-ro [only register the data in the index file to csw]");
		System.out.println("	-i [index file path]");
		System.out.println("	-u [last update time. format: 20170605]");
		
		
	}
	
	public static void main(String[] args) {
		
		String cswurl = null;
		
		String threddsurl = null;
		
		String indexfilepath = null;
		
		String mode = null; //init, update or sweep
		
		String crawleronly = null;
		
		String registeronly = null;
		
		String lastupdatetime = null;
		
		for(int i=0;i<args.length;i+=2){
			
			if("-c".equals(args[i])){
					
				cswurl = args[i+1];
				
				System.out.println("CSWURL:" + cswurl);
				
			}else if("-t".equals(args[i])){
				
				threddsurl = args[i+1];
				
				System.out.println("Thredds URL:" + threddsurl);
				
			}else if("-m".equals(args[i])){
				
				mode = args[i+1];
				
				System.out.println("Mode : " + mode);
				
			}else if("-i".equals(args[i])){
				
				indexfilepath = args[i+1];
				
				System.out.println("Index file path : " + indexfilepath);
				
			}else if("-co".equals(args[i])){
				
				crawleronly = args[i+1];
				
				System.out.println("Crawl only?  " + crawleronly);
				
			}else if("-ro".equals(args[i])){
				
				registeronly = args[i+1];
				
				System.out.println("Register only? " + registeronly);
				
			}else if("-u".equals(args[i])){
				
				lastupdatetime = args[i+1];
				
				System.out.println("Last update time : " + lastupdatetime);
				
			}
			
		}
		
		if(!"sweep".equals(mode)){
			
			if(cswurl==null||threddsurl==null||mode==null || indexfilepath == null){
				
				showHelp();
				
				return;
			}
			
		}else{
			
			if(lastupdatetime==null){
				
				showHelp();
				
				return;
				
			}
			
		}
		
		System.out.println("======= Start =======");
		
		run(cswurl, threddsurl, indexfilepath, mode, crawleronly, registeronly, lastupdatetime);
		
		System.out.println("======= End =======");

	}

}
