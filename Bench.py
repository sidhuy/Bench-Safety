import gpiozero
import time
import math
import Adafruit_CharLCDPlate

userFile = ""
lcd = display.lcd
trig0 = OutputDevice()
echo0= InputDevice()
trig1 = OutputDevice()
echo1 = InputDevice()
reps = 0
prev = -1
weight = 100
lastTime = time()

weightFlag = False

sleep(2)

def get_Users():
    users = {}
    f = open(userFile)
    for line in f:
        line = line.strip()
        line = line.split()
        users[line[0]] = line[1]
    return users

def get_pulse_time():
    trig.on()
    sleep(0.00001)
    trig.off()

    while echo.is_active == False:
        pulse_start = time()

    while echo.is_active == True:
        pulse_end = time()

    sleep(0.06)

    return pulse_end - pulse_start

def calculate_distance(duration):
    speed = 343
    distance = speed * duration / 2
    return distance

def calculate_velocity(d0,d1,old_d0,old_d1,last_read):
    v0 = (d0-old_d0)/(last_read-lastTime)
    v1 = (d1-old_d1)/(last_read-lastTime)
    return (v0+v1)/2
    


while True:
    lcd.clear()
    lcd.message('Please adjust your weight: '+ weight)
    while not weightFlag:
        b = lcd.buttons()
        if b is not prev:
            if lcd.buttonPressed(lcd.SELECT):
                lcd.clear()
                lcd.message('You may now begin lifting')
                break
            elif lcd.buttonPressed(lcd.UP):
                weight += 5
            elif lcd.buttonPressed(lcd.DOWN):
                weight -= 5
        else:
            now = time()
            since = now - lastTime
            if since > REFRESH_TIME or since < 0.0:
                lcd.clear()
                lcd.message('Please adjust your weight: '+ weight)
                lastTime = now
    

    duration = get_pulse_time()
    dist0_orig = calculate_distance(duration)
    print(dist0_orig)
    duration = get_pulse_time()
    dist1_orig = calculate_distance(duration)
    last_dist0 = dist0_orig
    last_dist1 = dist1_orig
    lastTime = time()
    v_last = 0
    lift_error = 0
    while True:
        duration = get_pulse_time()
        dist0 = calculate_distance(duration)
        duration = get_pulse_time()
        dist1 = calculate_distance(duration)
        now = time()
        v_now = calculate_velocity(dist0,dist1,last_dist0,last_dist1,now)
        if abs(dist0 - dist1) > .1:
            lift_bars()
            lift_error = 1
            break
        elif last_dist0 > dist0 and last_dist1 > dist1:
            
            reps += 1
