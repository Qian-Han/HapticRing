package com.teng.ring;

import java.awt.event.InputEvent;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.Enumeration;

public class Server {
	static final int socketServerPORT = 9090;
	public ServerSocket serverSocket;
	private Socket clientSocket;
	private PrintStream printStream;
	private OutputStream outputStream;
	
	private ArrayList<Integer> byteArray;
	private boolean receivingMode = false;
	
	private String message = "";
	private String activityTag;
	
	public Server(String activityTag) throws IOException
	{
		byteArray = new ArrayList<Integer>();
		this.activityTag = activityTag;
		
		Thread socketServerThread = new Thread(new SocketServerThread());
		socketServerThread.start();
	}
	
	public void onDestroy()
	{
		if(serverSocket != null)
		{
			try{
				if(printStream != null)
					printStream.close();
				serverSocket.close();
				System.out.println("server closed");
			}catch(IOException e)
			{
				e.printStackTrace();
			}
		}
	}
	
	private class SocketServerThread extends Thread {
		
		@Override
		public void run()
		{
			try{
				serverSocket = new ServerSocket(socketServerPORT);
				//incoming socket connection
				clientSocket = serverSocket.accept();
				message = "#1" + " from "
                        + clientSocket.getInetAddress() + ":"
                        + clientSocket.getPort() + "\n";
				
				System.out.println(message);
				
				outputStream = clientSocket.getOutputStream();
				printStream = new PrintStream(outputStream);
				
				//reply a connection confirmation
				//SocketServerReplyThread socketServerReplyThread = new SocketServerReplyThread();
            	//socketServerReplyThread.run();
            	
				
				if(activityTag == "angrybird")
				{
					AngryBirdActivity.getInstance().mouseReset();
				}
				
				
            	//keep listening
            	if(activityTag == "angrybird" || activityTag == "locker")
            	{
            		SocketServerReceiveThread socketServerReceiveThread = new SocketServerReceiveThread();
            		socketServerReceiveThread.run();
            	}
            	
				
			}catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
			
		}
	}
	
	private class SocketServerReplyThread extends Thread {

        SocketServerReplyThread() {
            
        }

        @Override
        public void run() {
            String msgReply = "Hello from Server";
            printStream.print(msgReply);
        } 
    }
	
	
	private class SocketServerSendThread extends Thread {
		String msgSend;
		
        SocketServerSendThread(String msg) {
        	msgSend = msg;
        }

        @Override
        public void run() {
        	printStream.print(msgSend);
        } 
    }
	
	public void sendMessage(String msg)
	{
		SocketServerSendThread socketServerSendThread = new SocketServerSendThread(msg);
    	socketServerSendThread.run();
	}
	
	private class SocketServerReceiveThread extends Thread {
		public boolean keepReading = true;
		//private BufferedInputStream input;
		//private InputStreamReader input;
		private BufferedReader input;
		private String msg;
		private String[] values;
		
		public SocketServerReceiveThread()
		{
			try {
				//this.input = new BufferedInputStream(clientSocket.getInputStream());
				this.input = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		@Override
		public void run()
		{
			while(!Thread.currentThread().isInterrupted() && keepReading)
			{
				try {
					if(clientSocket.isConnected())
					{
						
					}else
					{
						keepReading = false;
						System.out.println("connection lost");
						break;
					}
					
					//int byteRead = input.read();  
					//byteArray.add(byteRead);
					
					//lets read string
					if(input != null)
					{
						if((msg = input.readLine()) != null)  //when client lost, will read null
						{
							//System.out.println(msg);
							values = msg.split(",");
						}else
						{
							keepReading = false;
							continue;
						}
					}
					
					if(activityTag == "locker")
					{
						//values
						if(values.length == 1)
						{
							LockerActivity.getInstance().rotateAngle = Float.valueOf(values[0]);
						}else if(values.length == 2)
						{
							LockerActivity.getInstance().userAnswer[LockerActivity.getInstance().anserIter] = Integer.valueOf(values[0]);
							LockerActivity.getInstance().anserIter++;
							
							if(LockerActivity.getInstance().anserIter == 6)
							{
								//should check 
								LockerActivity.getInstance().checkAnswer();
								
							}else if(LockerActivity.getInstance().anserIter == 7)
							{
								LockerActivity.getInstance().showAnswer();
							}
						}
						else
						{
							continue;
						}
						
						
						
						
						
						
					}
					
					
					/*
					if(activityTag == "angrybird")
					{
						//if three items, x, y, z
						if(byteArray.size() == 3)
						{
							if(byteArray.get(2) == 1)
							{
								//mouse press down
							}else if(byteArray.get(2) == 2)
							{
								//mouse release
							}else if(byteArray.get(2) == 3)
							{
								//hold
								int x = (int)byteArray.get(0);
								int y = (int)byteArray.get(1);
								
								//mouse move to
							}
							
							byteArray.clear();
						}
					}else if(activityTag == "locker")
					{
						if(byteArray.size() == 1)
						{
							//this is only the angle
							//from byte to float
							LockerActivity.getInstance().rotateAngle = (float)byteArray.get(0);
							
							byteArray.clear();
						}
					}
					
					*/
					
				}catch (IOException e) {
                    e.printStackTrace();
                }
			}
		}
	}
	
	public String getIpAddress() {
        String ip = "get ip address ";
        try {
            Enumeration<NetworkInterface> enumNetworkInterfaces = NetworkInterface.getNetworkInterfaces();

            while (enumNetworkInterfaces.hasMoreElements()) {
                NetworkInterface networkInterface = enumNetworkInterfaces
                        .nextElement();
                Enumeration<InetAddress> enumInetAddress = networkInterface
                        .getInetAddresses();

                while (enumInetAddress.hasMoreElements()) {
                    InetAddress inetAddress = enumInetAddress
                            .nextElement();

                    //if (inetAddress.isSiteLocalAddress()) {
                        ip += "Server running at : "
                                //+ inetAddress.getHostAddress();
                                    +inetAddress.toString();
                    //}
                }
            }

        } catch (SocketException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            ip += "Something Wrong! " + e.toString() + "\n";
        }
        return ip;
    }
	
}
