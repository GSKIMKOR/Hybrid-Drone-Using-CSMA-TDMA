from pymavlink import mavutil
import time
import socket
import sys
from random import randint
import pandas as pd
import math

HOST = '10.0.1.104'
PORT = 3333

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

the_connection = mavutil.mavlink_connection('udp:10.0.1.22:2222')
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

num_slot = 2
num_drone = 4

def tdma():
    print("Waiting for the time slot")
    global xgyro, ygyro, zgyro
    time.sleep(num_slot-1)

    while True:
        msg = the_connection.recv_match()
        
        if not msg:
            continue
        if msg.get_type() == 'RAW_IMU':
            xgyro = float(float(msg.xgyro))
            ygyro = float(float(msg.ygyro))
            zgyro = float(float(msg.zgyro))
            
        if not msag:
            continue
        if msag.get_type() == 'RAW_IMU':
            ax = float(float(msag.xacc)*1e-2)
            ay = float(float(msag.yacc)*1e-2)   
            az = float(float(msag.zacc)*1e-2)
        
            pitchAngle = math.degrees(float(float(math.atan(-ax/math.sqrt(ay*ay+az*az)))))
            rollAngle = math.degrees(float(float(math.atan(ay/math.sqrt(ax*ax+az*az)))))
            
            tdv = "TDMA IMU: " + str(xgyro) + ' ' + str(ygyro) + ' ' + str(zgyro) + '             ' + str(round(pitchAngle,3)) + ' ' + str(round(rollAngle,3))
            print(tdv)
            s.send(tdv)
            time.sleep(num_drone-num_slot)
            
            break
            
           
                  
def csma():
    global xgyro, ygyro, zgyro
    while True:
        msag = the_connection.recv_match()
        
        if not msag:
            continue
        if msag.get_type() == 'RAW_IMU':
            xgyro = float(float(msag.xgyro))
            ygyro = float(float(msag.ygyro))
            zgyro = float(float(msag.zgyro))     
            
        if not msag:
            continue
        if msag.get_type() == 'RAW_IMU':
            ax = float(float(msag.xacc)*1e-2)
            ay = float(float(msag.yacc)*1e-2)   
            az = float(float(msag.zacc)*1e-2)
        
            pitchAngle = math.degrees(float(float(math.atan(-ax/math.sqrt(ay*ay+az*az)))))
            rollAngle = math.degrees(float(float(math.atan(ay/math.sqrt(ax*ax+az*az)))))
            
            csv = "CSMA IMU: " + str(xgyro) + ' ' + str(ygyro) + ' ' + str(zgyro) + '             ' + str(round(pitchAngle,3)) + ' ' + str(round(rollAngle,3))
            print(csv)
            s.send(csv)

            break



xgyro_threshold = 200
ygyro_threshold = 200
zgyro_threshold = 200

pitchAngle_threshold = 4   #Unit[degree]
rollAngle_threshold = 4
#yawAngle_threshold = 4

   

while True:
    msag = the_connection.recv_match()

    if not msag:
        continue
    if msag.get_type() == 'RAW_IMU':
        xgyro = float(float(msag.xgyro))
        ygyro = float(float(msag.ygyro))
        zgyro = float(float(msag.zgyro))
        
    if not msag:
        continue
    if msag.get_type() == 'RAW_IMU':
        ax = float(float(msag.xacc)*1e-2)
        ay = float(float(msag.yacc)*1e-2)   
        az = float(float(msag.zacc)*1e-2)
        
        pitchAngle = math.degrees(float(float(math.atan(-ax/math.sqrt(ay*ay+az*az)))))
        rollAngle = math.degrees(float(float(math.atan(ay/math.sqrt(ax*ax+az*az)))))
        #yawAngle = math.degrees(float(float(math.atan(math.sqrt(ax*ax+ay*ay)/(-az)))))
        

    
        if abs(xgyro) > xgyro_threshold or abs(ygyro) > ygyro_threshold or abs(zgyro) > zgyro_threshold or abs(pitchAngle) > pitchAngle_threshold or abs(rollAngle) > rollAngle_threshold:
            tdma()
        else:
            csma()
