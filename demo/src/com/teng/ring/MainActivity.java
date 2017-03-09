package com.teng.ring;

import processing.core.PApplet;

public class MainActivity extends PApplet{
	public void settings(){
		print("hello");
		size(1280,800);
    }

    public void setup(){
    	background(255);
    }

    public void draw(){

    }
    
    public void keyPressed() {
    	if (key == 'q') {
    	    exit();
    	}
    }
	
	public static final void main(String args[]){
		PApplet.main("com.teng.ring.MainActivity");
	}
	
	
}
