package com.teng.ring;

import java.io.IOException;
import java.util.ArrayList;

import processing.core.PApplet;


/**Profile Change and Authoring Tool
 * Work with Demo_Authoring.py to run the prototype
 * @author hanteng
 *
 */
class MPoint
{
	float xpos, ypos;
	public MPoint(float x, float y)
	{
		xpos = x;
		ypos = y;
	}
	public float getX()
	{
		return xpos;
	}
	public float getY()
	{
		return ypos;
	}
	
	public void setX(float x)
	{
		xpos = x;
	}
	
	public void setY(float y)
	{
		ypos = y;
	}
}

class NPoint
{
	int angle, force;
	public NPoint(int _angle, int _force)
	{
		angle = _angle;
		force = _force;
	}
	
	public int getAngle()
	{
		return angle;
	}
	
	public int getForce()
	{
		return force;
	}
}

public class MainActivity extends PApplet{
	
	//button 
	private int rectX = 1100;
	private int rectY = 40;      // Position of square button
	private int rectSize = 100;     // Diameter of rect
	private boolean rectOver = false;
	private int rectColor = color(200);
	private int rectHighlight = color(180);
	
	//draw profile
	private int width = 1280;
	private int height = 800;
	private int axis_x_start = 200;
	private int axis_x_end = 1000;
	private int axis_y_end = 100;
	private int axis_y_start = 620;
	private int force_zero = 580;
	private int force_full = 150;
	
	private int profile_start_angle = 20;
	private int profile_end_angle = 180;
	private int profile_start_axis_x =  axis_x_start + (axis_x_end - axis_x_start) * profile_start_angle / profile_end_angle;
	
	private int mouseXL = 0;
	
	private int angle_step = 5;
	
	private ArrayList<MPoint> input_points;
	private ArrayList<NPoint> profile;
	
	private Server server;
	private String activityTag = "authoring";
	
	public static MainActivity instance;
	public static MainActivity getInstance()
	{
		if(instance == null)
		{
			instance = new MainActivity();
		}
		return instance;
	}
	
	public void settings(){
		print("hello\n");
		size(1280,800);
    }

