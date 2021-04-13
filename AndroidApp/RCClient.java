package com.example.keyva.rclandcruiser;
import java.io.*;
import java.net.*;

public class RCClient  {
    //MainActivity mainActivity;
    public static final String SERVER_IP = "172.16.1.77"; // Change IP address to the IP of the Raspi server
    // Pinout is defined in the code on the server
    /// pinout is defined on server file /java/landcruiser/steering.java

    Socket socket;
    PrintWriter output;
    BufferedReader input;
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
            ***************************************************
            */
    RCClient(){  // Code from Daniel Ross
        try {
            socket = new Socket(InetAddress.getByName(SERVER_IP), 4141);
            // open port 4141 to passthrough to the server over wifi
            output = new PrintWriter(socket.getOutputStream(), true);
            input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            write(output, "SYN"); // Synchronize
        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }           // Code from Daniel Ross

    void turn(int pulseWidth) {
        write(output, "pwAngle=" + pulseWidth);
    }
    void turnY(int pulseWidthY) {
        write(output, "pwAngleY=" + pulseWidthY);
    }
    void write(PrintWriter output, String message) {
        System.out.println("Sending: " +message);
        output.println(message);
    }

    void closeUp() {
        try {
            write(output, "FIN");
            String in = "";
            while ((in = input.readLine()) != null) {
                if (in.equals("FIN-ACK")){ // Final-Acknowledge
                    break;
                }
            }
            System.out.print("Closing socket.");
            input.close();
            output.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
