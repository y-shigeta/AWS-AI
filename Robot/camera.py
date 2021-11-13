from time import sleep
import datetime
import time

from picamera import PiCamera
import RPi.GPIO as GPIO

PATH = '/home/pi/aws/pics/'
LedPin = 17 # Set GPIO17 as LED pin 
BtnPin = 18 # Set GPIO18 as button pin
# Set Led status to True(OFF)
Led_status = True

# Define a setup function for some setup
def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set LedPin's mode to output,
    # and initial level to high (3.3v) 
    GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.HIGH) 
    # Set BtnPin's mode to input,
    # and pull up to high (3.3V)
    GPIO.setup(BtnPin, GPIO.IN)

# Define a callback function for button callback
def swLed(ev=None):
    global Led_status
    # Switch led status(on-->off; off-->on) 
    Led_status = not Led_status 
    GPIO.output(LedPin, Led_status)
    if Led_status:
        print ('LED OFF...')
    else:
        print ('...LED ON')
        takeCamera()
        

# Take picture by picamera
def takeCamera():
    setup() 
    camera = PiCamera()
    camera.resolution = (1024, 768)
    
    camera.start_preview()

    Today = datetime.datetime.now()
    FileName = PATH + Today.strftime("PiCamera-%Y%m%d%H%M%S.jpeg")
    camera.capture(FileName)

    return FileName

# Define a main function for main process
def main():
    # Set up a falling detect on BtnPin,
    # and callback function to swLed 
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=swLed) 
    while True:
        # Don't do anything.
        time.sleep(2)

# Define a destroy function for clean up everything after # the script finished
def destroy():
    # Turn off LED
    GPIO.output(LedPin, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
    setup() 
    camera = PiCamera()
    camera.resolution = (1024, 768)
    try:
        main()
    # When 'Ctrl+C' is pressed, the program # destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
