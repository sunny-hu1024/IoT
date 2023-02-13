import network
from umqtt.simple import MQTTClient
import time as time
import random

#buzzer use
from machine import Pin,PWM
import time

#define note
tones = {
    
    "B0": 31,
    
    "C1": 33, "CS1": 35, "D1": 37, "DS1": 39,  "E1": 41, "F1": 44,
    "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62,
    
    "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87,
    "FS2": 93, "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123,
    
    "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175,
    "FS3": 185, "G3": 196, "GS3": 208, "A3": 220,  "AS3": 233, "B3": 247,
    
    "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349,
    "FS4": 370, "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494,
    
    "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698,
    "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988,
    
    "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397,
    "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
    
    "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794,
    "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
    
    "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978,
}


###create senbonzakura sheet###

#create note
senbonzakura_note =["D5","F5","G5","G5","A5","A5","A5","C6","D6","G5","F5","A5",
                    "D5","F5","G5","G5","A5","A5","A5","AS5","A5","G5","F5","F5",
                    "D5","F5","G5","G5","A5","A5","A5","C6","D6","G5","F5","A5",
                    "D5","F5","AS5","A5","G5","F5","G5","A5","E5","C5","D5"]
#create tempo
senbonzakura_tempo =[0.25,0.25,0.375,0.375,0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.5,
                      0.25,0.25,0.375,0.375,0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.5,
                      0.25,0.25,0.375,0.375,0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.5,
                      0.25,0.25,0.5,0.5,0.5,0.5,0.25,0.25,0.25,0.25,0.5]

###create kaikaikitan sheet###

#create note
kaikaikitan_note =["AS4","AS4","AS4","AS5","A5","AS5",
                   "AS4","AS4","AS4","AS5","A5","AS5",
                   "AS4","AS4","AS4","AS4","G5","F5","F5","D5","D5","DS5","F5","D5","C5","AS4",
                   "AS4","F5","F5","AS4","AS4","AS4","AS4","F5","F5",
                   "AS4","AS4","AS4","AS4","A4","AS4","C5",
                   "D5","D5","D5","D5","D5","AS5","A5","G5","F5"]
#create tempo
kaikaikitan_tempo =[0.25,0.25,0.25,0.25,0.5,0.5,
                     0.25,0.25,0.25,0.25,0.5,0.5,
                     0.25,0.25,0.25,0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.25,0.5,
                     0.375,0.375,0.5,0.25,0.25,0.25,0.375,0.375,0.5,
                     0.25,0.25,0.25,0.25,0.25,0.25,0.5,
                     0.25,0.25,0.25,0.25,0.25,0.25,0.375,0.125,0.5]

###create gunsei sheet###

#create note
gunsei_note =["DS6",
             "AS5","G5","A5","AS5","G5","A5","AS5","A5","AS5","C6",
              "F5","G5","A5","F5","G5","A5","F5","C5","C5","F5","C5","D5",
              "G5","F5","AS4","G5","F5","AS4","AS4","G5","FS5","FS5","C6","A5",
             "A5","DS6","D6","C6","AS5","C6","F6","DS6","DS6","D6","D6"]
#create tempo
gunsei_tempo =[0.875,
                0.25,0.25,0.25,0.5,0.25,0.25,0.5,0.25,0.25,0.5,
                0.25,0.25,0.5,0.25,0.25,0.5,0.25,0.25,0.5,0.25,0.25,0.5,
                0.25,0.25,0.5,0.25,0.25,0.5,0.25,0.25,0.5,0.25,0.25,0.5,
                0.25,0.25,0.25,0.5,0.25,0.5,0.25,0.25,0.5,0.25,0.25,0.625]

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#connect network
wlan.connect('nukim_iot','nukimiot')
time.sleep(5)

#connect mqtt broker
mqClient0 = MQTTClient('Test','140.127.220.208')
mqClient0.connect()
print("[OK]")

#let buzzer sing

#LED light
led=Pin(2,Pin.OUT)

#buzzer (use PWM )
buzzer = PWM(Pin(15))

#if buzzer don't end first it will makes a sound continueously before receive message
buzzer.deinit()#let buzzer end first

def playSong(note,tempo):
    i=0
    #buzzer sing 
    while (i!=len(note)):
       buzzer.init()#let buzzer start sing
       buzzer.freq(tones[note[i]])#set frequency of buzzer
       led.value(1)
       time.sleep(tempo[i])#set sleep time (pause time)
       led.value(0)
       i=i+1
    buzzer.deinit()#play finish,let buzzer stop to make a sound

def get_msg(topic,msg):
    msg1=str(msg).replace('b','',1).replace('\'','')
    print(msg1)
    if(msg1=="senbonzakura"):
        playSong(senbonzakura_note,senbonzakura_tempo)
    elif(msg1=="kaikaikitan"):
        playSong(kaikaikitan_note,kaikaikitan_tempo)
    elif(msg1=="gunsei"):
        playSong(gunsei_note,gunsei_tempo)
        
mqClient0.set_callback(get_msg)
mqClient0.subscribe("iot",0)

while (True):
    mqClient0.check_msg()
    
    

