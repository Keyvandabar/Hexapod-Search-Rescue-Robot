
#include <stdio.h>
#include <pigpio.h>

#include "Steering.h"

using namespace std;
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
	    *** This is actually a header file automatically created from a terminal command line prompt that compiles
            the javascript variables into workable C++ variables that the server can extract.
            ***************************************************
            */
JNIEXPORT int JNICALL Java_Steering_turnWheels
(JNIEnv *env, jobject o, jint pin, jint pulseWidth) 
{
    printf("pin = %d, pulseWidth= %d \n", pin, pulseWidth);

    if (gpioInitialise() < 0) 
    {
        printf("failed gpioInitialise \n");
        return 0;
    }	
    gpioServo(pin, pulseWidth);

    return 1;
}

JNIEXPORT int JNICALL Java_Steering_turnWheelsY
(JNIEnv *env, jobject o, jint pinY, jint pulseWidthY) 
{
    printf("pinY = %d, pulseWidthY= %d \n", pinY, pulseWidthY);

    if (gpioInitialise() < 0) 
    {
        printf("failed gpioInitialise \n");
        return 0;
    }	
    gpioServo(pinY, pulseWidthY);

    return 1;
}

