package com.teng.ring;

import java.io.IOException;
import java.util.ArrayList;

import processing.core.PApplet;
import processing.core.PImage;

public class LockerActivity extends PApplet{
	
	//private Server server;
	private String activityTag = "locker";
	private PImage locker;
	private PImage rotator;
	public float rotateAngle = 0.0f;
	private Server server;
	
	public static LockerActivity instance;
	public static LockerActivity getInstance()
	{
		if(instance == null)
		{
			instance = new LockerActivity();
		}
		return instance;
	}
	
	public void settings(){
		print("hello\n");
		size(1280,800);
    }

    public void setup(){
    	background(255);
    	instance = this;
    	
    	locker = loadImage("locker_outer.png");
    	rotator = loadImage("locker_inner.png");
    	
    	
    	try {
			server = new Server(activityTag);
			println(server.getIpAddress());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
    
    public void draw()
    {
    	background(255);
    	
    	//rotateAngle += 0.01f;
    	
    	pushMatrix();
    	translate(width/2, height/2 + 60);
    	rotate(rotateAngle * PI / 180 );
    	image(rotator, -17.16f, -79.56f, 28.6f, 132.6f);
    	popMatrix();
    	
    	image(locker, 480, 180, 320, 440);
    }
    
    public void keyPressed() {
    	if (key == 'q') {
    		//server.onDestroy();
    	    exit();
    	}else if(key == 'e' || key == 'x')
    	{
    		server.sendMessage("" + key);
    	}
    }
	
	public static final void main(String args[]){
		PApplet.main("com.teng.ring.LockerActivity");
	}

}
