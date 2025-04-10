import RPi.GPIO as gp
from enum import Enum
from gpiozero import Button, DistanceSensor
import speech_recognition as sr
import pyttsx3
import threading
import time
import FaceEmotions as face

gp.setmode(gp.BOARD)

### Define Channels ###

# Distance Sensor
channelTrigg = 19
channelEcho = 21
distanceSensor = DistanceSensor(
    channelTrigg, channelEcho, max_distance=1, threshold_distance=0.2)

# IR Sensors
channelIRA = 13
channelIRB = 15
irA = Button(channelIRA)
irB = Button(channelIRB)

# Motor Left
channelEnableA = 3
channelDirectionA = 5
gp.setup(channel=channelEnableA, direction=gp.OUT)
gp.setup(channel=channelDirectionA, direction=gp.OUT)

# Motor Right
channelEnableB = 7
channelDirectionB = 11
gp.setup(channel=channelEnableB, direction=gp.OUT)
gp.setup(channel=channelDirectionB, direction=gp.OUT)

# Controll Variables
dutyCycle = 100
power = 100
speech = ''


class DIR(Enum):
    FO = 1
    BA = 1
    RI = 1
    LE = 1


r = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)


# PWM variables
enableA = gp.PWM(channelEnableA, dutyCycle)
enableB = gp.PWM(channelEnableB, dutyCycle)

### Default Values ###
enableA.stop()
enableB.stop()
gp.output(channelDirectionA, True)
gp.output(channelDirectionB, True)

### Controll Funcitons ###


def setDirection(direction: DIR):
    match direction:
        case DIR.F:
            gp.output(channelDirectionA, True)
            gp.output(channelDirectionB, True)
        case DIR.B:
            gp.output(channelDirectionA, False)
            gp.output(channelDirectionB, False)
        case DIR.R:
            gp.output(channelDirectionA, True)
            gp.output(channelDirectionB, False)
        case DIR.L:
            gp.output(channelDirectionA, False)
            gp.output(channelDirectionB, True)
    pass


def stop():
    enableA.stop()
    enableB.stop()
    pass


def start():
    global power
    enableA.start(power)
    enableB.start(power)


def setPower(powerInt: int):
    global power
    power = powerInt
    pass


def forward():
    setDirection(DIR.FO)
    pass


def right():
    setDirection(DIR.RI)


def left():
    setDirection(DIR.LE)


def backwards():
    setDirection(DIR.BA)

# Text to Speech


def recogniseSpeech():
    global r, engine
    try:

        with sr.Microphone() as source:
            sr.adjust_for_ambient_noise(source, duration=0.2)

            print("Listening...")
            audio = sr.listen(source)
            print("Done...")

            text = sr.recognize_google(audio_data=audio)
            text = text.lower()

            if type(text) == type("hello"):
                return text
            return ""

    except sr.RequestError as e:
        print("Could not request results {e}")
        return ""

    except sr.UnknownValueError:
        print("Unknown error occured")
        return ""


def startRecognision():
    global speech
    while True:
        speech = recogniseSpeech()


voice_thread = threading.Thread(target=startRecognision, daemon=True)
voice_thread.start()


def speak(command):
    stop()
    global engine
    engine.say(command)
    engine.runAndWait()
    pass


### Pygame ###

face.pg.init()

face_thread = threading.Thread(target=face.runFaceDisplay(), daemon=True)
face_thread.start()

### Main Loop ###
while True:
    if irA.is_pressed and irB.is_pressed:
        forward()
    elif irA.is_pressed:
        left()
    elif irB.is_pressed:
        right()
    else:
        forward()
