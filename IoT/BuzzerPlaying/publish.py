# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 18:03:38 2022

@author: user
"""

import paho.mqtt.client as mqtt
import time


print("***************************")
print("*         蜂鳴器控制       *")
print("*  歌名 ->蜂鳴器唱指定歌曲 *")
print("*  exit ->停止控制        *")
print("***************************")

#create object
client = mqtt.Client()

#connect
client.connect('140.127.220.208', 1883,120)


#publish control commend
command = "default"

while(command!="exit"):
    command = input("請輸入蜂鳴器控制指令:")
    client.publish("iot",command)
    time.sleep(0.25)
    
    