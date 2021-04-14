import RPi.GPIO as GPIO
import serial
import sys
import math
from time import sleep
PI = math.pi#3.1415
cos = math.cos
tan = math.tan
sin = math.sin
atan2 = math.atan2
atan = math.atan
acos = math.acos
PosY = float(0.0)
PosX = float(0.0)
PosZ = float(0.0)
RotZ = float(0.0)
RotX = float(0.0)
RotY = float(0.0)
global FemurAngle_1, TibiaAngle_1, CoxaAngle_1

'''
/*
**********************************************
Title: SSC-32U
Author: Lynxmotion
Date: unknown
Code version: *
Availability: https://www.robotshop.com/media/files/pdf2/lynxmotion_ssc-32u_usb_user_guide.pdf
- The PDF / Documentation provided with the SSC-32U provided decent instructions on how to 
communicate through serial communication from the Raspberry Pi to the SSC-32U. The most useful 
part of this documentation was to discover its ability to send a signal to numerous servo motors 
at the same time.
*** THE PRIMARY FUNCTION OF THIS CODE IS TO ONLY WORK AS A KIND OF LIBRARY TO WORK FROM
***************************************************
*/
/*
**********************************************
Title: Inverse Kinematic Equations (def equ)
Author: TogleFritz
Date: unknown
Code version: *
Availability: https://toglefritz.com/hexapod-inverse-kinematics-equations/
- The inspiration to adopt Inverse Kinematics came from this source and provided 
some insight on how a mathematical approach is the best course of action if the 
robot was to traverse more difficult terrain in furute iterations. 
*** THIS BIT OF CODE SERVES 0 ACTUAL FUNCTION IN THE OPERATION OF THIS PROJECT
***************************************************
The inverse kinematic equations are present in the code but DO NOT provide any actual function to the project and is for future iterations of the project. 
The source for that is https://toglefritz.com/hexapod-inverse-kinematics-equations/
*/
'''

s = serial.Serial('/dev/ttyUSB0', 115200, timeout = 1.0)#9600//38400//115200

