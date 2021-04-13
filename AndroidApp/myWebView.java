package com.example.keyva.rclandcruiser;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebSettings;
import android.widget.Button;
import android.webkit.WebView;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.widget.Toast;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

import java.io.ByteArrayOutputStream;
import java.util.Properties;

public class myWebView extends AppCompatActivity
{
    private Button returnMain, buttonStart, forwardBtn, stopBtn, backwardBtn, leftBtn, rightBtn;
    WebView myWebView, myWebView2;
    RCClient rcClient;
    public int pulseWidth = 1500;
    public int pulseWidthY = 1500;

    private    SensorManager sensorManager;
    private Sensor gyroscopeSensor;
    private Sensor gamerotationSensor;
    private SensorEventListener gyroscopeEventListener;
    boolean runningThread = true;
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
        ***************************************************
        */
    Thread thread = new Thread(new Runnable() {
        @Override
        public void run() {
            try  {
                rcClient = new RCClient();
                int oldPW = 0;
                int oldPWY = 0;

                while (runningThread){
                    if (pulseWidth == 500) {
                        break;
                    }

                    if (pulseWidthY == 500) {
                        break;
                    }

                    if (oldPW != pulseWidth) {
                        rcClient.turn(pulseWidth);
                        oldPW = pulseWidth;
                    }
                    if (oldPWY != pulseWidthY) {
                        rcClient.turnY(pulseWidthY);
                        oldPWY = pulseWidthY;
                    }
                    if (oldPW != pulseWidth) {
                        rcClient.turn(pulseWidth);
                        oldPW = pulseWidth;
                    }
                    if (oldPWY != pulseWidthY) {
                        rcClient.turnY(pulseWidthY);
                        oldPWY = pulseWidthY;
                    }
                }

                rcClient.closeUp();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    });
        /*
        **********************************************
        Title: Android Development
        Author: Android Developers
        Date: Feb 18, 2021
        Code version: *
        Availability: developer.android.com/reference/android/hardware/SensorEventListener.
                      developer.android.com/reference/android/hardware/Sensor#
                      developer.android.com/reference/android/hardware/SensorEvent.
        - The primary function of this code allowed me to get a good introduction to android studio code and
        presented a way of establishing connection to the Gyroscope sensor and how to manipulate the code for my required function.
        The code is very generalized functions that every android app requires to function, but customised for my needs.
        ***************************************************
        */
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_web_view);

        //Remove notification bar Source = https://stackoverflow.com/questions/2591036/how-to-hide-the-title-bar-for-an-activity-in-xml-with-existing-custom-theme
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        //set content view AFTER ABOVE sequence (to avoid crash)
        this.setContentView(R.layout.activity_my_web_view);

        try
        {
            this.getSupportActionBar().hide();
        }
        catch (NullPointerException e){}
        myWebView = (WebView) findViewById(R.id.webView);
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        myWebView.loadUrl("172.16.1.77:5000");
        thread.start();

        buttonStart = (Button) findViewById(R.id.buttonStart);
        buttonStart.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                pulseWidth = 1500;
                pulseWidthY = 1500;
                ///thread.start();
                runningThread = true;
                        /*
                **********************************************
                Title: Execute SSH commands on Raspberry pi with and Android app
                Author: Michael Thum
                Date: May 23, 2017
                Code version: *
                Availability: https://stackoverflow.com/questions/28099291/execute-ssh-command-on-rasperry-pi-with-android-app

                - The primary function of this code allowed me to get a good introduction to android studio code and
                presented a way of establishing connection to the Raspberry pi in order to execute SSH commands.
                It was incredibly hard to piece together old code that used depreciated libraries but this example proved as
                the best stepping stone to the best libraries to perform the function I required.
                ***************************************************
                */
                //POST method
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        try {
                            executeRemoteCommandStart("pi", "Freddy121314","172.16.1.77", 22);
                            //Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        return null;
                    }
                }.execute(1);
                //buttonStart.setEnabled(false);
            }
        });
        stopBtn = findViewById(R.id.stopBtn);
        stopBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
