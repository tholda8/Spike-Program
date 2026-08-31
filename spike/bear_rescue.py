
from spike_lib.maths import vec2, avr
from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *

def bear():
    if drive.robot.devices[3].distance() > 30:
        return True
    return False

gotbear = False
def bearsetup():
    global gotbear
    gotbear = False

def close(background = False):
        angle = 20
        if background:
            drive.turnMotor(0,-angle, background=True, simple = True, time = 400)
            drive.turnMotor(1,angle, background=background, simple = True, time = 400)
        else:
            drive.turnMotor(0,-angle, background=True, simple = True)
            drive.turnMotor(1,angle, background=True, simple = True)
            while drive.isTasksRunning():
                drive.runTasks()
            drive.stopTasks()
            drive.robot.devices[0].hold()
            drive.robot.devices[1].hold()

def open(background = False, time = 0):
        drive.turnMotor(0,0, background=True, simple = True, time = time)
        drive.turnMotor(1,0, background=background, simple = True, time = time)

def hunter(value=30):
    global gotbear
    if drive.robot.devices[3].distance() > value:
        print("hunt", drive.robot.devices[3].distance())
        drive.stopTasks()
        drive.robot.stop()
        close()
        gotbear = True
        return True
    return False
    
def skener(uvalues, sample = 10, value=40):
    uvalues.append(drive.robot.devices[2].distance())
    if len(uvalues) > sample:
        uvalues.pop(0)
    if avr(uvalues) > value:
        print("sken", avr(uvalues))
        drive.robot.stop()
        return True
    
def sken(distance, value, sample=10):
    uvalues = []
    drive.toPos(vec2(120,distance), background=True, speed=550)
    while drive.isTasksRunning():
        if hunter() or skener(uvalues, sample, value):
            return
        drive.runTasks()
        
def hunt():
    global gotbear
    if gotbear:
        return None
    if drive.robot.pos.y < 100:
        drive.straight(-10, speed=1000, backwards=True)
    drive.rotate(180)
    print(drive.robot.pos)
    if drive.robot.pos.y > 249:
        drive.toPos(vec2(90, 258), speed = 600)
        drive.toPos(vec2(21, 258), background=True, speed = 600)
    else: 
        drive.toPos(vec2(21, drive.robot.pos.y), background=True, speed = 600)
    while drive.isTasksRunning():
        if hunter():
            drive.stopTasks()
            drive.robot.stop()
            return
        drive.runTasks()
    close()

def start():
    drive.circleToPos(vec2(17,75), connect=[False,True])
    drive.circleToPos(vec2(60,75), connect=[True,True])
    drive.circleToPos(vec2(60,65), connect=[True,True])
    drive.circleToPos(vec2(110,65), connect=[True,True])
    open(background=True, time = 400)
    drive.circleToPos(vec2(115,100), connect=[True,True])
    drive.circleToPos(vec2(115,155), connect=[True,False], accuracy=1.5)
    drive.stopTasks()
    drive.rotate(90)

def finish():
    drive.toPos(vec2(110,60), connect=[False,True], backwards=True, tolerance=5)
    #drive.circleToPos(vec2(110,55), connect=[False,True], backwards=True)
    drive.circleToPos(vec2(65,60), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(55,82), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(20,82), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(20,50), connect=[True,True], backwards=True)
    drive.toPos(vec2(20,0),connect=[True,False], backwards=True)

    drive.rotate(90)
def bear_rescue():
    drive.robot.addDevice(motor(Port.F))
    drive.robot.addDevice(motor(Port.E))
    drive.robot.addDevice(Ultrasonic(Port.B))
    drive.robot.addDevice(Ultrasonic(Port.D))
    
    drive.robot.hub.resetAngle()
    
    drive.setDefaultMode()
    drive.setMotorsToDef()
    
    bearsetup()
    close()
    drive.robot.hub.addOffset(-180)
    
    drive.robot.pos = vec2(17,11.3)

    close()
    
    drive.robot.hub.colorAnimate([Color.MAGENTA, Color.NONE,Color.WHITE, Color.NONE], 100)
    while not drive.robot.hub.isButtonPressed(Button.CENTER):
        pass
    drive.robot.hub.color(Color.MAGENTA)
    start()
    while not bear():
        open()
        gotbear = False
        sken(distance = 249, value = 175, sample=12)
        drive.stopTasks()
        drive.robot.stop()
        hunt()
        drive.stopTasks()
        drive.robot.stop()
        if drive.robot.pos.y > 249:
            drive.circleToPos(drive.robot.pos + vec2(20,-20),backwards=True)
        if drive.robot.pos.y < 110 or  drive.robot.pos.x < 90:
            drive.toPos(vec2(115,160), backwards=True)
        drive.rotate(90)
        
    finish()
    raise SystemExit("Bear rescued!")