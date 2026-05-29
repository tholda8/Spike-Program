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
    
    def aling(self): #not used
        self.motor.run_target(1000, 0)

    def up(self):
        self.motor.run_target(1000, 55)

    def down(self):
        self.motor.run_target(500, -30)
        
    def flakanec(self):
        self.motor.run_target(1000, -35, wait=False)

    def pickUp(self, pos: vec2):
        self.drive.toPos(pos+self.excentricity - vec2(3, 0), backwards=True)
        self.drive.rotate(180)
        self.down()
        self.drive.straight(-4, backwards=True)
        self.flakanec()

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
    while not antidata[0]:
        antidata = straightAntifail2(distance, backwards, speed)
        print(antidata)
        distanceTraveled = clamp((drive.robot.pos - initialPos).length(), abs(distance)/2, abs(distance)) * sign(distance)
        side = antidata[1]
        if gyroTrust:
            drive.rotate(initAngle, speed = 500)
        if not antidata[0]:
            drive.straight(-distanceTraveled, speed, not backwards)
            drive.rotate(drive.robot.hub.angle() + correction * side, speed = 500)
            

def WRO():
    """
    #start system
    drive.robot.hub.m_hub.system.set_stop_button(Button.CENTER)
    while not drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.beep(500, 100)
    while drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.m_hub.system.set_stop_button(Button.BLUETOOTH)
    """

    #inicialization
    drive.robot.pos = vec2(18.5,11.5)
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
    gridFit()
    #carpet bombing (unloading cubes)
    c = vec2(5.48, 0)
    pos = vec2(124, 69.6)
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
    drive.toPos(vec2(176,25), backwards=True)
    drive.toPos(vec2(122,25), backwards=True)
    drive.rotate(-90,speed = 200)
    drive.toPos(vec2(122,41.5), backwards=True)
    beton.up()
    drive.straight(5)
    drive.toPos(vec2(122,25),backwards=True)
    
    
    #miska
    drive.rotate(90)
    drive.straight(-2, backwards=True)
    beton.down()
    drive.straight(2)
    drive.toPos(vec2(168, 25), backwards=True)
    drive.rotate(-90)
    drive.straight(-10,backwards=True)
    beton.up()
    drive.straight(10)
    
    #BLUE
    #beton.pickUp(vec2(227, 51))
    #drive.straight(10)
    #drive.rotate(90)

    #nástroje
    #drive.toPos(vec2(200, 21))
    drive.toPos(vec2(196, 18),backwards=True)
    drive.toPos(vec2(161, 13.3),backwards=True)
    drive.rotate(0)
    beton.down()
    
    drive.toPos(vec2(89, 13.3),backwards=True)
    drive.toPos(vec2(59, 39),backwards=True)
    drive.toPos(vec2(30, 24),backwards=True)
    drive.rotate(50)
    return
    drive.toPos(vec2(105, 15))
    drive.toPos(vec2(61, 34),backwards=True)
    drive.toPos(vec2(61, 70),backwards=True)
    drive.toPos(vec2(88, 70),backwards=True)
    beton.up()
    
    
    drive.toPos(vec2(70, 70))
    drive.toPos(vec2(70, 19), backwards=True)
    drive.rotate(135)
    beton.down()
    drive.rotate(180)
    drive.toPos(vec2(30, 19))
    drive.straight(-10)
    drive.toPos(vec2(22, 19))
    
    return
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
    
def WROday():
    """
    #start system
    drive.robot.hub.m_hub.system.set_stop_button(Button.CENTER)
    while not drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.beep(500, 100)
    while drive.robot.hub.isButtonPressed(Button.BLUETOOTH):
        wait(10)
    drive.robot.hub.m_hub.system.set_stop_button(Button.BLUETOOTH)
    """

    #inicialization
    drive.robot.pos = vec2(18.5,11.5)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    print(drive.robot.hub.angle(), " | ", drive.robot.pos)
    h = handleCube(drive, Port.F, Port.C, vec2(0,0))
    beton = betonovator(drive, Port.B, vec2(-12,0))
    h.up()
    beton.up()