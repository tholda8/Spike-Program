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
        self.liftMotor.run_target(1000, 123)
    
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
        self.release()
        self.down()
        wait(200)
        self.grab()
        wait(200)
        self.up()
        
    def pickUp2(self):
        self.midleDown()
        wait(100)
        self.release()
        self.down()
        wait(100)
        self.grab()
        wait(100)
        self.up()        


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



def WRO():
    
    drive.robot.pos = vec2(19,11.5)
    drive.robot.hub.addOffset(-90)
    h = handleCube(drive, Port.F, Port.C, vec2(0,0))
    a = 7.3
    b = 8.3
    h.up()
    drive.toPos(vec2(19,29))
    h.pickUp()
    drive.toPos(vec2(19,29+a))
    #h.drop()
    h.pickUp2()
    drive.toPos(vec2(19,29+b+a))
    #h.drop()
    h.pickUp2()
    drive.toPos(vec2(19,29+b+2*a))
    h.pickUp2()
    
    drive.toPos(vec2(51,70))
    drive.toPos(vec2(91,70),backwards=True)
    
    a = 5
    drive.toPos(vec2(123,70),backwards=True)
    h.drop()
    drive.toPos(vec2(123+a,70),backwards=True)
    h.drop()
    drive.toPos(vec2(123+2*a,70),backwards=True)
    h.drop()
    drive.toPos(vec2(123+3*a,70),backwards=True)
    h.drop()
    return
    
    drive.toPos(vec2(173,70))
    drive.toPos(vec2(173,70))
    drive.toPos(vec2(236-28,20))
    drive.rotate(180)
    
    
