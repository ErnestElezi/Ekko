from gpiozero import DistanceSensor
import Channels

distanceSensor = DistanceSensor(echo=Channels.ECHO, trigger=Channels.TRIGG)
