
from driveFunc import *
from setup import *



def wro2():
    drive.robot.Diameter = 9
    drive.robot.axle = 17.5
    drive.toPos(vec2(55,0), speed=500)