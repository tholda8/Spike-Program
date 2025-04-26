from maths import *
from setup import *
from umath import *
from robot import *
from pybricks.tools import wait

class driveManager:
    def __init__(self, robot:robot):
        self.robot = robot
        self.setDefaultMode()

    def setDefaultMode(self):
        #both
        self.defspeed = 80
        #drive
        self.deacc = 100
        self.turnCoeff = 7
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.0005
        self.rdeacc = 555
        self.braker = True
    
    def setFastMode(self):
        #both
        self.defspeed = 100
        #drive
        self.deacc = 300
        self.turnCoeff = 5
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.01
        self.rdeacc = 800
        self.braker = True
        
    def setPreciseMode(self):
        #both
        self.defspeed = 50
        #drive
        self.deacc = 20
        self.turnCoeff = 10
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.001
        self.rdeacc = 100
        self.braker = True
        
    def setAggressiveMode(self):
        #both
        self.defspeed = 1000
        #drive
        self.deacc = 500
        self.turnCoeff = 5
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.1
        self.rdeacc = 1000
        self.braker = True
    
    def straight(self, length, speed = 1000, backwards = False):
        self.toPos(self.robot.pos + mat2.rotation(self.robot.hub.angleRad()) * vec2(length,0), speed, backwards)
    
    def toPos(self, pos, speed = 1000, backwards = False):
        
        offset = self.robot.pos
        angle = atan2((pos-offset).y,(pos-offset).x)
        rotMat = mat2.rotation(-angle)
        if backwards:
            angle += (pi)
        self.rotateRad(angle)
        length = rotMat*(pos - offset)
        swap = sign(length.x - (rotMat*self.robot.pos).x)
        movedPos = rotMat*(self.robot.pos-offset)
        while(movedPos.x*swap < length.x*swap):
            self.calcDir(rotMat*(self.robot.pos-offset), length.x, self.calcSpeed(movedPos, length.x, speed),angle, backwards)
            self.robot.update()
            movedPos = rotMat*(self.robot.pos-offset)
        self.robot.stop(self.brake)
        
    def calcDir(self, pos, length, speed, offsetAngle, backwards = False):
        a2 = (self.robot.hub.angleRad()-offsetAngle) % (2*pi)
        pos = vec2(length - pos.x, -pos.y)
        a1 = atan2(pos.y, pos.x) % (2*pi)
        angle = (a2 - a1 + pi) % (2*pi) - pi
        speedM = speed * minV(1-fabs(angle)*self.turnCoeff,-1)
        if(backwards):
            speed, speedM = -speedM, -speed
        
        if sign(angle) > 0:
            self.robot.setSpeed(speed, speedM)
        else:
            self.robot.setSpeed(speedM, speed)


    def calcSpeed(self, pos, length, speed):
        accSpeed = fabs(length - pos.x) * self.deacc + self.defspeed
        return clamp(fabs(accSpeed), self.defspeed ,speed)


    def rotate(self, angle, speed = 1000):
        self.rotateRad(angle/180 * pi, speed = 1000)
        
    def rotateRad(self, angle, speed = 1000):
        a1 = (self.robot.hub.angleRad()) % (2*pi)
        a2 = (angle) % (2*pi)
        angle = (a2 - a1 + pi) % (2*pi) - pi
        if fabs(angle) <= self.tolDiff:
            return
        while fabs(angle) > self.accuracy:
            rspeed = self.calcSpeedR(angle, speed)
            if(angle > 0):
                self.robot.setSpeed(-rspeed, rspeed)
            else:
                self.robot.setSpeed(rspeed, -rspeed)
            self.robot.update()
            a1 = (self.robot.hub.angleRad()) % (2*pi)
            angle = (a2 - a1 + pi) % (2*pi) - pi
        self.robot.stop(self.braker)

    def calcSpeedR(self, angle:float, speed:float):
        rspeed = fabs(angle) * self.rdeacc + self.defspeed
        return maxV(rspeed,speed)