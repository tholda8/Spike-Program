from driveFunc import *
from setup import *

class Arm:
    def __init__(self, drive: driveManager, color: Port, motor: Port) -> None:
        self.drive = drive
        self.color = ColorSensor(color)
        self.motor = Motor(motor)
        
    def colorBlue(self):
        for i in range(10):
            hvs = self.color.hsv()
            hue = hvs[0]
            if hue > 150 and hue < 280:
                return True
            elif hue > 280:
                return False
        self.drive.robot.hub.beep(500, 100)
        return False
             
    def mid(self):
        self.motor.run_target(1000, 0)
    
    def left(self):
        self.motor.run_target(1000, 80)

    def right(self):
        self.motor.run_target(1000, -80)

def vyzvajesenik():
    arm = Arm(drive, Port.F, Port.E)
    drive.robot.pos = vec2(15,8)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    arm.left()
    
    
    
    drive.toPos(vec2(10,40))
    drive.rotate(90)
    if arm.colorBlue():
        arm.mid()
        drive.rotate(0)
        drive.toPos(vec2(15,45))  
        drive.toPos(vec2(55,45)) 
        drive.rotate(90) 
        drive.rotate(180) 
        drive.rotate(-90) 
        drive.rotate(0) 
        drive.toPos(vec2(42,75))
    else:
        drive.toPos(vec2(15,54))
        arm.right()
        drive.toPos(vec2(15,45))  
        drive.toPos(vec2(30,46))  
        drive.toPos(vec2(40,40))
        arm.mid()
        drive.rotate(90)
        arm.left()
        drive.toPos(vec2(45,45))
        drive.toPos(vec2(45,85))
        drive.toPos(vec2(42,75),backwards=True)
        
    drive.rotate(0)
    if arm.colorBlue():
        arm.left()
        drive.toPos(vec2(55,75))    
        arm.right()
    else:
        arm.right()
        drive.toPos(vec2(55,75))   
        arm.left() 

    ##CCCCCC
    drive.toPos(vec2(82,75))
    drive.rotate(0)
    bluec = arm.colorBlue()
    if bluec:
        arm.left()
        drive.toPos(vec2(95,75))    
        arm.right()
    else:
        arm.right()
        drive.toPos(vec2(95,75))    
        arm.left()
    drive.toPos(vec2(125,75))
    if bluec:
        arm.left()
        drive.toPos(vec2(125,50))
        arm.right()
    else:
        arm.right()
        drive.toPos(vec2(125,50))
        arm.left()
    arm.mid()
    drive.toPos(vec2(125,20))
    drive.toPos(vec2(160,20),speed=300)
    drive.rotate(90)
    drive.rotate(-90)
    pass