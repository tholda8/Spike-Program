from maths import *
from setup import *
from umath import *
from robot import *
from pybricks.tools import wait

class driveManager:
    def __init__(self, robot:robot):
        self.robot = robot
        self.setDefaultMode()
        #curves
        self.cTolerance = 0.5
        self.cAcc = 100
        self.cDeacc = 50
        self.cStart = vec2(0,0)
        self.cFinish = vec2(0,0)

    def setDefaultMode(self):
        #both
        self.defspeed = 80
        #drive
        self.acc = 100
        self.deacc = 50
        self.turnCoeff = 2
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.0005
        self.racc = 555
        self.rdeacc = 555
        self.braker = True
    
    def setFastMode(self):
        #both
        self.defspeed = 100
        #drive
        self.acc = 300
        self.deacc = 300
        self.turnCoeff = 5
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.01
        self.racc = 800
        self.rdeacc = 800
        self.braker = True
        
    def setPreciseMode(self):
        #both
        self.defspeed = 50
        #drive
        self.acc = 20
        self.deacc = 20
        self.turnCoeff = 10
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.001
        self.racc = 100
        self.rdeacc = 100
        self.braker = True
        
    def setAggressiveMode(self):
        #both
        self.defspeed = 1000
        #drive
        self.acc = 1000
        self.deacc = 500
        self.turnCoeff = 5
        self.brake = True
        #rotate
        self.tolDiff = pi/180
        self.accuracy = 0.1
        self.racc = 1000
        self.rdeacc = 1000
        self.braker = True
    
    def straight(self, length, speed = 1000, backwards = False):
        self.toPos(self.robot.pos + mat2.rotation(self.robot.hub.angleRad()) * vec2(length,0), speed, backwards)
    
    def toPos(self, pos, speed = 1000, backwards = False, stop = True, turn = True, tolerance = 0, extraDist = 0):
        
        offset = self.robot.pos
        angle = atan2((pos-offset).y,(pos-offset).x)
        rotMat = mat2.rotation(-angle)
        if backwards:
            angle += (pi)
        if turn:
            self.rotateRad(angle)
        length = rotMat*(pos - offset)
        swap = sign(length.x - (rotMat*self.robot.pos).x)
        swap = 1
        movedPos = rotMat*(self.robot.pos-offset)
        #print(movedPos.x*swap, " < ", length.x*swap)
        while(movedPos.x*swap < length.x*swap - tolerance):
            self.calcDir(rotMat*(self.robot.pos-offset), length.x, self.calcSpeed(movedPos, length.x, speed),angle, backwards, extraDist)
            self.robot.update()
            movedPos = rotMat*(self.robot.pos-offset)
        #print(movedPos.x*swap, " < ", length.x*swap, movedPos.y)
        if not stop:
            self.robot.stop(False)
        else:
            self.robot.stop(self.brake)
        
    def calcDir(self, pos, length, speed, offsetAngle, backwards = False, extraDist = 0):
        a2 = (self.robot.hub.angleRad()-offsetAngle) % (2*pi)
        pos = vec2(length + extraDist - pos.x, -pos.y)
        a1 = atan2(pos.y, pos.x) % (2*pi)
        angle = (a2 - a1 + pi) % (2*pi) - pi
        speedM = speed * minV(1-(fabs(angle)*self.turnCoeff),-1.0)**1
        if(backwards):
            speed, speedM = -speedM, -speed
        mult = 1/(fabs(angle)*0+1)
        if sign(angle) > 0:
            self.robot.setSpeed(speed*mult, speedM*mult)
        else:
            self.robot.setSpeed(speedM*mult, speed*mult)


    def calcSpeed(self, pos, length, speed):
        if self.cStart == self.cFinish:
            accSpeed =  fabs(pos.x) * self.acc + self.defspeed
            deaccSpeed = fabs(length - pos.x) * self.deacc + self.defspeed
        else:
            accSpeed =  (self.robot.pos - self.cStart).length() * self.cAcc + self.defspeed
            deaccSpeed = (self.robot.pos - self.cFinish).length() * self.cDeacc + self.defspeed

        return clamp(fabs(maxV(deaccSpeed,accSpeed)), self.defspeed ,speed)


    def rotate(self, angle, speed = 1000):
        self.rotateRad(angle/180 * pi, speed = 1000)
        
    def rotateRad(self, angle, speed = 1000):
        angleInit = self.robot.hub.angleRad()
        angleInitD = 0
        angleD = self.angleDiff(self.robot.hub.angleRad(), angle)
        if fabs(angleD) <= self.tolDiff:
            return
        while fabs(angleD) > self.accuracy:
            rspeed = self.calcSpeedR(angleD, speed, angleInitD)
            self.robot.setSpeed(-rspeed*sign(angleD), rspeed*sign(angleD))
            self.robot.update()
            angleInitD = self.angleDiff(self.robot.hub.angleRad(), angleInit)
            angleD = self.angleDiff(self.robot.hub.angleRad(), angle)
        self.robot.stop(self.braker)

    def calcSpeedR(self, angle:float, speed:float, angleInit:float):
        rspeed = fabs(angle) * self.rdeacc + self.defspeed
        aspeed = fabs(angleInit) * self.racc + self.defspeed
        return maxV(maxV(rspeed,aspeed),speed)
    
    def angleDiff(self, angle1:float, angle2:float):
        a1 = (angle1) % (2*pi)
        a2 = (angle2) % (2*pi)
        return (a2 - a1 + pi) % (2*pi) - pi
    
    def bezier(self, p0:vec2, p1:vec2, p2:vec2, p3:vec2, numOfPoints = 10, speed = 500):
        points = generateBezierCurve(p0, p1, p2, p3, numOfPoints)
        #print(points)
        self.cStart = points[0]
        self.cFinish = points[len(points)-1]
        for i in range(numOfPoints+1):
            if i == 0:
                self.toPos(points[i], tolerance=self.cTolerance)
            elif i == 1:
                self.toPos(points[i], tolerance=self.cTolerance,stop=False, speed=speed)
            elif i == numOfPoints:
                self.toPos(points[i], turn=False, speed=speed)
                #print("boop", points[i])
            else:
                self.toPos(points[i], turn = False, stop=False, tolerance=self.cTolerance, extraDist=0.0,speed=speed)
            #print(i, self.robot.pos,points[i])
        self.cStart = self.cFinish = vec2(0,0)
    