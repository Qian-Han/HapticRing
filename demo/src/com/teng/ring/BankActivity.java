package com.teng.ring;

import java.io.IOException;
import java.util.ArrayList;

import processing.core.PApplet;
import processing.core.PImage;

public class BankActivity extends PApplet{
	
	private PImage bankBackground;
	private int day_1 = 1;
	private int day_2 = 0;
	private int balance = 1000;
	
	private boolean animation = false;
	private int wait = 500;
	private int time;
	
	public void settings(){
		print("hello\n");
		size(1280,800);
    }

    public void setup(){
    	background(255);
    	
    	/*
    	try {
			server = new Server(activityTag);
			println(server.getIpAddress());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}*/
    	
    	bankBackground = loadImage("bank.png");
    }
    
    
    public void draw(){
    	background(255);
    	image(bankBackground, 0, 0, width, height);
    	
    	//date
    	fill(181, 181, 181);
    	textSize(182);
    	text("" + day_2, 680, 260);
    	text("" + day_1, 820, 260);
    	
    	
    	//balance
    	fill(2, 159, 204);
    	textSize(122);
    	text("" + balance, 350, 610);
    	
    	if(animation)
    	{
    		if(millis() - time >= wait)
    		{
    			day_1 += 1;
    			if(day_1 == 10)
    			{
    				day_2 += 1;
    				day_1 = 0;
    			}
    			
    			if(day_2 == 3 && day_1 == 1)
    			{
    				animation = false;
    			}
    			
    			balance -= 32;
    			
    			if(wait > 100){
    				wait -= 50;
    			}
    			
    			time = millis();
    		}
    	}
    	
    }
    
    public void keyPressed() {
    	if (key == 'q') {
    		//server.onDestroy();
    	    exit();
    	}else if(key == 'a')
    	{
    		animation = true;
    		time = millis();
    	}else if(key == 'r')
    	{
    		animation = false;
    		wait = 500;
    		day_2 = 0;
    		day_1 = 1;
    		balance = 1000;
    	}
    	
    }
    
    
    public static final void main(String args[]){
		PApplet.main("com.teng.ring.BankActivity");
	}
    
    
    

}
