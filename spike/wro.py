from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *
from imgs import wroimg, wroimg2
from maths import pi, mat2
from umath import radians, cos, pi, degrees


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
        timer = StopWatch()
        timer.reset()
        self.liftMotor.run_target(1000, -155, wait=False)
        while not self.liftMotor.done():
            if timer.time() > 1500:
                break
            wait(10)

    def down(self):
        timer = StopWatch()
        timer.reset()
        self.liftMotor.run_target(1000, 120, wait=False)
        while not self.liftMotor.done():
            if timer.time() > 1300 or self.drive.robot.hub.m_hub.imu.tilt()[1]>10:
                self.liftMotor.stop()
                return False
        return True

    def midle(self):
        self.liftMotor.run_target(1000, 0)

    def midleDown(self):
        self.liftMotor.run_target(1000, -80)#######
    def semidown(self):
        self.liftMotor.run_target(1000, -40)#######
    def dropPos(self):
        self.liftMotor.run_target(1000, 120)

    def grab(self):
        self.grabMotor.run(-1000)

    def release(self):
        self.grabMotor.run_target(1000, 0)
        
    def pickUp(self,correction = 3):
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
                self.drive.rotate(initialAngle + correction * sign(attempts%2-0.5), speed = 500) 


    def drop(self):
        self.midleDown()
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
    
    def align(self): #not used
        self.motor.run_target(1000, 10)

    def up(self):
        self.motor.run_target(1000, 55)

    def down(self):
        self.motor.run_target(500, -35)

    def gentledown(self):
        self.motor.run_target(100, -35)
        
    def flakanec(self):
        self.motor.run_target(1000, -30, wait=False)

    def pulse(self):
        self.drive.setFastMode
        for i in range(2):
            self.flakanec()
            wait(500)
            self.drive.straight(10)
            self.align()
            self.drive.straight(-10, backwards=True)
        for i in range(2):
            self.flakanec()
            wait(500)
            self.drive.straight(7)
            self.align()
            self.drive.straight(-6, backwards=True)
        self.drive.setDefaultMode()

    def pickUp(self, pos: vec2):
        self.drive.toPos(pos+self.excentricity - vec2(3, 0), backwards=True)
        self.drive.rotate(180)
        self.down()
        self.drive.straight(-4, backwards=True)
        self.flakanec()

    def dropOff(self, pos: vec2, roatation: float):
        self.drive.toPos(pos + mat2.rotation(radians(roatation)) * self.excentricity, backwards=True)
        self.drive.rotate(180 + roatation)
        self.up()
        self.drive.straight(100)
    

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
    
def alignWall(wall: Line, contact: vec2, speed = 500, time = 1000, gyroCorrection = True):
    """contact is a vector from center of rotation to the side of contact, positive x is in default direction of motion"""
    timer = StopWatch()
    timer.reset()
    while timer.time() < time:
        drive.robot.setSpeed(speed, speed)
        #drive.robot.update()
    drive.robot.stop()
    #drive.robot.update()
    if round(wall.orientation) == 0:
        drive.robot.pos.y = wall.a.y - contact.x
    elif abs(wall.orientation - pi/2) < 0.1:
        drive.robot.pos.x = wall.a.x - contact.x
    else:
        drive.robot.hub.m_hub.speaker.beep()
        print("incorrect wall orientation: ", wall.orientation)
    if gyroCorrection:
        drive.robot.hub.resetAngle()
        drive.robot.hub.addOffset(degrees(wall.orientation) + 90*sign(contact.x))

wallX = Line(vec2(0,0), vec2(236.2, 0))
wallY = Line(vec2(0,0), vec2(0, 114.3))
wallXX = Line(vec2(0, 114.3), vec2(236.2, 114.3)) #opposite to wallX
wallYY = Line(vec2(236.2, 0), vec2(236.2, 114.3)) #opposite to wallY
rBack = vec2(-5.3, 0)   
rInsideBack = vec2(-4.2, 0)

def straightAntifail(distance, backwards = False, speed = 500, tolerance = 2):
    initialAngle = drive.robot.hub.angle()
    drive.straight(distance, speed, backwards, background = True)
    while drive.isTasksRunning():
        drive.runTasks()
        #print(drive.robot.hub.m_hub.imu.tilt()[0])
        if abs(drive.robot.hub.m_hub.imu.tilt()[0]) > tolerance:
            #fatal failure
            drive.stopTasks()
            drive.robot.stop()
            return False
    return True

def straightAntifail2(distance, backwards = False, speed = 500, tolerance = 2, gyrotolerance = 5):
    initialAngle = drive.robot.hub.angle()
    initialPos = drive.robot.pos
    if backwards:
        speed = -speed
    drive.robot.setSpeed(speed, speed)
    while (drive.robot.pos - initialPos).length() < abs(distance):
        drive.robot.update()
        if abs(drive.robot.hub.angle() - initialAngle) > gyrotolerance:
            drive.robot.stop()
            print(drive.robot.hub.angle() - initialAngle, "kola")
            return [False, sign(drive.robot.hub.angle() - initialAngle)]
        #print(drive.robot.hub.m_hub.imu.tilt()[0])
        if abs(drive.robot.hub.m_hub.imu.tilt()[0]) > tolerance:
            #fatal failure
            drive.robot.stop()
            print(drive.robot.hub.m_hub.imu.tilt()[0])
            return [False, sign(drive.robot.hub.m_hub.imu.tilt()[0])]
    drive.robot.stop()
    return [True, 0]

