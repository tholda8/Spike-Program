from pybricks.tools import wait
from pybricks.parameters import Color, Port, Button
from pybricks.pupdevices import ColorSensor
from Device_manager.maths import vec2
from Device_manager.robot import Robot
from driveFunc import driveManager
from pybricks.pupdevices import Motor
from setup import *
class cube:
    def __init__(self, color: Color, position: vec2):
        self.color = color
        self.pos = position

def setCubes():
    rShift = 31 #in mm
    c_shift = 31
    cubes = []
    for set in [
        [Color.YELLOW, vec2(0, 0)],
        [Color.BLUE, vec2(0, 0)],
        [Color.GREEN, vec2(0, 0)],
        [Color.WHITE, vec2(0, 0)],
    ]:
        cCubes = []
        for col in range(3):
            for row in range(2):
                cCubes.append(cube(set[0], set[1] + vec2(col * c_shift, row * rShift)))
        cubes.extend(cCubes)
    return cubes

class mozaikovator:
    def __init__(self, drive: driveManager, liftMotor: Port, grabMotor: Port, excentricity: vec2):
        """
        has 3 chambers for cubes and 2 motors for lifting and grabbing cubes
        excentricity: center in center of rotation; x in direction of motion; y perpendicular to x positive to the left, measured in read/write position"""
        self.drive = drive
        self.cubes = []
        self.liftMotor = Motor(liftMotor)
        self.grabMotor = Motor(grabMotor)
        self.excentricity = excentricity

    def up(self):
        self.liftMotor.run_target(1000, -145)

    def down(self):
        self.liftMotor.run_target(1000, 123)
    
    def midle(self):
        self.liftMotor.run_target(1000, 0)

    def dropPos(self):
        self.liftMotor.run_target(1000, 120)

    def grab(self):
        self.grabMotor.run(-1000)

    def release(self):
        self.grabMotor.run_target(1000, 0)

    def pickUp(self):
        self.release()
        self.down()
        wait(200)
        self.grab()
        wait(200)
        self.up()

    def drop(self):
        self.midle()
        self.release()
        self.up()

    def load(self, cubes: list[cube]):
        """loads 3 of each color in cubes"""
        for cube in cubes:
            self.drive.toPos(cube.pos-self.excentricity.rotated(pi/2))
            self.drive.rotate(90)
            self.pickUp()
            self.cubes.append(cube)

    def unload(self, pos: vec2, orientation: int, n = 4):
        """unloads all cubes in mozaikovator"""
        self.drive.toPos(pos-self.excentricity.rotated(orientation))
        for i in range(n):
            self.drop()
            self.cubes.pop(0)
            self.drive.straight(-5)

class betonovator:
    def __init__(self, drive: driveManager, motor: Port, excentricity):
        """excentricity: center in center of rotation; x in direction of motion; y perpendicular to x positive to the left, measured in read/write position"""
        self.drive = drive
        self.motor = Motor(motor)
    
    def aling(self): #not used
        self.motor.run_target(1000, 0)

    def up(self):
        self.motor.run_target(1000, 55)

    def down(self):
        self.motor.run_target(500, -30)

#inicialization
#robot = Robot(Port.A, Port.E, 5.6, 19.1, pos=vec2(19, 19))

"""
robot = Robot(Port.A, Port.E, 0, 0, pos=vec2(19, 19))
drive = driveManager(robot)

hub = robot.hub.m_hub
robot.rM.reverse = #False
robot.lM.switchDir = True
robot.rM.switchDir = True
"""

def wro():
    cubesLoad = [cube(Color.YELLOW, vec2(19, 42.5)), cube(Color.YELLOW, vec2(19, 48)), cube(Color.BLUE, vec2(19, 58.5)), cube(Color.BLUE, vec2(19, 65))]
    mozaik = mozaikovator(drive, Port.F, Port.C, vec2(12.5, 0))
    beton = betonovator(drive, Port.B, vec2(-13, 0))
    hub = drive.robot.hub.m_hub
    #wait till start
    mozaik.up()
    beton.up()
    while Button.CENTER not in hub.buttons.pressed():
        wait(10)   
    hub.speaker.beep()
    #start
    mozaik.load(cubesLoad)
    mozaik.unload(vec2(110.5, 70), 180)
    SystemExit("End of program")



    
