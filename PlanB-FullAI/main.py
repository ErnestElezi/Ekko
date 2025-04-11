import MotorController as mc
import InfraRed as ir
import DistanceSensor as ds
import FaceDisplay as fd
from time import sleep
import threading

faceThread = threading.Thread(target=fd.runFaceDisplay)
faceThread.start()


def crosWalk():
    mc.stop()
    sleep(2)
    mc.forward()


while True:

    leftSensor = ir.IRL.value
    rightSensor = ir.IRR.value

    distance = ds.distanceSensor.distance

    if leftSensor and rightSensor:
        mc.forward()
    elif leftSensor and not rightSensor:
        mc.left()
    elif not leftSensor and rightSensor:
        mc.right()
    else:
        crosWalk()

    if distance < 0.13:
        mc.stop()
