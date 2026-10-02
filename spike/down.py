from pybricks.parameters import Port
from pybricks.tools import wait
from spike_lib.maths import vec2
from spike_lib.robot import motor
from setup import drive

class liftClass:
    def __init__(self, drive):
        self.drive = drive
    
    turn = 3*360
    nearlydownturn = 360
    grabturn = 1*360
    def up(self, speed = 1000):
        self.drive.turnMotor(0,self.turn, simple = True)

    def down(self, speed = 1000):
        self.drive.turnMotor(0,0, simple = True)
        
    def grab(self, speed = 1000):
        wait(200)
        self.drive.robot.devices[1].setSpeed(speed)
        #self.drive.turnMotor(0,self.grabturn, simple = True)
    
    def release(self, speed = 1000):
        self.drive.robot.devices[1].stop()
        self.drive.turnMotor(1,0)
        
    def nearlydown(self, speed = 1000):
        self.drive.turnMotor(0,self.nearlydownturn, simple = True)

def downFunc():
    drive.robot.Diameter = 5.7
    drive.robot.axle = 14.5
    #drive.robot.pos = vec2(0,0)
    
    drive.robot.pos = vec2(18.5, 14.5)
    drive.robot.addDevice(motor(Port.A))
    drive.robot.addDevice(motor(Port.C))
    drive.robot.devices[0].setSpeed(-200)
    while True:
        pass
    
    return