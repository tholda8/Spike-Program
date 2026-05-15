from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *




class handleCube:
    def __init__(self, drive: driveManager, liftMotor: Port, grabMotor: Port, excentricity: vec2):
        """
        has 3 chambers for cubes and 2 motors for lifting and grabbing cubes
        excentricity: center in center of rotation; x in direction of motion; y perpendicular to x positive to the left, measured in read/write position"""
        self.drive = drive
        self.liftMotor = Motor(liftMotor)
        self.grabMotor = Motor(grabMotor)
        self.excentricity = excentricity

    def up(self):
        self.liftMotor.run_target(1000, -145)

    def down(self):
        timer = StopWatch()
        timer.reset()
        self.liftMotor.run_target(1000, 123, wait=False)
        while not self.liftMotor.done():
            if timer.time() > 1000 or self.drive.robot.hub.m_hub.imu.tilt()[1]>10:
                self.liftMotor.stop()
                return False
        return True

    def midle(self):
        self.liftMotor.run_target(1000, 0)

    def midleDown(self):
        self.liftMotor.run_target(1000, -40)

    def dropPos(self):
        self.liftMotor.run_target(1000, 120)

    def grab(self):
        self.grabMotor.run(-1000)

    def release(self):
        self.grabMotor.run_target(1000, 0)
        
    def pickUp(self):
        picked = False
        attempts = 0
        while not picked:
            attempts += 1
            self.midleDown()
            self.release()
            picked = self.down()
            self.grab()
            wait(200)
            self.up()
            if attempts > 3:
                self.drive.rotate(self.drive.robot.hub.angle()+3, speed = 500)
                self.drive.rotate(self.drive.robot.hub.angle()-3, speed = 500)

    def drop(self):
        self.midle()
        self.release()
        self.up()

    def load(self):
        """loads 3 of each color in cubes"""
        self.drive.rotate(90)
        self.pickUp()

    def unload(self, pos: vec2, orientation: int, n = 4):
        """unloads all cubes in mozaikovator"""
        for i in range(n):
            self.drop()
            self.drive.straight(-5)

class betonovator:
    def __init__(self, drive: driveManager, motor: Port, excentricity):
        """excentricity: center in center of rotation; x in direction of motion; y perpendicular to x positive to the left, measured in read/write position"""
        self.drive = drive
        self.motor = Motor(motor)
        self.excentricity = excentricity
    
    def aling(self): #not used
        self.motor.run_target(1000, 0)

    def up(self):
        self.motor.run_target(1000, 55)

    def down(self):
        self.motor.run_target(500, -30)

    def pickUp(self, pos: vec2):
        self.drive.toPos(pos+self.excentricity, backwards=True)
        self.drive.rotate(180)
        self.down()

def WRO():
    
    drive.robot.pos = vec2(19,11.5)
    drive.robot.hub.addOffset(-90)
    h = handleCube(drive, Port.F, Port.C, vec2(0,0))
    beton = betonovator(drive, Port.B, vec2(-12,0))
    a = 7.3
    b = 8.3
    h.up()
    drive.toPos(vec2(19,29))
    h.pickUp()
    drive.toPos(vec2(19,29+a))
    #h.drop()
    h.pickUp()
    drive.toPos(vec2(19,29+b+a))
    #h.drop()
    h.pickUp()
    drive.toPos(vec2(19,29+b+2*a))
    h.pickUp()
    
    drive.toPos(vec2(51,70))
    drive.rotate(180, speed = 500)
    drive.toPos(vec2(90,70),backwards=True, speed = 200)
    drive.toPos(vec2(125, 70),backwards=True, speed = 500)
    h.drop()
    drive.toPos(vec2(150,70),backwards=True, speed = 200)
    drive.toPos(vec2(170,70),backwards=True)

    #white
    beton.pickUp(vec2(228, 20))
    drive.straight(10)
    drive.toPos(vec2(150,70), backwards=True)
    beton.up()
    return
    
    drive.toPos(vec2(173,70))
    drive.toPos(vec2(173,70))
    drive.toPos(vec2(236-28,20))
    drive.rotate(180)
    
    
