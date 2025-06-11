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

def hunter(value=30):
    global gotbear
    if drive.robot.devices[3].distance() > value:
        print("hunt", drive.robot.devices[3].distance())
        drive.stopTasks()
        drive.robot.stop()
        drive.close()
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
    drive.close()

def start():
    drive.circleToPos(vec2(17,75), connect=[False,True])
    drive.circleToPos(vec2(60,75), connect=[True,True])
    drive.circleToPos(vec2(60,65), connect=[True,True])
    drive.circleToPos(vec2(110,65), connect=[True,True])
    drive.open(background=True, time = 400)
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
    drive.robot.devices.append(Ultrasonic(Port.C))
    
    drive.robot.pos = vec2(17,11.3)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    
    drive.setDefaultMode()
    drive.setMotorsToDef()
    
    bearsetup()
    
    drive.close()
    
    drive.robot.hub.colorAnimate([Color.MAGENTA, Color.NONE,Color.WHITE, Color.NONE], 100)
    while not drive.robot.hub.isButtonPressed(Button.CENTER):
        pass
    drive.robot.hub.color(Color.MAGENTA)
    start()
    while not bear():
        drive.open()
        drive.gotbear = False
        sken(distance = 249, value = 175, sample=12)
        drive.stopTasks()
        drive.robot.stop()
        hunt(distance = 105)
        drive.stopTasks()
        drive.robot.stop()
        if drive.robot.pos.y > 249:
            drive.circleToPos(drive.robot.pos + vec2(20,-20),backwards=True)
        if drive.robot.pos.y < 110 or  drive.robot.pos.x < 90:
            drive.toPos(vec2(115,160), backwards=True)
        drive.rotate(90)
        
    finish()
    raise SystemExit("Bear rescued!")