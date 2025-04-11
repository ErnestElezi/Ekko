import Channels
import RPi.GPIO as gp

gp.setmode(gp.BCM)

gp.setup(Channels.ENA, gp.OUT)
gp.setup(Channels.IN1, gp.OUT)
gp.setup(Channels.IN2, gp.OUT)

gp.setup(Channels.ENB, gp.OUT)
gp.setup(Channels.IN3, gp.OUT)
gp.setup(Channels.IN4, gp.OUT)


default_power = 60  # %
default_turn_power = 60  # %
duty_cycle = 100

ENA = gp.PWM(Channels.ENA, duty_cycle)  # Right Motor
ENB = gp.PWM(Channels.ENB, duty_cycle)  # Left Motor


def start(power=default_power):
    ENA.start(power)
    ENB.start(power)


def stop():
    ENA.stop()
    ENB.stop()


def forward(power=default_power):
    gp.output(Channels.IN1, 1)
    gp.output(Channels.IN2, 0)
    gp.output(Channels.IN3, 1)
    gp.output(Channels.IN4, 0)
    start(power=power)


def backward(power=default_power):
    gp.output(Channels.IN1, 0)
    gp.output(Channels.IN2, 1)
    gp.output(Channels.IN3, 0)
    gp.output(Channels.IN4, 1)
    start(power=power)


def right(power=default_turn_power):
    gp.output(Channels.IN1, 0)
    gp.output(Channels.IN2, 1)
    gp.output(Channels.IN3, 1)
    gp.output(Channels.IN4, 0)
    start(power=power)


def left(power=default_turn_power):
    gp.output(Channels.IN1, 1)
    gp.output(Channels.IN2, 0)
    gp.output(Channels.IN3, 0)
    gp.output(Channels.IN4, 1)
    start(power=power)