def equ(PosX, PosY, PosZ, RotX, RotY, RotZ):# Code from http://toglefritz.com/hexapod-inverse-kinematics-equations/
    BodySideLength = float(171.5)
    CoxaLength = float(76.0)
    FemurLength = float(114.0)
    TibiaLength = float(159.0)
    
    BodyCenterOffset1 = BodySideLength/2
    print('BodyCenterOffset1 : ' +str(float(BodyCenterOffset1)) )
    BodyCenterOffset2 = math.sqrt((math.pow(BodySideLength,2)) - (math.pow(BodyCenterOffset1,2)))
    print('BodyCenterOffset2 : ' +str(float(BodyCenterOffset2)) )
    print('----------------------------------')
    BodyCenterOffsetX_1 = BodyCenterOffset1
    print('BodyCenterOffsetX_1 : ' +str(float(BodyCenterOffsetX_1)) )
    BodyCenterOffsetX_2	= BodySideLength
    print('BodyCenterOffsetX_2 : ' +str(float(BodyCenterOffsetX_2)) )
    BodyCenterOffsetX_3 = BodyCenterOffset1
    print('BodyCenterOffsetX_3 : ' +str(float(BodyCenterOffsetX_3)) )
    BodyCenterOffsetX_4 = -BodyCenterOffset1
    print('BodyCenterOffsetX_4 : ' +str(float(BodyCenterOffsetX_4)) )
    BodyCenterOffsetX_5	= -BodySideLength
    print('BodyCenterOffsetX_5 : ' +str(float(BodyCenterOffsetX_5)) )
    BodyCenterOffsetX_6 = -BodyCenterOffset1
    print('BodyCenterOffsetX_6 : ' +str(float(BodyCenterOffsetX_6)) )
    print('----------------------------------')
    BodyCenterOffsetY_1 = BodyCenterOffset2
    print('BodyCenterOffsetY_1: ' +str(float(BodyCenterOffsetY_1)) )
    BodyCenterOffsetY_2 = 0
    print('BodyCenterOffsetY_2: ' +str(float(BodyCenterOffsetY_2)) )
    BodyCenterOffsetY_3 = -BodyCenterOffset2
    print('BodyCenterOffsetY_3: ' +str(float(BodyCenterOffsetY_3)) )
    BodyCenterOffsetY_4 = -BodyCenterOffset2
    print('BodyCenterOffsetY_4: ' +str(float(BodyCenterOffsetY_4)) )
    BodyCenterOffsetY_5 = 0
    print('BodyCenterOffsetY_5: ' +str(float(BodyCenterOffsetY_5)) )
    BodyCenterOffsetY_6 = BodyCenterOffset2
    print('BodyCenterOffsetY_6: ' +str(float(BodyCenterOffsetY_6)) )
    print('----------------------------------')
    #leg 1 - 8/9/10
    FeetPosX_1 = cos(60/180*PI)*(CoxaLength + FemurLength)
    FeetPosZ_1 = TibiaLength
    FeetPosY_1 = sin(60/180*PI)*(CoxaLength + FemurLength)
    print('FeetPosX_1 : ' +str(float(FeetPosX_1)) )
    print('FeetPosZ_1 : ' +str(float(FeetPosZ_1)) )
    print('FeetPosY_1 : ' +str(float(FeetPosY_1)) )
    print('----------------------------------')
    #leg 2 - 4/5/6
    FeetPosX_2 = CoxaLength + FemurLength
    FeetPosZ_2 = TibiaLength
    FeetPosY_2 = 0
    print('FeetPosX_2 : ' +str(float(FeetPosX_2)) )
    print('FeetPosZ_2 : ' +str(float(FeetPosZ_2)) )
    print('FeetPosY_2 : ' +str(float(FeetPosY_2)) )
    print('----------------------------------')
    #leg 3 - 0/1/2
    FeetPosX_3 = cos(60/180*PI)*(CoxaLength + FemurLength)
    FeetPosZ_3	= TibiaLength
    FeetPosY_3 = sin(-60/180*PI)*(CoxaLength + FemurLength)
    print('FeetPosX_3 : ' +str(float(FeetPosX_3)) )
    print('FeetPosZ_3 : ' +str(float(FeetPosZ_3)) )
    print('FeetPosY_3 : ' +str(float(FeetPosY_3)) )
    print('----------------------------------')
    #leg 4 - 24/25/26
    FeetPosX_4 = -cos(60/180*PI)*(CoxaLength + FemurLength)
    FeetPosZ_4 = TibiaLength
    FeetPosY_4 = math.sin(-60/180*PI)*(CoxaLength + FemurLength)
    print('FeetPosX_4 : ' +str(float(FeetPosX_4)) )
    print('FeetPosZ_4 : ' +str(float(FeetPosZ_4)) )
    print('FeetPosY_4 : ' +str(float(FeetPosY_4)) )
    print('----------------------------------')
    #leg 5 = 20/21/22
    FeetPosX_5 = -(CoxaLength + FemurLength)
    FeetPosZ_5 = TibiaLength
    FeetPosY_5 = 0
    print('FeetPosX_5 : ' +str(float(FeetPosX_5)) )
    print('FeetPosZ_5 : ' +str(float(FeetPosZ_5)) )
    print('FeetPosY_5 : ' +str(float(FeetPosY_5)) )
    print('----------------------------------')
    #leg 6 = 16/17/18
    FeetPosX_6 = -cos(60/180*PI)*(CoxaLength + FemurLength)
    FeetPosZ_6 = TibiaLength
    FeetPosY_6 = sin(60/180*PI)*(CoxaLength + FemurLength)
    print('FeetPosX_6 : ' +str(float(FeetPosX_6)) )
    print('FeetPosZ_6 : ' +str(float(FeetPosZ_6)) )
    print('FeetPosY_6 : ' +str(float(FeetPosY_6)) )
    print('----------------------------------')
    #Body Inverse Kinematics
    #leg 1 - 8/9/10
    TotalY_1 = FeetPosY_1 + BodyCenterOffsetY_1 + PosY
    TotalX_1 = FeetPosX_1 + BodyCenterOffsetX_1 + PosX
    DistBodyCenterFeet_1 = math.sqrt(math.pow(TotalY_1,2) + math.pow(TotalX_1,2))
    AngleBodyCenterX_1 = PI/2 - atan2(TotalX_1, TotalY_1)
    RollZ_1 = tan(RotZ * PI/180) * TotalX_1
    PitchZ_1 = tan(RotX * PI/180) * TotalY_1
    BodyIKX_1 = cos(AngleBodyCenterX_1 + (RotY * PI/180)) * DistBodyCenterFeet_1 - TotalX_1
    BodyIKY_1 = sin(AngleBodyCenterX_1 + (RotY  * PI/180)) * DistBodyCenterFeet_1 - TotalY_1
    BodyIKZ_1 = RollZ_1 + PitchZ_1
    print('TotalY_1 : ' +str(float(TotalY_1)) )
    print('TotalX_1 : ' +str(float(TotalX_1)) )
    print('DistBodyCenterFeet_1 : ' +str(float(DistBodyCenterFeet_1)) )
    print('AngleBodyCenterX_1 : ' +str(float(AngleBodyCenterX_1)) )
    print('RollZ_1 : ' +str(float(RollZ_1)) )
    print('PitchZ_1 : ' +str(float(PitchZ_1)) )
    print('BodyIKX_1 : ' +str(float(BodyIKX_1)) )
    print('BodyIKY_1 : ' +str(float(BodyIKY_1)) )
    print('BodyIKZ_1 : ' +str(float(BodyIKZ_1)) )
    print('----------------------------------')
    #leg 2 - 4/5/6
    TotalY_2 = FeetPosY_2 + BodyCenterOffsetY_2 + PosY
    TotalX_2 = FeetPosX_2 + BodyCenterOffsetX_2 + PosX
    DistBodyCenterFeet_2 = math.sqrt(math.pow(TotalY_2,2) + math.pow(TotalX_2,2))
    AngleBodyCenterX_2 = PI/2 - atan2(TotalX_2, TotalY_2)
    RollZ_2 = tan(RotZ * PI/180) * TotalX_2
    PitchZ_2 = tan(RotX * PI/180) * TotalY_2
    BodyIKX_2 = cos(AngleBodyCenterX_2 + (RotY * PI/180)) * DistBodyCenterFeet_2 - TotalX_2
    BodyIKY_2 = (sin(AngleBodyCenterX_1 + (RotY  * PI/180)) * DistBodyCenterFeet_1) - TotalY_1
    BodyIKZ_2 = RollZ_2 + PitchZ_2
    #leg 3 - 0/1/2
    TotalY_3 = FeetPosY_3 + BodyCenterOffsetY_3 + PosY
    TotalX_3 = FeetPosX_3 + BodyCenterOffsetX_3 + PosX
    DistBodyCenterFeet_3 = math.sqrt(math.pow(TotalY_3,2) + math.pow(TotalX_3,2))
    AngleBodyCenterX_3 = PI/2 - atan2(TotalX_3, TotalY_3)
    RollZ_3 = tan(RotZ * PI/180) * TotalX_3
    PitchZ_3 = tan(RotX * PI/180) * TotalY_3
    BodyIKX_3 = cos(AngleBodyCenterX_3 + (RotY * PI/180)) * DistBodyCenterFeet_3 - TotalX_3
    BodyIKY_3 = (sin(AngleBodyCenterX_3 + (RotY  * PI/180)) * DistBodyCenterFeet_3) - TotalY_3
    BodyIKZ_3 = RollZ_3 + PitchZ_3
    #leg 4 - 24/25/26
    TotalY_4 = FeetPosY_4 + BodyCenterOffsetY_4 + PosY
    TotalX_4 = FeetPosX_4 + BodyCenterOffsetX_4 + PosX
    DistBodyCenterFeet_4 = math.sqrt(math.pow(TotalY_4,2) + math.pow(TotalX_4,2))
    AngleBodyCenterX_4 = PI/2 - atan2(TotalX_4, TotalY_4)
    RollZ_4 = tan(RotZ * PI/180) * TotalX_4
    PitchZ_4 = tan(RotX * PI/180) * TotalY_4
    BodyIKX_4 = cos(AngleBodyCenterX_4 + (RotY * PI/180)) * DistBodyCenterFeet_4 - TotalX_4
    BodyIKY_4 = (sin(AngleBodyCenterX_4 + (RotY  * PI/180)) * DistBodyCenterFeet_4) - TotalY_4
    BodyIKZ_4 = RollZ_4 + PitchZ_4
    #leg 5 - 20/21/22
    TotalY_5 = FeetPosY_5 + BodyCenterOffsetY_5 + PosY
    TotalX_5 = FeetPosX_5 + BodyCenterOffsetX_5 + PosX
    DistBodyCenterFeet_5 = math.sqrt(math.pow(TotalY_5,2) + math.pow(TotalX_5,2))
    AngleBodyCenterX_5 = PI/2 - atan2(TotalX_5, TotalY_5)
    RollZ_5 = tan(RotZ * PI/180) * TotalX_5
    PitchZ_5 = tan(RotX * PI/180) * TotalY_5
    BodyIKX_5 = cos(AngleBodyCenterX_5 + (RotY * PI/180)) * DistBodyCenterFeet_5 - TotalX_5
    BodyIKY_5 = (sin(AngleBodyCenterX_5 + (RotY  * PI/180)) * DistBodyCenterFeet_5) - TotalY_5
    BodyIKZ_5 = RollZ_5 + PitchZ_5
    #leg 6 - 16/17/18
    TotalY_6 = FeetPosY_6 + BodyCenterOffsetY_6 + PosY
    TotalX_6 = FeetPosX_6 + BodyCenterOffsetX_6 + PosX
    DistBodyCenterFeet_6 = math.sqrt(math.pow(TotalY_6,2) + math.pow(TotalX_6,2))
    AngleBodyCenterX_6 = PI/2 - atan2(TotalX_6, TotalY_6)
    RollZ_6 = tan(RotZ * PI/180) * TotalX_6
    PitchZ_6 = tan(RotX * PI/180) * TotalY_6
    BodyIKX_6 = cos(AngleBodyCenterX_6 + (RotY * PI/180)) * DistBodyCenterFeet_6 - TotalX_6
    BodyIKY_6 = (sin(AngleBodyCenterX_6 + (RotY  * PI/180)) * DistBodyCenterFeet_6) - TotalY_6
    BodyIKZ_6 = RollZ_6 + PitchZ_6
    #Leg Inverse Kinematics
    #leg 1 - 8/9/10
    NewPosX_1 = FeetPosX_1 + PosX +  BodyIKX_1
    NewPosZ_1 = FeetPosZ_1 + PosZ + BodyIKZ_1
    NewPosY_1 = FeetPosY_1 + PosY + BodyIKY_1
    CoxaFeetDist_1 = math.sqrt(math.pow(NewPosX_1,2)   + math.pow(NewPosY_1,2))
    IKSW_1 = math.sqrt(math.pow((CoxaFeetDist_1 - CoxaLength ) ,2) + math.pow(NewPosZ_1,2))
    IKA1_1 = atan((CoxaFeetDist_1 - CoxaLength)/NewPosZ_1)
    IKA2_1 = acos((math.pow(TibiaLength,2) - math.pow(FemurLength,2) - math.pow(IKSW_1,2))/(-2 * IKSW_1 *  FemurLength))
    TAngle_1 = acos((math.pow(IKSW_1,2) - math.pow(TibiaLength,2) - math.pow(FemurLength,2))/(-2 * FemurLength * TibiaLength))
    IKTibiaAngle_1 = 90 - TAngle_1 * 180/PI
    IKFemurAngle_1 = 90 - (IKA1_1 + IKA2_1) * 180/PI
    IKCoxaAngle_1 = 90 - atan2(NewPosX_1, NewPosY_1) * 180 / PI
    print('NewPosX_1 : ' +str(float(NewPosX_1)) )
    print('NewPosZ_1 : ' +str(float(NewPosZ_1)) )
    print('NewPosY_1 : ' +str(float(NewPosY_1)) )
    print('CoxaFeetDist_1 : ' +str(float(CoxaFeetDist_1)) )
    print('IKSW_1 : ' +str(float(IKSW_1)) )
    print('IKA1_1 : ' +str(float(IKA1_1)) )
    print('IKA2_1 : ' +str(float(IKA2_1)) )
    print('TAngle_1 : ' +str(float(TAngle_1)) )
    print('IKTibiaAngle_1 : ' +str(float(IKTibiaAngle_1)) )
    print('IKFemurAngle_1 : ' +str(float(IKFemurAngle_1)) )
    print('IKCoxaAngle_1 : ' +str(float(IKCoxaAngle_1)) )
    print('-----------------')
    #leg 2 - 4/5/6
    NewPosX_2 = FeetPosX_2 + PosX +  BodyIKX_2
    NewPosZ_2 = FeetPosZ_2 + PosZ + BodyIKZ_2
    NewPosY_2 = FeetPosY_2 + PosY + BodyIKY_2
    CoxaFeetDist_2 = math.sqrt(math.pow(NewPosX_2,2)   + math.pow(NewPosY_2,2))
    IKSW_2 = math.sqrt((math.pow((CoxaFeetDist_2 - CoxaLength ) ,2) + math.pow(NewPosZ_2,2)))
    IKA1_2 = atan((CoxaFeetDist_2 - CoxaLength)/NewPosZ_2)
    IKA2_2 = acos(((math.pow(TibiaLength,2)) - (math.pow(FemurLength,2)) - (math.pow(IKSW_2,2)))/(-2 * IKSW_2 *  FemurLength))
    TAngle_2 = acos((math.pow(IKSW_2,2) - math.pow(TibiaLength,2) - math.pow(FemurLength,2))/(-2 * FemurLength * TibiaLength))
    IKTibiaAngle_2 = 90 - TAngle_2 * 180/PI
    IKFemurAngle_2 = 90 - (IKA1_2 + IKA2_2) * 180/PI
    IKCoxaAngle_2 = 90 - atan2(NewPosX_2, NewPosY_2) * 180/PI
    print('NewPosX_2 : ' +str(float(NewPosX_2)) )
    print('NewPosZ_2 : ' +str(float(NewPosZ_2)) )
    print('NewPosY_2 : ' +str(float(NewPosY_2)) )
    print('CoxaFeetDist_2 : ' +str(float(CoxaFeetDist_2)) )
    print('IKSW_2 : ' +str(float(IKSW_2)) )
    print('IKA1_2 : ' +str(float(IKA1_2)) )
    print('IKA2_2 : ' +str(float(IKA2_2)) )
    print('TAngle_2 : ' +str(float(TAngle_2)) )
    print('IKTibiaAngle_2 : ' +str(float(IKTibiaAngle_2)) )
    print('IKFemurAngle_2 : ' +str(float(IKFemurAngle_2)) )
    print('IKCoxaAngle_2 : ' +str(float(IKCoxaAngle_2)) )
    print('-----------------')
    #leg 3 - 0/1/2
    NewPosX_3 = FeetPosX_3 + PosX +  BodyIKX_3
    NewPosZ_3 = FeetPosZ_3 + PosZ + BodyIKZ_3
    NewPosY_3 = FeetPosY_3 + PosY + BodyIKY_3
    CoxaFeetDist_3 = math.sqrt(math.pow(NewPosX_3,2)   + math.pow(NewPosY_3,2))
    IKSW_3 = math.sqrt(math.pow((CoxaFeetDist_3 - CoxaLength ) ,2) + math.pow(NewPosZ_3,2))
    IKA1_3 = atan((CoxaFeetDist_3 - CoxaLength)/NewPosZ_3)
    IKA2_3 = acos((math.pow(TibiaLength,2) - math.pow(FemurLength,2) - math.pow(IKSW_3,2))/(-2 * IKSW_3 *  FemurLength))
    TAngle_3 = acos((math.pow(IKSW_3,2) - math.pow(TibiaLength,2) - math.pow(FemurLength,2))/(-2 * FemurLength * TibiaLength))
    IKTibiaAngle_3 = 90 - TAngle_3 * 180/PI
    IKFemurAngle_3 = 90 - (IKA1_3 + IKA2_3) * 180/PI
    IKCoxaAngle_3 = 90 - atan2(NewPosX_3, NewPosY_3) * 180/PI
    #leg 4 - 24/25/26
    NewPosX_4 = FeetPosX_4 + PosX +  BodyIKX_4
    NewPosZ_4 = FeetPosZ_4 + PosZ + BodyIKZ_4
    NewPosY_4 = FeetPosY_4 + PosY + BodyIKY_4
    CoxaFeetDist_4 = math.sqrt(math.pow(NewPosX_4,2)   + math.pow(NewPosY_4,2))
    IKSW_4 = math.sqrt(math.pow((CoxaFeetDist_4 - CoxaLength ) ,2) + math.pow(NewPosZ_4,2))
    IKA1_4 = atan((CoxaFeetDist_4 - CoxaLength)/NewPosZ_4)
    IKA2_4 = acos((math.pow(TibiaLength,2) - math.pow(FemurLength,2) - math.pow(IKSW_4,2))/(-2 * IKSW_4 *  FemurLength))
    TAngle_4 = acos((math.pow(IKSW_4,2) - math.pow(TibiaLength,2) - math.pow(FemurLength,2))/(-2 * FemurLength * TibiaLength))
    IKTibiaAngle_4 = 90 - TAngle_4 * 180/PI
    IKFemurAngle_4 = 90 - (IKA1_4 + IKA2_4) * 180/PI
    IKCoxaAngle_4 = 90 - atan2(NewPosX_4, NewPosY_4) * 180/PI
    #leg 5 - 20/21/22
    NewPosX_5 = FeetPosX_5 + PosX +  BodyIKX_5
    NewPosZ_5 = FeetPosZ_5 + PosZ + BodyIKZ_5
    NewPosY_5 = FeetPosY_5 + PosY + BodyIKY_5
    CoxaFeetDist_5 = math.sqrt(math.pow(NewPosX_5,2)   + math.pow(NewPosY_5,2))
    IKSW_5 = math.sqrt(math.pow((CoxaFeetDist_5 - CoxaLength ) ,2) + math.pow(NewPosZ_5,2))
    IKA1_5 = atan((CoxaFeetDist_5 - CoxaLength)/NewPosZ_5)
    IKA2_5 = acos((math.pow(TibiaLength,2) - math.pow(FemurLength,2) - math.pow(IKSW_5,2))/(-2 * IKSW_5 *  FemurLength))
    TAngle_5 = acos((math.pow(IKSW_5,2) - math.pow(TibiaLength,2) - math.pow(FemurLength,2))/(-2 * FemurLength * TibiaLength))
    IKTibiaAngle_5 = 90 - TAngle_5 * 180/PI
    IKFemurAngle_5 = 90 - (IKA1_5 + IKA2_5) * 180/PI
    IKCoxaAngle_5 = 90 - atan2(NewPosX_5, NewPosY_5) * 180/PI
    #leg 6 - 16/17/18
    NewPosX_6 = FeetPosX_6 + PosX +  BodyIKX_6
    NewPosZ_6 = FeetPosZ_6 + PosZ + BodyIKZ_6
    NewPosY_6 = FeetPosY_6 + PosY + BodyIKY_6
    CoxaFeetDist_6 = math.sqrt(math.pow(NewPosX_6,2)   + math.pow(NewPosY_6,2))
    IKSW_6 = math.sqrt(math.pow((CoxaFeetDist_6 - CoxaLength ) ,2) + math.pow(NewPosZ_6,2))
    IKA1_6 = atan((CoxaFeetDist_6 - CoxaLength)/NewPosZ_6)
    IKA2_6 = acos((math.pow(TibiaLength,2) - math.pow(FemurLength,2) - math.pow(IKSW_6,2))/(-2 * IKSW_6 *  FemurLength))
    TAngle_6 = acos((math.pow(IKSW_6,2) - math.pow(TibiaLength,2) - math.pow(FemurLength,2))/(-2 * FemurLength * TibiaLength))
    IKTibiaAngle_6 = 90 - TAngle_6 * 180/PI
    IKFemurAngle_6 = 90 - (IKA1_6 + IKA2_6) * 180/PI
    IKCoxaAngle_6 = 90 - atan2(NewPosX_6, NewPosY_6) * 180/PI
    #servo Angles
    #leg 1 - 8/9/10
    #nonlocal CoxaAngle_1, FemurAngle_1, TibiaAngle_1
    global CoxaAngle_1
    CoxaAngle_1 = (IKCoxaAngle_1 - 60) * 12 + 1500
    global FemurAngle_1
    FemurAngle_1 = IKFemurAngle_1 * 12 + 1500
    global TibiaAngle_1
    TibiaAngle_1 = IKTibiaAngle_1 * 12 + 1500
    #leg 2 - 4/5/6
    global CoxaAngle_2 
    CoxaAngle_2 = IKCoxaAngle_2 * 12 + 1500
    global FemurAngle_2
    FemurAngle_2	= IKFemurAngle_2 * 12 + 1500
    global TibiaAngle_2
    TibiaAngle_2 = IKTibiaAngle_2 * 12 + 1500
    #leg 3 - 0/1/2
    global CoxaAngle_3
    CoxaAngle_3 = (IKCoxaAngle_3 + 60) * 12 + 1500
    global FemurAngle_3
    FemurAngle_3 = IKFemurAngle_3 * 12 + 1500
    global TibiaAngle_3
    TibiaAngle_3 = IKTibiaAngle_3 * 12 + 1500
    #leg 4 - 24/25/26
    global CoxaAngle_4
    CoxaAngle_4 = (IKCoxaAngle_4 - 240) * 12 + 1500
    global FemurAngle_4
    FemurAngle_4 = IKFemurAngle_4 * 12 + 1500
    global TibiaAngle_4
    TibiaAngle_4 = IKTibiaAngle_4 * 12 + 1500
    #leg 5 - 20/21/22
    global CoxaAngle_5
    CoxaAngle_5 = (IKCoxaAngle_5 - 180) * 12 + 1500
    global FemurAngle_5
    FemurAngle_5 = IKFemurAngle_5 * 12 + 1500
    global TibiaAngle_5
    TibiaAngle_5 = IKTibiaAngle_5 * 12 + 1500
    #leg 6 - 16/17/18
    global CoxaAngle_6
    CoxaAngle_6 = (IKCoxaAngle_6 - 120) * 12 + 1500
    global FemurAngle_6
    FemurAngle_6 = IKFemurAngle_6 * 12 + 1500
    global TibiaAngle_6
    TibiaAngle_6 = IKTibiaAngle_6 * 12 + 1500
    print ( "CoxaAngle_1 : " + str(float(CoxaAngle_1)) )
    #print ( "CoxaAngle_1 PWM : " + str(float((CoxaAngle_1 * 9) + 1500)) )
    print ( "FemurAngle_1 : " + str(float(FemurAngle_1)) )
    print ( "TibiaAngle_1 : " + str(float(TibiaAngle_1)) )
    print('-----------------')
    print ( "CoxaAngle_2 : " + str(float(CoxaAngle_2)) )
    print ( "FemurAngle_2 : " + str(float(FemurAngle_2)) )
    print ( "TibiaAngle_2 : " + str(float(TibiaAngle_2)) )
    print('-----------------')
    print ( "CoxaAngle_3 : " + str(float(CoxaAngle_3)) )
    print ( "FemurAngle_3 : " + str(float(FemurAngle_3)) )
    print ( "TibiaAngle_3 : " + str(float(TibiaAngle_3)) )
    print('-----------------')
    print ( "CoxaAngle_4 : " + str(float(CoxaAngle_4)) )
    print ( "FemurAngle_4 : " + str(float(FemurAngle_4)) )
    print ( "TibiaAngle_4 : " + str(float(TibiaAngle_4)) )
    print('-----------------')
    print ( "CoxaAngle_5 : " + str(float(CoxaAngle_5)) )
    print ( "FemurAngle_5 : " + str(float(FemurAngle_5)) )
    print ( "TibiaAngle_5 : " + str(float(TibiaAngle_5)) )
    print('-----------------')
    print ( "CoxaAngle_6 : " + str(float(CoxaAngle_6)) )
    print ( "FemurAngle_6 : " + str(float(FemurAngle_6)) )
    print ( "TibiaAngle_6 : " + str(float(TibiaAngle_6)) )
    print('-----------------')

