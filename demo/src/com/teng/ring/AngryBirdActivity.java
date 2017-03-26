package com.teng.ring;

/**
 * need to run the angray bird app in full screen mode
 * this is to mock up the mouse event
 * @author hanteng
 *
 */

import java.awt.AWTException;
import java.awt.Cursor;
import java.awt.Point;
import java.awt.Robot;
import java.awt.Toolkit;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;
import java.io.IOException;

import javax.swing.JFrame;
import javax.swing.JPanel; 

public class AngryBirdActivity extends JPanel{

	public Robot robot = new Robot();
	private String activityTag = "angrybird";
	private Server server;
	public boolean isReadyToGo = false;
	public int playState = 1; // 1 - up and down, 2 - left and right  3 - release
	private int baseXPos = 0;
	private int baseYPos = 0;
	private int xPos = 0;
	private int yPos = 0;
	private int preXPos = 0;
	private int preYPos = 0;
	private float angleLimit = 180;
	private float posLimit = 100;
	
	public static void main(String[] args) throws AWTException
	{
		JFrame frame = new JFrame("mini");
		AngryBirdActivity angry = new AngryBirdActivity();
		frame.add(angry);
	    frame.setSize(200, 200);
	    frame.setVisible(true);
	    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	    
	    BufferedImage cursorImg = new BufferedImage(16, 16, BufferedImage.TYPE_INT_ARGB);
	    Cursor blankCursor = Toolkit.getDefaultToolkit().createCustomCursor(
	    	    cursorImg, new Point(0, 0), "blank cursor");
	    
	    frame.getContentPane().setCursor(blankCursor);
	}
	
	public static AngryBirdActivity instance;
	public static AngryBirdActivity getInstance()
	{
		if(instance == null)
		{
			try {
				instance = new AngryBirdActivity();
			} catch (AWTException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return instance;
	}
	
	public AngryBirdActivity() throws AWTException
	{
		
		instance = this;
		
		robot.setAutoDelay(40);
	    robot.setAutoWaitForIdle(true);
	    
	    //move to the original position and get ready
	    robot.delay(100);
	    robot.mouseMove(40, 130);
	    
	    
	    //server
	    try {
			server = new Server(activityTag);
			System.out.println(server.getIpAddress());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	  
	

	public void mouseReset()
	{
		//continue the game
		robot.delay(5000);
		
		
		
		
		robot.mouseMove(200, 310);
		robot.delay(100);
		robot.mousePress(InputEvent.BUTTON1_MASK);
		robot.delay(100);
		robot.mouseRelease(InputEvent.BUTTON1_MASK);
		robot.delay(100);
		
		robot.mousePress(InputEvent.BUTTON1_MASK);
		robot.delay(100);
		robot.mouseRelease(InputEvent.BUTTON1_MASK);
		robot.delay(100);
		
		
		
		//move the game view to left
		robot.mousePress(InputEvent.BUTTON1_MASK);
		robot.delay(100);
		robot.mouseMove(800, 610);
		robot.delay(1000);
		robot.mouseRelease(InputEvent.BUTTON1_MASK);
		robot.delay(1000);
		
		
		//set the cursor to start position
		robot.mouseMove(450, 625);
		robot.delay(1000);
		robot.mousePress(InputEvent.BUTTON1_MASK);
		robot.delay(2000);
		robot.mouseMove(420, 625);
		robot.delay(1000);
		
		
		
		
		robot.mouseMove(420, 625);
		baseXPos = 420;
		baseYPos = 625;
		xPos = baseXPos;
		yPos = baseYPos;
		preXPos = xPos;
		preYPos = yPos;
		
		isReadyToGo = true;
	}
	
	public void toPosition(float angle) //what about 180 degree to 50 on screen
	{
		
		if(playState == 1)
		{
			//translate to up and down,  mouse is pressed
			if(Math.abs(angle) < angleLimit)
			{
				yPos = baseYPos - (int)(angle * posLimit / angleLimit);
			}
			
			if(Math.abs(yPos - preYPos) >= 5){
				robot.mouseMove(xPos, yPos);
				preYPos = yPos;
			}
			
			
		}else if(playState == 2)
		{
			//translate to left and right, mouse is pressed
			if(Math.abs(angle) < angleLimit)
			{
				xPos = baseXPos + (int)(angle * posLimit / angleLimit);
			}
			
			if(Math.abs(xPos - preXPos) >= 5){
				robot.mouseMove(xPos, yPos);
				preXPos = xPos;
			}
			
			
		}else if(playState == 3)
		{
			//release, release the mouse
			robot.mouseRelease(InputEvent.BUTTON1_MASK);
		}
		

	}
	
	
	public void mousePress()
	{
	    robot.mousePress(InputEvent.BUTTON1_MASK);
	}
	
	public void mouseMove(int x, int y)
	{
		robot.mouseMove(x, y);
	}
	
	public void mouseRelease()
	{
		robot.mouseRelease(InputEvent.BUTTON1_MASK);
	}
	
	
}
