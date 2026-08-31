from pybricks.parameters import Port
from spike_lib.driveFunc import DriveManager
from spike_lib.robot import *

#C
r = Robot(Port.E, Port.A, 5.79, 19.1,pos=vec2(0,0))
r.lM.reverse = True
r.rM.switchDir = True
r.lM.switchDir = True
r.hub.addOffset(0)
r.pos = vec2(0,0)
drive = DriveManager(r)
