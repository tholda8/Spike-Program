#this is example of a script file
from umath import degrees
from spike_lib.maths import vec2, mat2
from spike_lib.robot import Robot
from spike_lib.driveFunc import DriveManager
from pybricks.parameters import Port, Direction
from pybricks.tools import wait, Matrix
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor

#script icon
Itest = Matrix([
    [100, 100, 100, 100, 100],
    [0, 0, 100, 0, 0],
    [0, 0, 100, 0, 0],
    [0, 0, 100, 0, 0],
    [0, 0, 0, 0, 0]
])

ItestI = Matrix([
    [100, 100, 100, 100, 100],
    [0, 0, 100, 0, 0],
    [0, 0, 100, 0, 100],
    [0, 0, 100, 0, 100],
    [0, 0, 0, 0, 0]
])

#script specific tools

#setup
def init():
    robot = Robot(Port.A, Port.E, 5.6, 15.2)
    robot.lM.reverse = False
    robot.lM.reverse = True
    robot.rM.switchDir = False
    robot.lM.switchDir = False
    drive = DriveManager(robot)
    
    return robot, drive

#application
def test():
    #inicialization
    robot, drive = init()
    while True:
        print(degrees(robot.hub.angleRad()))
        wait(100)
    robot.hub.addOffset(0)
    robot.pos = vec2(0,0)
    drive.straight(150)
    for i in range(5):
        drive.topos(200, 0)
        drive.topos(200, 50)
        drive.topos(150, 50)
        drive.topos(150, 0)
    drive.topos(0, 0, backwards=True)

def testII():
    #inicialization
    otherdrive = DriveBase(Motor(Port.A, Direction.COUNTERCLOCKWISE), Motor(Port.E), 5.6, 15.2)
    otherdrive.use_gyro(True)
    otherdrive.straight(150)
    for i in range(5):
        for j in range(4):
            otherdrive.straight(50)
            otherdrive.turn(-90)
    otherdrive.straight(-150)
    