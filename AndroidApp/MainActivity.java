package com.example.keyva.rclandcruiser;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;
import android.content.Intent;

import android.os.AsyncTask;
import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

import java.io.ByteArrayOutputStream;
import java.util.Properties;
//<uses-permission android:name="android.permission.INTERNET" />



public class MainActivity extends AppCompatActivity {

    Button buttonStart, buttonStop, webView, postBtn;
    SeekBar seekBar;
    SeekBar seekBar2;
    TextView textViewProgress;
    TextView textViewProgress2;

    RCClient rcClient;
    public int pulseWidth = 1500;
    public int pulseWidthY = 1500;

    private    SensorManager sensorManager;
    private Sensor gyroscopeSensor;
    private Sensor gamerotationSensor;
    private SensorEventListener gyroscopeEventListener;
    private SensorEventListener gamerotationEventListener;
    private TextView tv;

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
                while (true){
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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try
        {
            this.getSupportActionBar().hide();
        }
        catch (NullPointerException e){}

        ////// BUTTON CODE ///////
        postBtn = findViewById(R.id.postBtn);
        //RequestBody
        buttonStart = (Button) findViewById(R.id.buttonStart);
        buttonStop = (Button) findViewById(R.id.buttonStop);
        webView = (Button) findViewById(R.id.webView);
        buttonStart.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                pulseWidth = 1500;
                pulseWidthY = 1500;
                thread.start();
                //threadY.start();
                buttonStart.setEnabled(false);
                //buttonStop.setEnabled(true);
            }
        });

        buttonStop.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                pulseWidth = 1500;
                pulseWidthY = 1500;
                buttonStop.setEnabled(false);

            }
        });

        webView.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                WebView();
                Intent Intent = new Intent(view.getContext(), WebView.class);
                view.getContext().startActivity(Intent);
            }

        });


        postBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
//POST method
                new AsyncTask<Integer, Void, Void>(){
                    @Override
                    protected Void doInBackground(Integer... params) {
                        try {
                            executeRemoteCommand("pi", "Freddy121314","172.16.1.77", 22);
                            //Toast.makeText(MainActivity.this, result, Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        return null;
                    }
                }.execute(1);
            }

        });

        ////// BUTTON CODE ///////
        ///////// GYROSCOPE CODE
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        gyroscopeSensor = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE_UNCALIBRATED);
        sensorManager.registerListener(gyroscopeEventListener, gyroscopeSensor, SensorManager.SENSOR_DELAY_GAME);

        if (gyroscopeSensor == null) {
            Toast.makeText(this, "The device has no Gyroscope !", Toast.LENGTH_SHORT).show();
            finish();
        }

        gyroscopeEventListener = new SensorEventListener() {
            @Override
            public void onSensorChanged(SensorEvent sensorEvent) {
                //pulseWidth = 0;

                if (sensorEvent.values[0] > 0.05f) { // turn right
                    for (int i = 0; i < 40; i++)
                    {
                        pulseWidth = pulseWidth + 1;
                    }
                    //pulseWidth = pulseWidth + 50;
                }
                if (sensorEvent.values[1] > 0.05f) { // turn up
                    for (int i = 0; i < 40; i++)
                    {
                        pulseWidthY = pulseWidthY - 1;
                    }
                    //pulseWidthY = pulseWidthY - 50;
                }
                if (sensorEvent.values[0] < -0.05f){ // turn left
                    for (int i = 0; i < 40; i++)
                    {
                        pulseWidth = pulseWidth - 1;
                    }
                    //pulseWidth = pulseWidth - 50;
                }
                if (sensorEvent.values[1] < -0.05f) { // turn down
                    for (int i = 0; i < 40; i++)
                    {
                        pulseWidthY = pulseWidthY + 1;
                    }
                    //pulseWidthY = pulseWidthY + 50;
                }


                //if sensor is unreliable, return void
                if (sensorEvent.accuracy == SensorManager.SENSOR_STATUS_UNRELIABLE)
                {
                    return;
                }
                //else it will output the Roll, Pitch and Yawn values
                tv.setText("Orientation X (Roll) :"+ Float.toString(sensorEvent.values[2]) +"\n"+
                        "Orientation Y (Pitch) :"+ Float.toString(sensorEvent.values[1]) +"\n"+// up and down
                        "Orientation Z (Yaw) :"+ Float.toString(sensorEvent.values[0])); // left and right
            }
            @Override
            public void onAccuracyChanged(Sensor sensor, int i) {
            }
        };


        ///////// GYROSCOPE CODE

        textViewProgress = (TextView) findViewById(R.id.textViewX);
        textViewProgress2 = (TextView) findViewById(R.id.textViewY);
        //get the TextView from the layout file
        tv = (TextView) findViewById(R.id.tv);

        seekBar = (SeekBar) findViewById(R.id.seekBar);

        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                pulseWidth = 500+i;
                textViewProgress.setText(""+pulseWidth);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });
        seekBar2 = (SeekBar) findViewById(R.id.seekBar2);
        seekBar2.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar2, int i, boolean b) {
                pulseWidthY = 500+i;
                textViewProgress2.setText(""+pulseWidthY);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar2) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar2) { }
        });

    }

    ///////// GYROSCOPE CODE
    @Override
    protected void onResume(){
        super.onResume();
        sensorManager.registerListener(gyroscopeEventListener, gyroscopeSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }
    protected void onPause(){
        super.onPause();
        sensorManager.unregisterListener(gyroscopeEventListener);
    }
    ///////// GYROSCOPE CODE


    @Override
    protected void onDestroy(){
        pulseWidth = 1500;
        pulseWidthY = 1500;
        super.onDestroy();
    }

    public void WebView()
    {
        Intent Intent = new Intent(this, myWebView.class);
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
    public static String executeRemoteCommand(String username,String password,String hostname,int port)
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
        channelssh.setCommand("python /home/pi/Desktop/servoMove.py");
        //channelssh.setCommand("lsusb > /home/pi/test.txt");
        //channelssh.setCommand("sudo reboot");
        channelssh.connect();
        channelssh.disconnect();


        return baos.toString();
    }

}
