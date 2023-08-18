import time
import requests
import math
import random
import time
import RPi.GPIO as GPIO

TOKEN = "BBFF-llFcdHmn0AYFcGp7O0D0Uisu6EfvPo"   
DEVICE_LABEL = "HOCAGEE_44"  
VARIABLE_LABEL_1 = "sensor_ultrasonic"  

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)
 

GPIO_TRIGGER = 18 
GPIO_ECHO = 24 
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)  
 

GPIO.output(GPIO_TRIGGER, GPIO.LOW)


def get_range():
    
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
     
    
    GPIO.output(GPIO_TRIGGER, False)
    timeout_counter = int(time.time())
    start = time.time()
 
    
    while GPIO.input(GPIO_ECHO)==0 and (int(time.time()) - timeout_counter) < 3:
        start = time.time()
 
    timeout_counter = int(time.time())
    stop = time.time()
    
    while GPIO.input(GPIO_ECHO)==1 and (int(time.time()) - timeout_counter) < 3:
        stop = time.time()
 
    
    elapsed = stop-start
 
    
    distance = elapsed * 34320
 
    
    distance = distance / 2
 
    
    return distance


def build_payload(variable_1):
    
    val = get_range()
    value_1 = float("{0:.2f}".format(val))
    payload = {variable_1: value_1}

    return payload


def post_request(payload):
    
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(VARIABLE_LABEL_1)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
