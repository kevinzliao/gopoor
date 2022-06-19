#!/usr/bin/env python3
import datetime
from signal import pause
from gpiozero import LED, Button
import picamera
import threading
from AudioRecorder import AudioRecorder
import subprocess
import time

global audio_thread

camera = picamera.PiCamera(resolution=(640, 480), framerate=30)
button = Button(2)
button2 = Button(3)
green_led = LED(17)
red_led = LED(22)

recording = False
audio_thread = AudioRecorder()

# let camera get ready
time.sleep(2)
green_led.on()

def record_button():
    global recording
    # ready state when green led is on and red led is off
    if not recording and green_led.value == 1:
        green_led.off()
        red_led.on()
        recording = True
        now = datetime.datetime.now()
        timestamp = str(now.strftime("%y%m%d%H%M%S"))
        path = '/home/pi/Videos/'

        audio_thread.start(timestamp, path)
        camera.start_recording(path + timestamp + '.h264')

        # keep recording until we press the button again
        while recording:
            camera.wait_recording(0.1)
            print(recording)

        audio_thread.stop()
        camera.stop_recording()

        red_led.off()
        green_led.on()

        # we can start other threads while this post-processing occurs
        print("start muxing")
        cmd = "ffmpeg -i {1}/{0}.wav -i {1}/{0}.h264 -c:v copy -c:a aac -strict experimental {1}/{0}.mp4 && rm {1}/{0}.wav && rm {1}/{0}.h264".format(timestamp, path)
        subprocess.call(cmd, shell=True)

    else:
        print('this should be invoked')
        recording = False

def stop_record():
    print('this second button was pressed')
    global recording
    recording = False

button.when_pressed = record_button
button2.when_pressed = stop_record

pause()