def gridFit(distance = -15, backwards = True, speed = 200, gyroTrust = True, correction = -5):
    initAngle = drive.robot.hub.angle()
    initialPos = drive.robot.pos
    antidata = [False, 0]
    fitted = False
    while not antidata[0]:
        antidata = straightAntifail2(distance, backwards, speed)
        print(antidata)
        distanceTraveled = clamp((drive.robot.pos - initialPos).length(), abs(distance)/2, abs(distance)) * sign(distance)
        side = antidata[1]
        if gyroTrust:
            drive.rotate(initAngle, speed = 500)
        if not antidata[0]:
            fitted = True
            drive.straight(-distanceTraveled, speed, not backwards)
            drive.rotate(drive.robot.hub.angle() + correction * side, speed = 500)
    return fitted
            

def WRO():
    
    #start system
    drive.robot.hub.m_hub.system.set_stop_button(Button.CENTER)
    drive.robot.hub.image(wroimg)
    while not drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.beep(500, 100)
    while drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.m_hub.system.set_stop_button(Button.BLUETOOTH)
    

    #inicialization
    drive.robot.pos = vec2(18.5,12.3)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    print(drive.robot.hub.angle(), " | ", drive.robot.pos)
    h = handleCube(drive, Port.F, Port.C, vec2(0,0))
    beton = betonovator(drive, Port.B, vec2(-12,0))
    h.up()
    beton.up()

    #cube loading
    a = 7.2
    b = 9.2
    drive.toPos(vec2(19,29.3))
    drive.setPreciseMode()
    #drive.rotate(90)
    #drive.setDefaultMode()
    h.pickUp()
    drive.toPos(vec2(19,29.3+a))
    #drive.setPreciseMode()
    #drive.rotate(90)
    #drive.setDefaultMode()
    h.pickUp()
    drive.toPos(vec2(19,29.3+b+a))
    #drive.setPreciseMode()
    #drive.rotate(90)
    #drive.setDefaultMode()
    h.pickUp()
    drive.toPos(vec2(19,29.3+b+2*a))
    #drive.setPreciseMode()
    #drive.rotate(90)
    drive.setDefaultMode()
    h.pickUp()
    
    #transport
    drive.setPreciseMode()
    drive.toPos(vec2(51,70))
    drive.setDefaultMode()
    """
    drive.rotate(-90)
    drive.robot.lM.setSpeed(-300)
    drive.robot.rM.setSpeed(-300)
    for i in range(1700):
        drive.robot.update()
    drive.robot.lM.brake()
    drive.robot.rM.brake()
    rpos = drive.robot.pos
    drive.robot.pos = vec2(rpos.x, 110)
    drive.toPos(vec2(51,70),speed = 300)
    """
    drive.rotate(180, speed = 300)
    drive.toPos(vec2(100,69.6),backwards=True, speed = 300)
    if gridFit():
        drive.robot.pos = vec2(drive.robot.pos.x, 72)
    #carpet bombing (unloading cubes)
    c = vec2(5.48, 0)
    pos = vec2(122, drive.robot.pos.y) #124
    #drive.toPos(vec2(125, 70),backwards=True, speed = 500)
    drive.setPreciseMode()
    drive.toPos(pos, backwards=True, speed = 500)
    drive.setDefaultMode()
    h.drop()
    wait(250)
    h.semidown()
    h.grab()
    h.up()
    drive.toPos(pos+c, backwards=True, speed = 500)
    h.drop()
    wait(250)
    h.semidown()
    h.grab()
    h.up()
    drive.toPos(pos+2*c, backwards=True, speed = 500)
    h.drop()
    wait(250)
    h.semidown()
    h.grab()
    h.up()
    drive.toPos(pos+3*c, backwards=True, speed = 500)
    h.drop()
    wait(250)
    h.semidown()
    h.grab()
    h.up()
    
    
    #drive.toPos(vec2(150,70),backwards=True, speed = 100)
    drive.toPos(vec2(170,69.6),backwards=True)
    drive.setDefaultMode()

    #white (in progress...)
    """
    beton.pickUp(vec2(228, 20))
    drive.straight(20)
    
    drive.toPos(vec2(186,44), backwards=True) 
    drive.toPos(vec2(147,74), backwards=True) #I hate the need to turn (but it is there)
    beton.up()
    # zášup je potřeba vyladit
    drive.straight(15)
    beton.down()
    drive.straight(-13,backwards=True)
    beton.up()
    drive.straight(5)
    """

    #green
    beton.pickUp(vec2(227, 74))
    drive.straight(10)
    
    drive.toPos(vec2(150.2,70), backwards=True)
    drive.rotate(0)
    beton.up()
    drive.straight(15)

    #yellow
    beton.pickUp(vec2(224, 98))
    drive.straight(10)
    drive.toPos(vec2(176,26), backwards=True)
    drive.toPos(vec2(122,26), backwards=True)
    drive.rotate(-90,speed = 200)
    drive.toPos(vec2(122,41.5), backwards=True)
    beton.up()
    drive.straight(5)
    drive.toPos(vec2(122,25),backwards=True)
    
    
    #miska
    drive.rotate(90)
    drive.straight(-2, backwards=True)
    beton.gentledown()
    drive.straight(2)
    drive.toPos(vec2(168, 25), backwards=True)
    drive.rotate(-90)
    drive.straight(-10,backwards=True)
    beton.up()
    #drive.straight(15)
    #drive.rotate(90)
    #alignWall(wallX, rBack, -500)
    
    #BLUE
    #beton.pickUp(vec2(227, 51))p
    #drive.straight(10)
    #drive.rotate(90)

    #nástroje
    drive.toPos(vec2(200, 21))
    #drive.straight(5)
    #drive.robot.hub.beep(300, 100)
    #drive.rotate(0)
    #drive.toPos(vec2(196, 18),backwards=True)
    drive.toPos(vec2(161, 13.3),backwards=True)
    drive.rotate(0)
    beton.down()
    
    drive.toPos(vec2(89, 13.3),backwards=True)
    drive.toPos(vec2(59, 39),backwards=True)
    drive.toPos(vec2(30, 24),backwards=True)
    drive.rotate(50)
    beton.up()

    #extra
    drive.toPos(vec2(65, 80))
    drive.rotate(270)
    beton.down()
    drive.toPos(vec2(40, 50))
    drive.rotate(70)
    beton.up()
    drive.straight(10)
    beton.down()
    drive.straight(-25, backwards=True)
    return
    
