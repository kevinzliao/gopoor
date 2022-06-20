for raspberry pi

`sudo pip3 install -r requirements.txt`
needs `sudo apt-get install libportaudio2`

I used this adafruit microphone for audio recording:
learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-test

Sample rate might need to be modified depending on hardware, pi 3B+ works with default settings but pi zero needed the sample rate reduced to 32000 Hz and InputStream passed blocksize=4096
