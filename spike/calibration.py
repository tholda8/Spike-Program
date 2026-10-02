from setup import drive
from pybricks.tools import Matrix
from spike_lib.maths import vec2
from umath import pi, degrees, radians
from pybricks.robotics import DriveBase
from pybricks.parameters import Port, Stop, Axis
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch, wait, hub_menu
from pybricks.hubs import PrimeHub

calibrationI = Matrix([
    [0, 100, 100, 100, 0],
    [100, 0, 0, 0, 0],
    [100, 0, 0, 0, 0],
    [0, 100, 100, 100, 0],
    [0, 0, 0, 0, 0]
])

def tDistance():
    drive.robot.pos = vec2(0, 0)
    print("")
    print("Running distance test:")
    drive.straight(100)
    print("End position: " + str(drive.robot.pos))
    print("It was supposed to go 1m straight, if it is less then make the wheel radius smaller, and vice versa.")
    print("")

def tTurn():
    drive.robot.pos = vec2(0, 0)
    print("")
    print("Running turn test:")
    print("lol, not implemented yet!")
    print("")
    
def tPos():
    drive.robot.pos = vec2(0, 0)
    print("")
    print("Running toPos test:")
    drive.tp(200, 0)
    drive.tp(0, 0, True)
    print("End position: " + str(drive.robot.pos))
    print("It should be around (0, 0) and the robot should be close to the starting position, if not you have a big problem.")
    print("")

def tRide():
    drive.robot.pos = vec2(0, 0)
    print("")
    print("Running ride (orientation) test:")
    drive.tp(200, 0)
    print("2m straight: " + str(drive.robot.pos))
    drive.tp(200, 100)
    print("1m left: " + str(drive.robot.pos))
    drive.tp(100, 0)
    print("1m back and 1m right: " + str(drive.robot.pos))
    drive.tp(200, -50)
    print("1m straight and 0.5m right: " + str(drive.robot.pos))
    drive.tp(0, 100)
    print("2m back and1.5m left: " + str(drive.robot.pos))
    drive.tp(0, 0)
    print("Back to start")
    print("End position: " + str(drive.robot.pos))
    print("")

def calibration():
    while True:
        page = hub_menu("D", "T", "P", "R")

        if page == "D":
            tDistance()

        elif page == "T":
            tTurn()

        elif page == "P":
            tPos()

        elif page == "R":
            tRide()