def offset():# offset the servos
    s.write("#0 PO -100\r".encode())#br leg
    s.write("#2 PO -100\r".encode())#br body
    s.write("#4 PO -100\r".encode())#cr leg
    s.write("#6 PO -100\r".encode())#cr body
    #s.write("#16 PO 100\r".encode())#fl leg
    s.write("#20 PO 100\r".encode())#cl leg
    s.write("#22 PO -100\r".encode())#cl body
    s.write("#24 PO 100\r".encode())#bl leg
    s.write("#26 PO 100\r".encode())#bl body
def brCenter(): #Back right center
    s.write("#0 P1400 #1 P1500 #2 P1500 \r".encode())# BACK RIGHT LEG=1500 FEMUR=1500 BODY=1400
    
def crCenter(): #Center right center
    s.write("#4 P1500 #5 P1500 #6 P1500 \r".encode())# BACK RIGHT LEG=1500 FEMUR=1500 BODY=1400
    
def frCenter():#Front Right Center
    s.write("#8 P1500 #9 P1500 #10 P1600 \r".encode())# FRONT RIGHT LEG=1600 FEMUR=1500 BODY=1500
    
def flCenter():#Front left leg Center
    s.write("#16 P1600 #17 P1500 #18 P1500 \r".encode())# Front LEFT LEG=1500 FEMUR=1500 BODY=1500
    
