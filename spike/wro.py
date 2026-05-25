from math import *
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
        
    def pickUp(self, correction = 3):
        picked = False
        attempts = 0
        initialAngle = self.drive.robot.hub.angle()
        while not picked:
            attempts += 1
            self.midleDown()
            self.release()
            picked = self.down()
            self.grab()
            wait(200)
            self.up()
            if attempts > 3:
                self.drive.rotate(initialAngle + correction * sign(attempts%2-1), speed = 500)

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

def straightAntifail(distance, backwards = False, speed = 500, tolerance = 5):
    drive.straight(distance, backwards, speed, background = True)
    while drive.isTasksRunning():
        drive.runTasks()
        if abs(drive.robot.hub.m_hub.imu.tilt()[0]) > tolerance:
            #fatal failure
            drive.stopTasks()
            drive.robot.stop()
            return False
    return True

def gridFit(distance = -10, backwards = True, speed = 500, gyroTrust = True, correction = -5):
    initAngle = drive.robot.hub.angle()
    initialPos = drive.robot.pos
    while not straightAntifail(distance, backwards, speed):
        distanceTraveled = clamp((drive.robot.pos - initialPos).length(), abs(distance)/2, abs(distance)) * sign(distance)
        side = sign(drive.robot.hub.m_hub.imu.tilt()[0])
        if gyroTrust:
            drive.rotate(initAngle, speed = 500)
        drive.straight(-distanceTraveled, not backwards, speed)
        drive.rotate(drive.robot.hub.angle() + correction * side, speed = 500)

class Line:
    def __init__(self, a: vec2, b: vec2):
        self.a = a
        self.b = b
        self.direction = (b - a).normalize()
        self.normal = vec2(-self.direction.y, self.direction.x)
        self.parC = - self.normal.x * self.a.x - self.normal.y * self.a.y
        self.orientation = self.direction.xAngle()

    def move(self, shift: vec2):
        self.a += shift
        self.b += shift

    def translated(self, shift: vec2):
        """new line parallel to the original and shifted by given vector"""
        return Line(self.a + shift, self.b + shift)
    
    def fPoint(self, point: vec2):
        """from point to line vector"""
        return (vec2((self.a - point).length() * cos((self.a - point).xAngle() - self.orientation - pi/2, 0)), 0).rotate(self.orientation + pi/2)
    
def alignWall(wall: Line, contact: vec2, speed = 500, time = 1000, general = False):
    """contact is a vector from center of rotation to the side of contact, positive x is in default direction of motion"""
    timer = StopWatch()
    timer.reset()
    while timer.time() < time:
        drive.robot.setSpeed(speed, speed)
        drive.robot.update()
    drive.robot.stop()
    drive.robot.update()
    if general:
        drive.robot.pos += wall.fPoint(drive.robot.pos + contact.rotate(drive.robot.hub.angle()))
    else:
        if round(wall.orientation) == 0:
            drive.robot.pos.y = wall.a.y - contact.x
        elif round(wall.orientation) == pi/2:
            drive.robot.pos.x = wall.a.x - contact.x
        else:
            drive.robot.hub.m_hub.speaker.beep()
            print("incorrect wall orientation: ", wall.orientation)

wallX = Line(vec2(0,0), vec2(0,236.2))
wallY = Line(vec2(0,0), vec2(114.3,0))
wallXX = Line(vec2(114.3,0), vec2(114.3,236.2)) #opposite to wallX
wallYY = Line(vec2(0,236.2), vec2(114.3,236.2)) #opposite to wallY
rFront = vec2(12, 0) #random
rBack = vec2(-12, 0) #random   

def WRO():
    #inicialization
    drive.robot.pos = vec2(19,11.5)
    drive.robot.hub.addOffset(-90)
    h = handleCube(drive, Port.F, Port.C, vec2(0,0))
    beton = betonovator(drive, Port.B, vec2(-12,0))
    h.up()
    beton.up()

    #cube loading
    a = 7.3
    b = 8.3
    drive.toPos(vec2(19,29))
    h.pickUp()
    drive.toPos(vec2(19,29+a))
    h.pickUp()
    drive.toPos(vec2(19,29+b+a))
    h.pickUp()
    drive.toPos(vec2(19,29+b+2*a))
    h.pickUp()
    
    #transport
    drive.toPos(vec2(51,70))
    drive.rotate(180, speed = 500)
    drive.toPos(vec2(90,70),backwards=True, speed = 200)

    #carpet bombing (unloading cubes)
    #drive.toPos(vec2(125, 70),backwards=True, speed = 500)
    toPosAntifail(vec2(125, 70), backwards=True, speed = 500)
    h.drop()
    toPosAntifail(vec2(150,70),backwards=True, speed = 200)
    drive.toPos(vec2(170,70),backwards=True)

    #white (in progress...)
    beton.pickUp(vec2(228, 20))
    drive.straight(10)
    drive.toPos(vec2(150,70), backwards=True) #I hate the need to turn (but it is there)
    beton.up()
    # zášup je potřeba vyladit
    drive.straight(10)
    beton.down()
    drive.straight(-10, backwards=True)
    beton.up()
    drive.straight(30)

    #green
    beton.pickUp(vec2(228, 72))
    drive.straight(10)
    drive.toPos(vec2(150,72), backwards=True)
    drive.rotate(0)
    beton.up()
    drive.straight(30)

    #yellow
    beton.pickUp(vec2(228, 94))
    drive.straight(10)
    drive.toPos(vec2(170,25), backwards=True)
    drive.toPos(vec2(118,25), backwards=True)
    drive.rotate(-90)
    drive.straight(-30, backwards=True)
    beton.up()

    #miska and hladítko
    drive.toPos(vec2(130, 20))
    drive.rotate(30)
    drive.straight(-10, backwards=True)
    beton.down() #miska in
    drive.toPos(vec2(800, 15), backwards=True) #hladítko šoup
    drive.toPos(vec2(170, 40))
    beton.up() #miska out

    #blue and lžička
    beton.pickUp(vec2(228, 46))
    drive.straight(10)
    drive.toPos(vec2(160, 15))
    drive.toPos(vec2(30, 20)) #lžička šoup (možno přidat ninja moves)
    drive.straight(-5, backwards=True)
    drive.toPos(vec2(70, 72), backwards=True)
    beton.up()

    return
    
    drive.toPos(vec2(173,70))
    drive.toPos(vec2(173,70))
    drive.toPos(vec2(236-28,20))
    drive.rotate(180)
    
    
