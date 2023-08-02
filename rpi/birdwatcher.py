from gpiozero import LED
from gpiozero import MotionSensor
from time import sleep
from picamera import PiCamera
import datetime
import base64
import requests

camera = PiCamera
camera.resolution = (800,600)
camera.rotation = 180
green_led = LED(17)
pir = MotionSensor(4)

apigw = "YOUR GATEWAY HERE"

green_led.off()

while True:
    pir.wait_for_motion()
    capture_time = datetime.datetime.now()
    image_name = capture_time.strftime('%y%m%d%H%M%S') + '.jpg'
    green_led.on()
    sleep(2)
    camera.capture(image_name)
    green_led.off()

    # Base64 encode image
    img = open(image_name, 'rb')
    img_b64 = base64.b64encode(img.read())
    img.close()

    # Create query string parameters
    qsp = {'ImageName': image_name, 'CapureTime': capture_time}

    # Send image to API Gateway
    img_post = requests.post(apigw, data=img_b64, params=qsp)

    # Print response
    print(img_post.status_code)
    print(img_post.text)
    
    sleep(15)