def blCenter():#Back left leg Center
    s.write("#24 P1600 #25 P1500 #26 P1600 \r".encode())# Back LEFT LEG=1400 FEMUR=1500 BODY=1500

def clCenter():#Center left leg Center
    s.write("#20 P1600 #21 P1500 #22 P1500 \r".encode())# CENTER LEFT LEG=1500 FEMUR=1500 BODY=1400

def frForward():#Front Right leg forward
    
    s.write("#9 P1300 #8 P1700 #10 P1250 \r".encode())# T2000 = 2s to moveFRONT RIGHT FEMUR MAX UPWARD = 2150 # FRONT RIGHT LEG MAX OUTWARD = 1250 # FRONT RIGHT BODY MAX FORWARD = 2150                
    #s.write(("#9 P" +str(FemurAngle_1) + "#8 P" +str(TibiaAngle_1) + "#10 P"+str(CoxaAngle_1) + " \r").encode())# T2000 = 2s to moveFRONT RIGHT FEMUR MAX UPWARD = 2150 # FRONT RIGHT LEG MAX OUTWARD = 1250 # FRONT RIGHT BODY MAX FORWARD = 2150                
    #print ( "CoxaAngle_1 : " + str(CoxaAngle_1) )
    #print ( "CoxaAngle_1 PWM : " + str(float((CoxaAngle_1 * 9) + 1500)) )
    #print ( "FemurAngle_1 : " + str(float(FemurAngle_1)) )
    #print ( "TibiaAngle_1 : " + str(float(TibiaAngle_1)) )
    #print('-----------------')
    sleep(1)
    #s.write("#8 P1600 #9 P1500 \r".encode())
