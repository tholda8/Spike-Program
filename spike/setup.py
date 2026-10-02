from pybricks.parameters import Port
from maths import *
from driveFunc import driveManager
from robot import *


r = robot(Port.E, Port.F, 5.8, 11.2,pos=vec2(0,0))
r.lM.reverse = True
r.rM.switchDir = True
r.lM.switchDir = True
r.hub.addOffset(0)
r.pos = vec2(0,0)
drive = driveManager(r)
