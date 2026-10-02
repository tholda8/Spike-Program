from pybricks.parameters import Port
from pybricks.tools import wait
from spike_lib.maths import vec2
from spike_lib.robot import motor
from setup import drive

class liftClass:
    def __init__(self, drive):
        self.drive = drive
        self.drive.robot.devices[0].setDefAngle()
        self.release()
    
    turn = 3*360
    nearlydownturn = 90
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

def wroportorico():
    drive.robot.Diameter = 5.7
    drive.robot.axle = 14.5
    #drive.robot.pos = vec2(0,0)
    
    drive.robot.pos = vec2(18.5, 14.5)
    drive.robot.addDevice(motor(Port.A))
    drive.robot.addDevice(motor(Port.C))
    lift = liftClass(drive)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    
    #lift.down()
    
    drive.toPos(vec2(18.5, 41),speed=400)
    lift.grab()
    lift.up()
    drive.rotate(0)
    
    drive.toPos(vec2(38, 41),speed=500)
    drive.toPos(vec2(68, 69.5),speed=500)
    drive.toPos(vec2(104.5, 69.5),speed=500)
    
    lift.nearlydown()
    lift.release()
    
    drive.straight(-4.6, speed=100)
    lift.up()
    drive.straight(-40, speed=1000)
    drive.toPos(vec2(18.5, 14.5),speed=1000, backwards=True)
    drive.rotate(90)
    lift.down()
    drive.toPos(vec2(18.5, 57),speed=400)
    
    lift.grab()
    lift.up()
    
    return