from pybricks.parameters import Port
from spike_lib.maths import vec2
from spike_lib.robot import Robot
from spike_lib.driveFunc import DriveManager


r = Robot(Port.E, Port.F, 5.8, 11.2, pos=vec2(0,0))
r.lM.reverse = True
r.rM.switchDir = True
r.lM.switchDir = True
r.hub.addOffset(0)
r.pos = vec2(0,0)
drive = DriveManager(r)