//POST method
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        try {
                            executeRemoteCommandStop("pi", "Freddy121314","172.16.1.77", 22);
                            //Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        return null;
                    }
                }.execute(1);
                //thread.sleep(5000);
                //rcClient.closeUp();
                runningThread = false;
            }

        });
        forwardBtn = findViewById(R.id.forwardBtn);
        forwardBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
//POST method
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        try {
                            executeRemoteCommandForward("pi", "Freddy121314","172.16.1.77", 22);
                            //Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        return null;
                    }
                }.execute(1);
            }

        });
        backwardBtn = findViewById(R.id.backwardBtn);
        backwardBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
//POST method
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        try {
                            executeRemoteCommandBackward("pi", "Freddy121314","172.16.1.77", 22);
                            //Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        return null;
                    }
                }.execute(1);
            }

        });
        leftBtn = findViewById(R.id.leftBtn);
        leftBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
//POST method
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        try {
                            executeRemoteCommandLeft("pi", "Freddy121314","172.16.1.77", 22);
                            //Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        return null;
                    }
                }.execute(1);
            }

        });
        rightBtn = findViewById(R.id.rightBtn);
        rightBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
//POST method
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        try {
                            executeRemoteCommandRight("pi", "Freddy121314","172.16.1.77", 22);
                            //Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        return null;
                    }
                }.execute(1);
            }

        });
        ///////// GYROSCOPE CODE
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        gyroscopeSensor = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE_UNCALIBRATED);
        sensorManager.registerListener(gyroscopeEventListener, gyroscopeSensor, SensorManager.SENSOR_DELAY_GAME);

        if (gyroscopeSensor == null) {
            Toast.makeText(this, "The device has no Gyroscope !", Toast.LENGTH_SHORT).show();
            finish();
        }

        gyroscopeEventListener = new SensorEventListener() {
                /*
           **********************************************
           Title: Android Development
           Author: Android Developers
           Date: Feb 18, 2021
           Code version: *
           Availability: developer.android.com/reference/android/hardware/SensorEventListener.
                         developer.android.com/reference/android/hardware/Sensor#
                         developer.android.com/reference/android/hardware/SensorEvent.
           - The primary function of this code allowed me to get a good introduction to android studio code and
           presented a way of establishing connection to the Gyroscope sensor and how to manipulate the code for my required function.
           The code is very generalized functions that every android app requires to function, but customised for my needs.
           ***************************************************
           */
            @Override
            public void onSensorChanged(SensorEvent sensorEvent) {
                //pulseWidth = 0;

                if (sensorEvent.values[0] > 0.15f) { // turn right
                    for (int i = 0; i < 10; i++)
                    {
                        if (pulseWidth < 2400)
                        {
                            pulseWidth = pulseWidth + 5;
                        }
                        else if (pulseWidth >= 2400)
                        {
                            pulseWidth = 2400;
                        }
                    }
                    //pulseWidth = pulseWidth + 50;
                }
                if (sensorEvent.values[1] > 0.15f) { // turn up
                    for (int i = 0; i < 7; i++)
                    {
                        if (pulseWidthY > 1250)
                        {
                            pulseWidthY = pulseWidthY - 5;
                        }
                        else if (pulseWidthY <= 1250)
                        {
                            pulseWidthY = 1250;
                        }
                    }
                    //pulseWidthY = pulseWidthY - 50;
                }
                if (sensorEvent.values[0] < -0.15f){ // turn left
                    for (int i = 0; i < 10; i++)
                    {
                        if (pulseWidth > 550)
                        {
                            pulseWidth = pulseWidth - 5;
                        }
                        else if (pulseWidth <= 550)
                        {
                            pulseWidth = 550;
                        }
                    }
                    //pulseWidth = pulseWidth - 50;
                }
                if (sensorEvent.values[1] < -0.15f) { // turn down
                    for (int i = 0; i < 7; i++)
                    {
                        if (pulseWidthY < 2000)
                        {
                            pulseWidthY = pulseWidthY + 5;
                        }
                        else if (pulseWidthY >= 2000)
                        {
                            pulseWidthY = 2000;
                        }
                    }
                    //pulseWidthY = pulseWidthY + 50;
                }


                //if sensor is unreliable, return void
                if (sensorEvent.accuracy == SensorManager.SENSOR_STATUS_UNRELIABLE)
                {
                    return;
                }

            }
            @Override
            public void onAccuracyChanged(Sensor sensor, int i) {
            }
        };


        ///////// GYROSCOPE CODE


        //STEREOSCOPIC VIEW TEST!?!?!?
        //myWebView2 = (WebView) findViewById(R.id.webView);
        //WebSettings webSettings2 = myWebView2.getSettings();
        //webSettings2.setJavaScriptEnabled(true);
        //myWebView2.loadUrl("172.16.1.77:5000");


        returnMain = (Button) findViewById(R.id.returnMain);
        returnMain.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                returnToMain();
            }
        });
    }


    protected void onPause(){
        super.onPause();
        sensorManager.unregisterListener(gyroscopeEventListener);    ///////// GYROSCOPE CODE
        runningThread = false;
    }
    ///////// GYROSCOPE CODE


    @Override
    protected void onDestroy(){
        pulseWidth = 1500;    ///////// GYROSCOPE CODE
        pulseWidthY = 1500;    ///////// GYROSCOPE CODE
        runningThread = false;
        super.onDestroy();
    }

    protected void onResume(){
        super.onResume();
        myWebView.onResume();
        sensorManager.registerListener(gyroscopeEventListener, gyroscopeSensor, SensorManager.SENSOR_DELAY_NORMAL);    ///////// GYROSCOPE CODE
        runningThread = true;
    }

    public void returnToMain()
    {
        Intent Intent = new Intent(this, MainActivity.class);
        startActivity(Intent);
    }
    /*
        **********************************************
        Title: Execute SSH commands on Raspberry pi with and Android app
        Author: Michael Thum
        Date: May 23, 2017
        Code version: *
        Availability: https://stackoverflow.com/questions/28099291/execute-ssh-command-on-rasperry-pi-with-android-app

        - The primary function of this code allowed me to get a good introduction to android studio code and
        presented a way of establishing connection to the Raspberry pi in order to execute SSH commands.
        It was incredibly hard to piece together old code that used depreciated libraries but this example proved as
        the best stepping stone to the best libraries to perform the function I required.
        ***************************************************
        */
    public static String executeRemoteCommandForward(String username,String password,String hostname,int port)
            throws Exception {
        JSch jsch = new JSch();
        Session session = jsch.getSession(username, hostname, port);
        session.setPassword(password);

        // Avoid asking for key confirmation
        Properties prop = new Properties();
        prop.put("StrictHostKeyChecking", "no");
        session.setConfig(prop);

        session.connect();

        // SSH Channel
        ChannelExec channelssh = (ChannelExec)
                session.openChannel("exec");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        channelssh.setOutputStream(baos);

        // Execute command
        channelssh.setCommand("python /home/pi/Desktop/servoForward.py");
        //channelssh.setCommand("lsusb > /home/pi/test.txt");
        //channelssh.setCommand("sudo reboot");
        channelssh.connect();
        channelssh.disconnect();


        return baos.toString();
    }
    public static String executeRemoteCommandBackward(String username,String password,String hostname,int port)
            throws Exception {
        JSch jsch = new JSch();
        Session session = jsch.getSession(username, hostname, port);
        session.setPassword(password);

        // Avoid asking for key confirmation
        Properties prop = new Properties();
        prop.put("StrictHostKeyChecking", "no");
        session.setConfig(prop);

        session.connect();

        // SSH Channel
        ChannelExec channelssh = (ChannelExec)
                session.openChannel("exec");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        channelssh.setOutputStream(baos);

        // Execute command
        channelssh.setCommand("python /home/pi/Desktop/servoBackward.py");
        //channelssh.setCommand("lsusb > /home/pi/test.txt");
        //channelssh.setCommand("sudo reboot");
        channelssh.connect();
        channelssh.disconnect();


        return baos.toString();
    }
    public static String executeRemoteCommandLeft(String username,String password,String hostname,int port)
            throws Exception {
        JSch jsch = new JSch();
        Session session = jsch.getSession(username, hostname, port);
        session.setPassword(password);

        // Avoid asking for key confirmation
        Properties prop = new Properties();
        prop.put("StrictHostKeyChecking", "no");
        session.setConfig(prop);

        session.connect();

        // SSH Channel
        ChannelExec channelssh = (ChannelExec)
                session.openChannel("exec");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        channelssh.setOutputStream(baos);

        // Execute command
        channelssh.setCommand("python /home/pi/Desktop/servoLeft.py");
        //channelssh.setCommand("lsusb > /home/pi/test.txt");
        //channelssh.setCommand("sudo reboot");
        channelssh.connect();
        channelssh.disconnect();


        return baos.toString();
    }
    public static String executeRemoteCommandRight(String username,String password,String hostname,int port)
            throws Exception {
        JSch jsch = new JSch();
        Session session = jsch.getSession(username, hostname, port);
        session.setPassword(password);

        // Avoid asking for key confirmation
        Properties prop = new Properties();
        prop.put("StrictHostKeyChecking", "no");
        session.setConfig(prop);

        session.connect();

        // SSH Channel
        ChannelExec channelssh = (ChannelExec)
                session.openChannel("exec");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        channelssh.setOutputStream(baos);

        // Execute command
        channelssh.setCommand("python /home/pi/Desktop/servoRight.py");
        //channelssh.setCommand("lsusb > /home/pi/test.txt");
        //channelssh.setCommand("sudo reboot");
        channelssh.connect();
        channelssh.disconnect();


        return baos.toString();
    }
    public static String executeRemoteCommandStart(String username,String password,String hostname,int port)
            throws Exception {
        JSch jsch = new JSch();
        Session session = jsch.getSession(username, hostname, port);
        session.setPassword(password);

        // Avoid asking for key confirmation
        Properties prop = new Properties();
        prop.put("StrictHostKeyChecking", "no");
        session.setConfig(prop);

        session.connect();

        // SSH Channel
        ChannelExec channelssh = (ChannelExec)
                session.openChannel("exec");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        channelssh.setOutputStream(baos);

        // Execute command
        channelssh.setCommand("python /home/pi/Desktop/servoStart.py");
        //channelssh.setCommand("lsusb > /home/pi/test.txt");
        //channelssh.setCommand("sudo reboot");
        channelssh.connect();
        channelssh.disconnect();


        return baos.toString();
    }
    public static String executeRemoteCommandStop(String username,String password,String hostname,int port)
            throws Exception {
        JSch jsch = new JSch();
        Session session = jsch.getSession(username, hostname, port);
        session.setPassword(password);

        // Avoid asking for key confirmation
        Properties prop = new Properties();
        prop.put("StrictHostKeyChecking", "no");
        session.setConfig(prop);

        session.connect();

        // SSH Channel
        ChannelExec channelssh = (ChannelExec)
                session.openChannel("exec");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        channelssh.setOutputStream(baos);

        // Execute command
        channelssh.setCommand("python /home/pi/Desktop/servoStop.py");
        //channelssh.setCommand("lsusb > /home/pi/test.txt");
        //channelssh.setCommand("sudo reboot");
        channelssh.connect();
        channelssh.disconnect();


        return baos.toString();
    }
}
