from pybricks.parameters import Port
from maths import *
from driveFunc import driveManager
from robot import *

#C
r = robot(Port.E, Port.A, 5.6, 19.1,pos=vec2(0,0))
r.lM.reverse = True
r.rM.switchDir = True
r.lM.switchDir = True
r.hub.addOffset(0)
r.pos = vec2(0,0)
drive = driveManager(r)
