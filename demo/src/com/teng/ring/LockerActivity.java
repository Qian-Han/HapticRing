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
	public int rotateDirection = 1;
	private Server server;
	
	public boolean isLock = true;
	public int[] password = {1, 1, 1, -1, -1, 1};
	public int[] userAnswer;
	public int anserIter = 0;
	
	
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
		//size(1280,800);  //1280, 800
		fullScreen();  // 1440, 900
		
    }

    public void setup(){
    	background(255);
    	instance = this;
    	
    	locker = loadImage("locker_outer.png");
    	rotator = loadImage("locker_inner.png");
    	
    	userAnswer = new int[6];
    	
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
    	
    	//rotateAngle += 1f;
    	
    	pushMatrix();
    	translate(width/2, height/2 + 10);
    	rotate(rotateAngle * PI / 180 );
    	image(rotator, -17.16f, -79.56f, 34.32f, 159.12f);
    	popMatrix();
    	
    	image(locker, 560, 180, 320, 440);
    	
    	textSize(122);
    	fill(100);
    	
    	if(isLock)
    	{
    		text("LOCK", 580, 800);
    	}else
    	{
    		text("UNLOCK", 500, 800);
    		
    		//do something
    		
    	}
    	
    	
    	
    }
    
    public void checkAnswer()
    {
    	boolean answerCorrect = true;
    	for(int itr = 0; itr < 6; itr++)
    	{
    		if(userAnswer[itr] == password[itr])
    		{
    			
    		}else
    		{
    			answerCorrect = false;
    		}
    	}
    	
    	if(answerCorrect)
    	{
    		isLock = false;
    	}else
    	{
    		anserIter = 0;
    	}
    	
    	
    	
    }
    
    public void keyPressed() {
    	if (key == 'q') {
    		//server.onDestroy();
    	    exit();
    	}
    }
	
	public static final void main(String args[]){
		PApplet.main("com.teng.ring.LockerActivity");
	}

}
