package com.teng.ring;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.Enumeration;

public class Server {
	static final int socketServerPORT = 9090;
	public ServerSocket serverSocket;
	private Socket clientSocket;
	private PrintStream printStream;
	private OutputStream outputStream;
	
	String message = "";
	
	public Server() throws IOException
	{
		Thread socketServerThread = new Thread(new SocketServerThread());
		socketServerThread.start();
	}
	
	public void onDestroy()
	{
		if(serverSocket != null)
		{
			try{
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
				SocketServerReplyThread socketServerReplyThread = new SocketServerReplyThread();
            	socketServerReplyThread.run();
            	
            	//keep listening
				
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
