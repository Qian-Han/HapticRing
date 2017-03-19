package com.teng.ring;

/**
 * need to run the angray bird app in full screen mode
 * this is to mock up the mouse event
 * @author hanteng
 *
 */

import java.awt.AWTException;
import java.awt.Robot;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;

import javax.swing.JFrame;
import javax.swing.JPanel; 

public class AngryBirdActivity extends JPanel{

	public Robot robot = new Robot();
	private String acitivtyTag = "angrybird";
	
	public static void main(String[] args) throws AWTException
	{
		JFrame frame = new JFrame("mini");
		AngryBirdActivity angry = new AngryBirdActivity();
		frame.add(angry);
	    frame.setSize(200, 200);
	    frame.setVisible(true);
	    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
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
		robot.setAutoDelay(40);
	    robot.setAutoWaitForIdle(true);
	    
	    //move to the original position and get ready
	    robot.delay(100);
	    robot.mouseMove(40, 130);
	    
	    
	    //server
	    
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
