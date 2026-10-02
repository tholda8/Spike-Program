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
        self.motor.run_target(500, 0)
    
    def left(self):
        self.motor.run_target(500, 80)

    def right(self):
        self.motor.run_target(500, -80)

def vyzvajesenik3():
    arm = Arm(drive, Port.F, Port.E)
    drive.robot.pos = vec2(15,8)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    drive.setPreciseMode()
    
    arm.left()
    drive.toPos(vec2(15,45))
    drive.toPos(vec2(45,45))
    drive.toPos(vec2(47,75))
    drive.toPos(vec2(128,75),backwards=True)
    drive.toPos(vec2(125,18),backwards=True)
    drive.rotate(0)
    drive.toPos(vec2(190,20))
    
    pass