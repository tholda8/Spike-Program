from pybricks.parameters import *
from maths import *
from driveFunc import driveManager
from robot import *

r = robot(Port.D, Port.B, 5.75, 11.25,pos=vec2(0,0))
r.lM.reverse = True
r.rM.switchDir = True
r.lM.switchDir = True
r.hub.addOffset(0)
drive = driveManager(r)