def brForward():#Back right leg forward
    s.write("#1 P1300 #0 P1700 #2 P1250 \r".encode())# BACK RIGHT FEMUR MAX UPWARD = 2150 # BACK RIGHT LEG MAX OUTWARD = 1250 # BACK RIGHT BODY MAX FORWARD = 2150                
    sleep(1)
    #s.write("#0 P1500 #1 P1500 \r".encode())
def clForward():#Center left leg forward
    s.write("#21 P1700 #20 P1300 #22 P1750 \r".encode()) # Move forward        
    sleep(1)
    #s.write("#20 P1500 #21 P1500 \r".encode()) #Place leg/femur to original position
def flForward():#Front left leg forward
    s.write("#17 P1700 #16 P1300 #18 P1750 \r".encode()) # Move forward        
    sleep(1)
    s.write("#16 P1500 #17 P1500 \r".encode()) #Place leg/femur to original position
def blForward():#Back left leg forward
    s.write("#25 P1700 #24 P1300 #26 P1750 \r".encode()) # Move forward        
    sleep(1)
    s.write("#24 P1500 #25 P1500 \r".encode()) #Place leg/femur to original position
def crForward():#Center right leg forward
    s.write("#5 P1300 #4 P1700 #6 P1000 \r".encode())# BACK RIGHT FEMUR MAX UPWARD = 2150 # BACK RIGHT LEG MAX OUTWARD = 1250 # BACK RIGHT BODY MAX FORWARD = 2150                
    sleep(1)
    s.write("#4 P1500 #5 P1500 \r".encode())
    

    
    
