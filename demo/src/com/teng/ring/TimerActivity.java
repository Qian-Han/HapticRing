package com.teng.ring;

import java.io.IOException;
import java.util.ArrayList;

import processing.core.PApplet;

public class TimerActivity extends PApplet{

	private String activityTag = "timer";
	private int hours = 1;
	private int seconds = 59;
	private int mins = 10;
	private int width = 1280;
	private int height = 800;
	
	private boolean isLate = false;
	private boolean isHush = false;
	private Server server;
	
	public void settings(){
		print("hello\n");
		
		fullScreen();  // 1440, 900
    }

    public void setup(){
    	background(255);
    	
    	try {
			server = new Server(activityTag);
			println(server.getIpAddress());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }

    public void draw(){
    	background(255);
    	
    	textSize(64);

    	fill(20, 20, 20, 200);
    	text("Next meeting starts in: ", 380, 350); 
    	
    	if(hours > 0){
    		text("h", 560, 520);
        	text("m", 740, 520);
        	text("s", 940, 520); 
    	}else
    	{
        	text("m", 640, 520);
        	text("s", 860, 520); 
    	}
    	
    	
    	fill(0, 102, 153, 150);
    	if(mins < 15 && hours == 0)
    	{
    		fill(250, 20, 20, 150);
    	}
    	
    	if(hours > 0){
    		text("" + hours, 480, 520);
        	text("" + mins, 640, 520);
        	text("" + seconds, 840, 520);
    	}else
    	{
    		text("" + mins, 540, 520);
        	text("" + seconds, 760, 520);
    	}
    	
    
    	
    	
    	
    	if(isLate == false)
    	{
    		seconds--;
        	if(seconds == -1)
        	{
        		seconds = 59;
        		mins--;
        		
        		if(mins == -1)
        		{
        			mins = 59;
        			hours--;
        			
        		}
        	}
    	}
    	
    	
    	
    	if(hours == 0 && mins == 15 && seconds == 0)
    	{
    		if(isHush == false)
    		{
    			isHush = true;
    			server.sendMessage("72");
    			print("is hush");
    		}
    	}
    	
    	
    	
    	if(hours == 0 && mins == 0 && seconds == 0)
    	{
    		//being late
    		if(isLate == false)
    		{
    			isLate = true;
    			server.sendMessage("73");
    			print("is late");
    		}
    		
    	}
    	
    	
    	delay(1000);
    	
    	
    }
    
    public void keyPressed() {
    	if (key == 'q') {
    		//server.onDestroy();
    	    exit();
    	}else if(key == 'e' || key == 'x')
    	{
    		server.sendMessage("" + key);
    	}else if(key == 'a')
    	{
    		hours = 0;
    		mins = 15;
    		seconds = 15;
    	}else if(key == 'b')
    	{
    		hours = 0;
    		mins = 0;
    		seconds = 10;
    	}
    }
	
	
	public static final void main(String args[]){
		PApplet.main("com.teng.ring.TimerActivity");
	}
}
