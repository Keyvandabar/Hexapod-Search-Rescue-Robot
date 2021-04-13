The code found within this folder is almost entirely my own other than the required functions stated within the android app development website for setting up the apps basic interface and sensor calls. Some code was required to be adopted as a basis for executing SSH commands on the Raspberry pi as I was not successful with the android documentation itself. In this folder the mainactivity.java was the stepping stone and does not provide nearly any function. The portion written by myself was the WebView.java and merely adopted the communication with the java server on the pi and the SSH terminal commands on button press.
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
