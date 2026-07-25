#this is example of a script file
from spike_lib.maths import vec2, mat2
from spike_lib.robot import Robot
from spike_lib.driveFunc import DriveManager
from pybricks.parameters import Port
from pybricks.tools import wait, Matrix

#script icon
Imain = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

#script specific tools

#setup
def init():
    robot = Robot(Port, Port, 0, 0)
    robot.lM.reverse = False
    robot.lM.reverse = True
    robot.rM.switchDir = False
    robot.lM.switchDir = False
    drive = DriveManager(robot)
    return robot, drive

#application
def main():
    #inicialization
    robot, drive = init()
    robot.hub.addOffset(0)
    robot.pos = vec2(0,0)