def WROday():
    
    #start system
    drive.robot.hub.m_hub.system.set_stop_button(Button.CENTER)
    drive.robot.hub.image(wroimg2)
    while not drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.beep(500, 100)
    while drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.m_hub.system.set_stop_button(Button.BLUETOOTH)
    

    #inicialization
    drive.robot.pos = vec2(18.5,12.3)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    print(drive.robot.hub.angle(), " | ", drive.robot.pos)
    h = handleCube(drive, Port.F, Port.C, vec2(0,0))
    beton = betonovator(drive, Port.B, vec2(-12,0))
    h.up()
    beton.up()

    #cube loading
    a = 7.2
    b = 9.2
    drive.toPos(vec2(19,29.3))
    drive.setPreciseMode()
    #drive.rotate(90)
    #drive.setDefaultMode()
    h.pickUp()
    drive.toPos(vec2(19,29.3+a))
    #drive.setPreciseMode()
    #drive.rotate(90)
    #drive.setDefaultMode()
    h.pickUp()
    
    #/overkill
    drive.setDefaultMode()
    drive.toPos(vec2(70, 69))
    drive.rotate(180)
    drive.straight(-13, backwards=True)
    beton.down()
    beton.flakanec()
    drive.rotate(160)
    drive.rotate(200)

    #/fill 1
    drive.toPos(vec2(40, 60))
    drive.toPos(vec2(27, 30), backwards=True)
    drive.rotate(45)
    beton.up()

    #/overkill
    drive.toPos(vec2(70, 68))
    drive.rotate(180)
    beton.align()
    drive.straight(-32, backwards=True)
    beton.pulse()
    beton.flakanec()

    #/fill2
    drive.toPos(vec2(40, 60))
    drive.toPos(vec2(30, 30), backwards=True)
    drive.rotate(45)
    beton.up()

    #/load
    drive.toPos(vec2(50, 70))
    drive.toPos(vec2(100,69.6))
    drive.rotate(0)
    #if gridFit(15, backwards=False, correction=5):
    #    drive.robot.pos = vec2(drive.robot.pos.x, 72)
    drive.straight(13)
    h.release()
    drive.straight(-20, backwards= True, speed=300)

    #/golf
    beton.align()
    drive.toPos(vec2(65, 70), backwards=True)
    drive.toPos(vec2(65, 40), backwards=True)
    drive.rotate(180)
    drive.straight(-14, backwards=True)
    drive.straight(14)
    drive.toPos(vec2(60, 95), backwards=True)
    drive.rotate(180)
    drive.straight(-14, backwards=True)
    drive.straight(10)
    
    #white
    drive.toPos(vec2(50, 25))
    drive.toPos(vec2(117, 25), backwards=True)
    drive.toPos(vec2(117, 40), backwards=True)
    beton.down()
    beton.flakanec()
    drive.rotate(250)
    drive.rotate(290)
    drive.rotate(270)
    drive.straight(15)
    drive.toPos(vec2(70, 20))
    beton.up()
    beton.align()
    drive.toPos(vec2(180, 30))

    #golf 3
    drive.toPos(vec2(150, 40), backwards=True)
    drive.straight(5)
    beton.down()

    #white2
    drive.toPos(vec2(210,97))
    drive.rotate(180)
    beton.up()