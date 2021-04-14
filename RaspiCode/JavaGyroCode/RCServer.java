import java.io.*;
import java.net.*;
/*
            **********************************************
            Title: Android Remote Control Part 1*
            Author: Daniel Ross
            Date: Feb 02, 2017
            Code version: *
            Availability: www.youtube.com/watch?v=Zgmaho84d2I&list=PL6LQDONHZvFJH6b_YFybR9Bi3nXPFhjU5&index=13.
            - The primary function of this code allowed me to get a good introduction to android studio code and
            presented a javascript alternative to open a network socket with the Raspberry pi in order to
            transmit data in real-time. **This is actually not even used within mainactivity.java but served as
            the stepping stone for the research and development
            *** THE PRIMARY FUNCTION OF THIS CODE IS TO ONLY CONTROL THE GYROSCOPE SERVO MECHANISM
	    *** The functions are created by Daniel Ross and the limits and variables manipulated for my
		gyroscope functionality. This is the part of the project that opens a network socket and
		sends a pulsewidth variable to the server to extract the integer value from the string.
            ***************************************************
            */

public class RCServer {

    private static final int STEERING_CENTER = 1500;
    private static final int STEERING_RIGHT_MAX = 500;
    private static final int STEERING_LEFT_MAX = 2500;
    private static final int GPIO_PIN = 23;
    private static final int PINY = 22;

    private Steering steering;
    //private Steering steeringY;

    RCServer() {                         
        this.steering = new Steering();    
	//this.steeringY = new Steering();     
    }

    public static void main(String[] args){
    
        RCServer rcServer = new RCServer();

        try(ServerSocket serverSocket = new ServerSocket(4141)) 
	{
            while (true)
	    {
                System.out.println("Listening on port 4141, CRTL-C to quit ");
                Socket socket = serverSocket.accept();
                try ( 	PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
                        BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                ){
                    System.out.println("Connection accepted.");
                    String in = "";
                    while ((in = input.readLine()) != null) {
                        System.out.println("Received: " + in);
                        if (in.equals("SYN")){ // Synchronize
                            rcServer.write(output, "SYN-ACK"); // Synchronize-Acknowledge
                        }	
                        if (in.equals("FIN")){ // Final
                            rcServer.write(output, "FIN-ACK"); // Final-Acknowledge
                            break;
                        }
                        if (in.contains("pwAngle=")){
                            rcServer.write(output, rcServer.turn(in));
                        }
			if (in.contains("pwAngleY=")){
                            rcServer.write(output, rcServer.turnY(in));
                        }
		    }
		    
                    System.out.print("Closing socket.\n\n");				
                } catch (IOException e) {
                    e.printStackTrace();	
                } 
	    }
	} catch (IOException e) {
            e.printStackTrace();	
        } 
        
    }

    void write(PrintWriter output, String message) {
        System.out.println("Sending: "+message);
        output.println(message);
    }

    String turn(String input) {
        int i = 0;
        try {
            i = Integer.parseInt(input.substring(8));
            i = (STEERING_RIGHT_MAX + STEERING_LEFT_MAX) - i; // Reverse the value to correct the physical turning direction
            if (i >= STEERING_RIGHT_MAX && i <= STEERING_LEFT_MAX) {
                steering.turnWheels(GPIO_PIN, i);
		//steering.turnWheels(PINY, i);
                return ("response=OK");
	    }
	    
        } catch (NumberFormatException e) {
            return ("response=FAILED");
        }
        return "response=FAILED";
    }

    String turnY(String input) {
        
	int x = 0;
        try {
            
	    x = Integer.parseInt(input.substring(9));
            x = (STEERING_RIGHT_MAX + STEERING_LEFT_MAX) - x; // Reverse the value to correct the physical turning direction
            if (x >= STEERING_RIGHT_MAX && x <= STEERING_LEFT_MAX) {
                steering.turnWheels(PINY, x);
                return ("response=OK");
            }
        } catch (NumberFormatException e) {
            return ("response=FAILED");
        }
        return "response=FAILED";
    }

        
}