def center():#Tripod B (Back right + Center left + Front Right -- 0/1/2 + 20/21/22 + 8/9/10)
    clCenter()
    brCenter()
    frCenter()
    crCenter()
    blCenter()
    flCenter()    
def taForward():#Tripod B (Back right + Center left + Front Right -- 0/1/2 + 20/21/22 + 8/9/10)
    crForward()
    flForward()
    blForward()
    
def tbForward():#Tripod B (Back right + Center left + Front Right -- 0/1/2 + 20/21/22 + 8/9/10)
    clForward()
    frForward()
    brForward()
def tripodMove():
    #taForward()#forward and down
    #ta forward and up
    s.write("#5 P1300 #4 P1700 #6 P1250 \r".encode())#cr forward
    s.write("#17 P1700 #16 P1300 #18 P1900 \r".encode())#fl forward
    s.write("#25 P1700 #24 P1200 #26 P1800\r".encode())#bl Forward
    sleep(0.1)
    #ta down
    s.write("#16 P1600 #17 P1500 #24 P1600 #25 P1500 #4 P1500 #5 P1500\r".encode())
    sleep(0.1)
    #tbOnly forward and up
    s.write("#9 P1300 #8 P1700 #10 P1200 \r".encode())#fr forward
    s.write("#1 P1200 #0 P1800 #2 P1200 \r".encode())#br Forward
    s.write("#21 P1700 #20 P1300 #22 P1750\r".encode())#cl Forward
    sleep(0.1)
    #move ta push
    s.write("#4 P1500 #5 P1500 #6 P1650 \r".encode())#cr push
    s.write("#16 P1600 #17 P1500 #18 P1350 \r".encode())#fl push
    s.write("#24 P1600 #25 P1500 #26 P1450 \r".encode())#bl push
    sleep(0.1)
    #tbDown
    s.write("#8 P1600 #9 P1500 #0 P1400 #1 P1500 #20 P1600 #21 P1500 \r".encode())
    sleep(0.1)
    #ta forward and up
    s.write("#5 P1300 #4 P1700 #6 P1250 \r".encode())#cr forward
    s.write("#17 P1700 #16 P1300 #18 P1900 \r".encode())#fl forward
    s.write("#25 P1700 #24 P1200 #26 P1800\r".encode())#bl Forward
    sleep(0.1)
    #move tb push
    s.write("#20 P1600 #21 P1500 #22 P1350 \r".encode())#cl push
    s.write("#0 P1400 #1 P1500 #2 P1650 \r".encode())#br push
    s.write("#8 P1500 #9 P1500 #10 P1750 \r".encode())#fr push
    sleep(0.1)
    #ta down
    s.write("#16 P1600 #17 P1500 #24 P1600 #25 P1500 #4 P1500 #5 P1500\r".encode())
    sleep(0.1)
    center()
    
