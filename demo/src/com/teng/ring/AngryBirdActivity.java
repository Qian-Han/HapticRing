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