    public void setup(){
    	background(255);
    	input_points = new ArrayList<MPoint>();
    	profile = new ArrayList<NPoint>();
    	instance = this;
    	
    	try {
			server = new Server(activityTag);
			println(server.getIpAddress());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }

    public void draw(){
    	//background(255);
    	update(mouseX, mouseY);
    	//draw frame
    	
    	fill(200);
    	stroke(200);
    	strokeWeight(5);
    	line(axis_x_start, axis_y_start, axis_x_end, axis_y_start);
    	line(axis_x_start, axis_y_start, axis_x_start, axis_y_end);

    	textSize(52);
    	text("0", axis_x_start, 700);
    	//text("20", profile_start_axis_x, 700);
    	text("180", axis_x_start + (axis_x_end - axis_x_start) * 180 / profile_end_angle, 700);
    	text("degree", axis_x_start + (axis_x_end - axis_x_start) * 180 / profile_end_angle + 100, 700);
    	text("force", axis_x_start - 150, axis_y_end);
    	
    	//stroke(158, 193, 188, 100);
    	//strokeWeight(3);
    	//line(profile_start_axis_x, axis_y_start, profile_start_axis_x, axis_y_start - 20);
    	
    	fill(235, 152, 44, 200);
    	stroke(235, 152, 44, 200);
    	strokeWeight(3);
    	line(axis_x_start, force_zero, axis_x_end, force_zero);
    	text("0", axis_x_start - 50, force_zero);
    	line(axis_x_start, force_full, axis_x_end, force_full);
    	text("full", axis_x_start - 120, force_full);
    	
    	
    	if (mousePressed == true) {
    		stroke(152, 235, 44, 200);
    		if(mouseX > axis_x_start && mouseX < axis_x_end && pmouseX > axis_x_start && pmouseX < axis_x_end 
    				)
    		{
    			line(mouseX, mouseY, pmouseX, pmouseY);
    			if(mouseX > mouseXL)
    			{
    				if(mouseY > force_full && mouseY < force_zero)
    				{
    					input_points.add(new MPoint(mouseX, mouseY));
    				}else if(mouseY <= force_full)
    				{
    					input_points.add(new MPoint(mouseX, force_full));
    				}else{
    					input_points.add(new MPoint(mouseX, force_zero));
    				}
    				
    				if(input_points.size() == 1)
    				{
    					//put a zero x point there
    					MPoint first_point = new MPoint(axis_x_start, input_points.get(0).getY());
    					input_points.add(0, first_point);
    				}
    				
    			}
    			if(mouseX > mouseXL)
    			{
    				mouseXL = mouseX;
    			}
    			
    		}
    		
    	}else
    	{
    		
    		if(input_points.size() > 0)
        	{
        		stroke(152, 44, 235, 200);
        		for(int i = 1; i < input_points.size(); i++)
        		{
        			line(input_points.get(i).getX(), input_points.get(i).getY(), input_points.get(i-1).getX(), input_points.get(i-1).getY());
        			
        		}
        	}
    	}
    	
    	//draw button
    	if (rectOver) {
    	    fill(rectHighlight);
    	} else {
    	    fill(rectColor);
    	}
    	
    	stroke(200);
    	rect(rectX, rectY, rectSize, rectSize/3);
    	fill(255);
    	textSize(26);
    	text("confirm",rectX,rectY + rectSize/4);
    	
    }
    
    
    void update(int x, int y) {
    	if ( overRect(rectX, rectY, rectSize, rectSize) ) {
    	    rectOver = true;
    	  } 
    	else {
    	    rectOver = false;
    	  }
    }
    
    boolean overRect(int x, int y, int width, int height)  {
    	if (mouseX >= x && mouseX <= x+width && 
    			mouseY >= y && mouseY <= y+height) {
    		return true;
    		} 
    	else {
    		return false;
    	 	}
    }
    
    public void mousePressed()
    {
    	background(255);
    	mouseXL = 0;
    	input_points.clear();
    	
    	if (rectOver) {
    	    //clicked the button
    		server.sendMessage(profileToString(profile));
    	}
    }
    
    public String profileToString(ArrayList<NPoint> _profile)
    {
    	String message = "";
    	if(_profile.size() > 0)
    	{
    		message += ("" + _profile.size() + ",");
    		for(int itrp = 0; itrp < _profile.size(); itrp++)
    		{
    			message += ("" + _profile.get(itrp).getAngle() + "," + _profile.get(itrp).getForce() + ",");
    		}
    	}
    	
    	return message;
    }
    
    public void mouseReleased() {
    	background(255);
    	if(input_points.size() > 1)
    	{
    		
    		/*
    		int profile_start_index = 0;
    		
    		for(int itri = 1; itri < input_points.size(); itri++)
    		{
    			if(input_points.get(itri).getX() < profile_start_axis_x)
        		{
    				input_points.get(itri).setY(input_points.get(0).getY());
        		}else if(input_points.get(itri).getX() > profile_start_axis_x && input_points.get(itri-1).getX() < profile_start_axis_x)
        		{
        			profile_start_index = itri;
        		}
    		}
    		
    		//ad a profile_start file
    		input_points.add(profile_start_index, new MPoint(profile_start_axis_x, input_points.get(0).getY()));
    		
    		//delete unusual start points
    		if(input_points.get(0).getX() > axis_x_start)
    		{
    			//remove it
    			input_points.remove(0);
    		}
    		
    		*/
    		
    		
    		deSample(input_points);
    		
    	}
    	
    	/*
    	for(int itri = 0; itri < input_points.size(); itri++)
    	{
    		println(input_points.get(itri).getX());
    	}
    	
    	println();
    	*/
    }
    
    
    public void keyPressed() {
    	if (key == 'q') {
    		server.onDestroy();
    	    exit();
    	}
    }
    
    public void reSample(ArrayList<MPoint> list)
    {
    	//return a sample site with every 1 points
    	
    }
    
    public void deSample(ArrayList<MPoint> list)
    {	
    	profile.clear();
    	if(list.size() < 2)
    	{
    		
    	}else
    	{
    		ArrayList<MPoint> tempList = new ArrayList<MPoint>();
    		int sd = 0; //sample degree
    		float sd_axis = 1.0f * axis_x_start;  //sample axis x
    		int si = 5; //sample interval
    		//float si_axis = 1.0f * (axis_x_end - axis_x_start) * si / (profile_end_angle - profile_start_angle);
    		float si_axis = 1.0f * (axis_x_end - axis_x_start) * si / profile_end_angle;
    		
    		int sf = 0;  //sample force level
    		float sf_axis = 1.0f * force_zero;
    		int sfi = 1;  //force level interval
    		int sfl = 20; //force levels
    		float sfi_axis = 1.0f * (force_zero - force_full) * sfi / sfl;
    		
    		int itra = 0;
    		tempList.add(list.get(0));  //add 0
    		itra++;
    		
    		//add rest
    		for(sd_axis = axis_x_start + si_axis ; sd_axis < axis_x_end; sd_axis+=si_axis)	
    		{
    			if(itra == list.size())
    			{
    				//all list points were examined
    				tempList.add(new MPoint(sd_axis, list.get(itra-1).getY()));
    				
    			}else
    			{
    				while(list.get(itra).getX() < sd_axis)
        			{
        				itra++;
        				if(itra == list.size())
        					break;
        			}
        			
        			//should be between the itra-1 point and itra point
        			if(itra < list.size())
        			{
        				float sd_axis_y = list.get(itra-1).getY() + (list.get(itra).getY() - list.get(itra-1).getY()) * (sd_axis - list.get(itra-1).getX()) 
            					/ (list.get(itra).getX() - list.get(itra-1).getX());
            			
            			tempList.add(new MPoint(sd_axis, sd_axis_y));
        			}
    			}
    			
    		}
    		
    		list.clear();
    		
    		for(int itrt = 0; itrt < tempList.size(); itrt++)
    		{
    			//map y values
    			float temp_y = tempList.get(itrt).getY();
    			//axis_y_end 
    			//axis_y_start
    			int force_levels = (int) ((force_zero - temp_y) / sfi_axis);
    			int force_angle = sd + itrt * si;
    			//println("" + force_levels);
    			profile.add(new NPoint(force_angle, force_levels));
    			
    			temp_y = sf_axis - force_levels * sfi_axis;
    			
    			list.add(new MPoint(tempList.get(itrt).getX(), temp_y));
    		}
    		
    		
    		/*
    		for(int itrp = 0; itrp < profile.size(); itrp++)
    		{
    			println("[" + profile.get(itrp).getAngle() + " , " + profile.get(itrp).getForce() + "]");
    		}*/
    		
    	}
    	
    	
    }
	
	public static final void main(String args[]){
		PApplet.main("com.teng.ring.MainActivity");
	}
	
	
}
