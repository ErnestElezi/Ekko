import threading
import FaceDisplay as fd
from time import sleep

faceThread = threading.Thread(target=fd.runFaceDisplay)

faceThread.start()
