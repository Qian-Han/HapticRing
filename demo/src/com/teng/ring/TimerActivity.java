package com.teng.ring;

import java.io.IOException;
import java.util.ArrayList;

import processing.core.PApplet;

public class TimerActivity extends PApplet{

	private int seconds = 59;
	private int mins = 5;
	private int width = 1280;
	private int height = 800;
	
	public void settings(){
		print("hello\n");
		size(1280,800);
    }

    public void setup(){
    	background(255);
    	
    	/*
    	try {
			server = new Server();
			println(server.getIpAddress());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}*/
    }

    public void draw(){
    	background(255);
    	
    	textSize(64);

    	fill(20, 20, 20, 200);
    	text("Next meeting starts in: ", 300, 300); 
    	text("m", 540, 450);
    	text("s", 750, 450); 
    	
    	if(mins > 4)
    	{
    		fill(0, 102, 153, 150);
    	}else
    	{
    		fill(250, 20, 20, 150);
    	}
    	text("" + mins, 450, 450);
    	text("" + seconds, 650, 450);
    
    	delay(1000);
    	
    	seconds--;
    	if(seconds == -1)
    	{
    		seconds = 59;
    		mins--;
    	}
    }
    
    public void keyPressed() {
    	if (key == 'q') {
    		//server.onDestroy();
    	    exit();
    	}
    }
	
	
	public static final void main(String args[]){
		PApplet.main("com.teng.ring.TimerActivity");
	}
}
