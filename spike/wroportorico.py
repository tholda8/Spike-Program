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
    
    turn = 6*360
    nearlydownturn = 420#36
    grabturn = 1*360
    
    def align(self):
        """
        smart align: it will take the harvestor down, and then it resets the angle to 0 at last full turn.
        """
        self.drive.robot.devices[0].m_motor.run_until_stalled(-1000, duty_limit = 30)
        #self.drive.robot.devices[0].m_motor.reset_angle((self.drive.robot.devices[0].angle())%360)
        self.drive.turnMotor(0,self.drive.robot.devices[0].angle()+200, simple = True)
        self.drive.turnMotor(0,0)
        self.drive.robot.devices[0].setDefAngle()
        #self.drive.robot.devices[0].m_motor.run_target(1000, 0)
        
    def up(self, speed = 1000):
        self.drive.turnMotor(0,self.turn, simple = True)

    def down(self, speed = 1000):
        self.drive.turnMotor(0,-20, simple = True)
    
    
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
    drive.robot.Diameter = 5.6
    drive.robot.axle = 14.5
    #drive.robot.pos = vec2(0,0)
    
    #initialization
    drive.robot.pos = vec2(18.5, 14.5)
    drive.robot.addDevice(motor(Port.D))
    drive.robot.addDevice(motor(Port.C))
    lift = liftClass(drive)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    
    #setup
    lift.release()
    lift.align()
    #lift.down()
    
    #yellow pickup
    drive.toPos(vec2(18.5, 42),speed=400)
    lift.grab()
    lift.up()
    drive.rotate(0)
    
    #to the grid
    drive.toPos(vec2(38, 41),speed=500)
    drive.toPos(vec2(68, 69.5),speed=500)
    drive.toPos(vec2(105, 69.5),speed=500)
    
    #yellow drop
    lift.down()
    lift.release()
    #lift.up()
    lift.nearlydown()
    
    #shake yellow
    drive.rotate(3)
    drive.rotate(-3)
    drive.rotate(0)
    
    #align yellow
    drive.straight(-4.6, speed=100, backwards=True)
    lift.down()
    lift.up()
    drive.straight(-40, speed=1000, backwards=True)
    
    #to bricks
    drive.toPos(vec2(18.5, 30),speed=1000, backwards=True)
    drive.rotate(90)
    lift.down()
    
    #pick up bricks (blue)
    offa = -5
    drive.toPos(vec2(18.5, 65),speed=400)
    drive.rotate(90+offa)
    drive.straight(10, speed=400)
    drive.rotate(90-offa)
    drive.straight(10, speed=400)
    drive.rotate(90+offa)
    drive.straight(10, speed=400)
    
    lift.grab()
    lift.up()
    
    #to bowl
    drive.toPos(vec2(68, 24),speed=1000)
    drive.rotate(0)
    drive.toPos(vec2(96, 24),speed=1000)
    
    #get the bowl
    drive.rotate(-45)
    drive.straight(10, speed=1000)
    drive.toPos(vec2(138, 24),speed=1000)
    
    #to the pool
    drive.toPos(vec2(165, 24),speed=1000)
    drive.rotate(90)
    #drive.straight(20, speed=1000)
    drive.toPos(vec2(165, 68),speed=1000)
    
    #drop the bowl
    drive.rotate(-90)
    drive.straight(10, speed=1000)
    drive.rotate(-50)
    #drive.straight(-10, speed=1000, backwards=True)
    drive.toPos(vec2(165, 68),speed=1000, backwards=True)    
    
    #to the grid
    drive.rotate(180)
    drive.toPos(vec2(131, 68),speed=400)
    drive.rotate(180)
    
    #drop the bricks
    lift.down()
    lift.release()
    #lift.up()
    lift.nearlydown()
    
    #shake bricks
    drive.rotate(3+180)
    drive.rotate(-3+180)
    drive.rotate(0+180)
    
    #align bricks
    drive.straight(-4.6, speed=100, backwards=True)
    lift.down()
    lift.up()

    return