from pybricks.parameters import *
from maths import *
from driveFunc import driveManager
from robot import *

r = robot(Port.E, Port.A, 8.7, 15.4,pos=vec2(17,11.3))
r.lM.reverse = True
r.rM.switchDir = True
r.lM.switchDir = True
r.hub.addOffset(-90)
La = motor(Port.F)
Ra = motor(Port.B)
Us = Ultrasonic(Port.D)
#Ut = Ultrasonic(Port.C)
r.devices.append(La)
r.devices.append(Ra)
r.devices.append(Us)
drive = driveManager(r)