def startup():
    s.write("#1 P1000 #5 P1000 #9 P1000 #17 P2000 #21 P2000 #25 P2000 T2000\r".encode())#max femurs up
    sleep(0.5)
    s.write("#0 P1000 #4 P1000 #8 P1000 #16 P2000 #20 P2000 #24 P2000 T2000\r".encode())#max legs in
    sleep(0.5)
    center()
    sleep(0.1)
    offset()
    sleep(0.1)
    adjustLegs()

def adjustLegs():
    s.write("#1 P1250 #0 P2000 \r".encode())#adjust each leg
    sleep(0.2)
    s.write("#1 P1500 #0 P1500 \r".encode())#adjust each leg
    s.write("#17 P1750 #16 P1250 \r".encode())#adjust each leg
    sleep(0.2)
    s.write("#17 P1500 #16 P1500 \r".encode())#adjust each leg

    s.write("#9 P1250 #8 P1750 \r".encode())#adjust each leg
    sleep(0.2)
    s.write("#9 P1500 #8 P1600 \r".encode())#adjust each leg
    s.write("#25 P1750 #24 P1250 \r".encode())#adjust each leg
    sleep(0.2)
    s.write("#25 P1500 #24 P1400 \r".encode())#adjust each leg

    s.write("#21 P1750 #20 P1250 \r".encode())#adjust each leg
    sleep(0.2)
    s.write("#21 P1500 #20 P1500 \r".encode())#adjust each leg
    s.write("#5 P1250 #4 P1750 \r".encode())#adjust each leg
    sleep(0.2)
    s.write("#5 P1500 #4 P1500 \r".encode())#adjust each leg    
    
