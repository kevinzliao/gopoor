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

camera = picamera.PiCamera(resolution=(640, 480), framerate=25)
button = Button(2)
button2 = Button(3)
recording = False
audio_thread = AudioRecorder()

ready_state = 1

# let camera get ready
time.sleep(2)

def toggle_led():
    global ready_state
    return  'echo {} | sudo tee /sys/class/leds/led1/brightness'.format(ready_state ^ 1)


def record_button():
    global recording
    global ready_state

    if not recording and ready_state:
        ready_state = 0
        subprocess.Popen(toggle_led(), shell=True)
        recording = True
        now = datetime.datetime.now()
        timestamp = str(now.strftime("%y%m%d%H%M%S"))
        path = '/home/pi/Videos/'

        camera.start_recording(path + timestamp + '.h264')
        audio_thread.start(timestamp, path)


        # keep recording until we press the button again
        while recording:
            camera.wait_recording(0.01)
            print(recording)
            print(button2.value)
            if button2.value:
                break
        print('exit recording loop')

        camera.stop_recording()
        audio_thread.stop()

        cmd = "ffmpeg -i {1}/{0}.wav -i {1}/{0}.h264 -c:v copy -c:a aac -strict experimental {1}/{0}.mp4 && rm {1}/{0}.wav && rm {1}/{0}.h264".format(timestamp, path)
        subprocess.call(cmd, shell=True)
        ready_state = 1
        subprocess.Popen(toggle_led(), shell=True)
        recording = False

subprocess.Popen(toggle_led(), shell=True)
button.when_pressed = record_button

pause()