def powerdown():
    center()
    sleep(1)
    s.write("#1 P1000 #5 P1000 #9 P1000 #17 P2000 #21 P2000 #25 P2000 T2000\r".encode())#max femurs up
    sleep(1)
    s.write("#0 P1000 #4 P1000 #8 P1000 #16 P2000 #20 P2000 #24 P2000 T2000\r".encode())#max legs in
    
    
def shiftForward():
    s.write("#2 P1300 #6 P1300 #10 P1300 #18 P1700 #22 P1700 #26 P1700 \r".encode())
def moveForward():
    #shiftForward()
    #sleep(1)
    
    frForward()
    clForward()
    #sleep(1)
    brForward()
    flForward()
    #sleep(1)
    crForward()
    blForward()
    #sleep(1)
    center()
    #sleep(1)
    adjustLegs()
    

startup()
sleep(1)
center()
sleep(1)
#sleep(5)
s.close()
'''
i = 1
for i in range(10):
    tripodMove()
    sleep(0.2)
  '''  
'''
tripodMove()
sleep(0.2)
tripodMove()
sleep(0.2)
tripodMove()
sleep(0.2)
tripodMove()
sleep(0.2)
tripodMove()
sleep(1)
tripodMove()
sleep(1)
tripodMove()
'''
#center()
'''
sleep(5)
sleep(1)
powerdown()
'''

###def equ(PosX, PosY, PosZ, RotX, RotY, RotZ):###
#equ(0,50,0,0,0,0)
##THIS WORKS##
'''
s.write(("#9 P" +str(FemurAngle_1) + "#8 P" +str(TibiaAngle_1) + "#10 P"+str(CoxaAngle_1) + " \r").encode())# T2000 = 2s to moveFRONT RIGHT FEMUR MAX UPWARD = 2150 # FRONT RIGHT LEG MAX OUTWARD = 1250 # FRONT RIGHT BODY MAX FORWARD = 2150                
s.write(("#5 P" +str(FemurAngle_2) + "#4 P" +str(TibiaAngle_2) + "#6 P"+str(CoxaAngle_2) + " \r").encode())
s.write(("#1 P" +str(FemurAngle_3) + "#0 P" +str(TibiaAngle_3) + "#2 P"+str(CoxaAngle_3) + " \r").encode())
s.write(("#25 P" +str(FemurAngle_4) + "#24 P" +str(TibiaAngle_4) + "#26 P"+str(CoxaAngle_4) + " \r").encode())
s.write(("#21 P" +str(FemurAngle_5) + "#20 P" +str(TibiaAngle_5) + "#22 P"+str(CoxaAngle_5) + " \r").encode())
s.write(("#17 P" +str(FemurAngle_6) + "#16 P" +str(TibiaAngle_6) + "#18 P"+str(CoxaAngle_6) + " \r").encode())
print ( "CoxaAngle_1 : " + str(float(CoxaAngle_1)) )
print ( "FemurAngle_1 : " + str(float(FemurAngle_1)) )
print ( "TibiaAngle_1 : " + str(float(TibiaAngle_1)) )
print('-----------------')
print ( "CoxaAngle_2 : " + str(float(CoxaAngle_2)) )
print ( "FemurAngle_2 : " + str(float(FemurAngle_2)) )
print ( "TibiaAngle_2 : " + str(float(TibiaAngle_2)) )
print('-----------------')
print ( "CoxaAngle_3 : " + str(float(CoxaAngle_3)) )
print ( "FemurAngle_3 : " + str(float(FemurAngle_3)) )
print ( "TibiaAngle_3 : " + str(float(TibiaAngle_3)) )
print('-----------------')
print ( "CoxaAngle_4 : " + str(float(CoxaAngle_4)) )
print ( "FemurAngle_4 : " + str(float(FemurAngle_4)) )
print ( "TibiaAngle_4 : " + str(float(TibiaAngle_4)) )
print('-----------------')
print ( "CoxaAngle_5 : " + str(float(CoxaAngle_5)) )
print ( "FemurAngle_5 : " + str(float(FemurAngle_5)) )
print ( "TibiaAngle_5 : " + str(float(TibiaAngle_5)) )
print('-----------------')
print ( "CoxaAngle_6 : " + str(float(CoxaAngle_6)) )
print ( "FemurAngle_6 : " + str(float(FemurAngle_6)) )
print ( "TibiaAngle_6 : " + str(float(TibiaAngle_6)) )
'''



#s.write("#1 P1500 #0 P1500 #2 P1500 S5000 T5000\r".encode())
#sleep(3)
#s.write("#1 P2000 #0 P2000 #2 P1750 T5000\r".encode())
#brForward()
#sleep(3)
#brCenter()

#tbForward()
#tbCenter()



'''
#pinOut = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)


p = GPIO.PWM(23, 50) # set PWN to 50Hz for pin 17
p.start(0) #Start at 0 angle
#p2 = GPIO.PWM(23, 50) # set PWN to 50Hz for pin 17
#p2.start(0) #Start at 0 angle
p.ChangeDutyCycle(7.5)
sleep(1)
p.stop()
GPIO.cleanup()
'''

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(22, True)
    p.ChangeDutyCycle(7.5)
    sleep(1)
    GPIO.output(22, False)
    p.ChangeDutyCycle(0)
    '''
    GPIO.output(23, True)
    p2.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(23, False)
    p2.ChangeDutyCycle(0)
    '''
    


