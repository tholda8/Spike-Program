

from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *

def bear():
    distance = drive.robot.devices[3].distance()
    if  distance > 30 or distance < 7:
        return True
    return False

gotbear = False
def bearsetup():
    global gotbear
    gotbear = False

def close(background = False):
        angle = 25
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

def closeCompletely():
    #drive.robot.hub.beep(525,200)
    drive.robot.devices[0].setSpeed(-1000)
    drive.robot.devices[1].setSpeed(1000)
    timer = StopWatch()
    while timer.time() < 200:
        drive.runTasks()
        drive.robot.update() 
    #drive.turnMotor(0,-25, background=True, simple = True, time = 400)drive.turnMotor(0,-angle, background=True, simple = True, time = 400)
    #drive.turnMotor(1,angle, background=background, simple = True, time = 400)
        

def open(background = False, time = 0):
    drive.robot.devices[0].stop()
    drive.robot.devices[1].stop()

    drive.turnMotor(0,0, background=True, simple = True, time = time)
    drive.turnMotor(1,0, background=background, simple = True, time = time) 

def openCompletely(delay = False):
    drive.robot.devices[0].stop()
    drive.robot.devices[1].stop()
    drive.robot.devices[0].setSpeed(1000)
    drive.robot.devices[1].setSpeed(-1000)
    if delay:
        timer = StopWatch()
        while timer.time() < 200:
            drive.runTasks()
            drive.robot.update() 
    return
    drive.turnMotor(0,0, background=True, simple = True, time = time)
    drive.turnMotor(1,0, background=background, simple = True, time = time) 

def hunter(value=30):
    global gotbear
    distance = drive.robot.devices[3].distance()
    if  distance > value or distance < 7:
        #print("hunt", drive.robot.devices[3].distance())
        drive.stopTasks()
        drive.robot.stop()
        closeCompletely()
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
    drive.toPos(vec2(122,distance), background=True, speed=350)
    #print("A")
    while drive.isTasksRunning():
        if hunter() or skener(uvalues, sample, value):
            #open(background=True)
            openCompletely()
            return
        drive.runTasks()
    #print("B")
        
def hunt():
    global gotbear
    if gotbear:
        return None
    if drive.robot.pos.y < 248 and drive.robot.pos.y > 162:
        drive.straight(-10, speed=1000, backwards=True)
    if drive.robot.pos.y > 248:
        closeCompletely()
    ###
    #print("C")
    if hunter():
        drive.stopTasks()
        drive.robot.stop()
        return
    ###
    drive.stopTasks()
    drive.rotate(180)
    if drive.robot.pos.y > 248:
        #print("D")
        openCompletely()
    if drive.robot.pos.y > 248:
        #print("E")
        #drive.robot.hub.beep(420,500)
        drive.toPos(vec2(90, 264), speed = 600)#######
        drive.toPos(vec2(22.5, 267), background=True, speed = 600)######
    else: 
        #print("F")
        drive.toPos(vec2(22, drive.robot.pos.y), background=True, speed = 800)
    while drive.isTasksRunning():
        
        if hunter():
            #print("G")
            drive.stopTasks()
            drive.robot.stop()
            return
        drive.runTasks()
    #print("H")
    closeCompletely()

def start():
    drive.circleToPos(vec2(17,75), connect=[False,True])
    drive.circleToPos(vec2(60,75), connect=[True,True])
    drive.circleToPos(vec2(60,65), connect=[True,True])
    drive.circleToPos(vec2(110,65), connect=[True,True])
    open(background=True, time = 400)
    drive.circleToPos(vec2(115,100), connect=[True,True])
    drive.circleToPos(vec2(115,160.5), connect=[True,False], accuracy=1.5)
    drive.stopTasks()
    drive.rotate(90)
    openCompletely()

def planB(drive:driveManager):
    drive.straight(1)
    drive.rotate(-90)
    timer = StopWatch()
    while timer.time() < 2500:
        drive.robot.setSpeed(-500,-500)
        drive.runTasks()
        drive.robot.update()
    drive.straight(10)
    
    drive.rotate(0)
    timer = StopWatch()
    while timer.time() < 2500:
        drive.robot.setSpeed(-500,-500)
        drive.runTasks()
        drive.robot.update()
    drive.straight(4)
    
    drive.rotate(90)
    timer = StopWatch()
    while timer.time() < 5000:
        drive.robot.setSpeed(-500,-500)
        drive.runTasks()
        drive.robot.update()
    
def planBTimer(drive:driveManager):
    timer = StopWatch()
    while timer.time() < 10000:
        yield
        pass
    drive.stopTasks()
    planB(drive)
    planC(drive)

def planC(drive:driveManager):
    drive.rotate(90)
    drive.straight(4)
    
    
    drive.rotate(0)
    timer = StopWatch()
    while timer.time() < 2500:
        drive.robot.setSpeed(-500,-500)
        drive.runTasks()
        drive.robot.update()
    drive.straight(4)
    
    drive.rotate(90)
    timer = StopWatch()
    while timer.time() < 5000:
        drive.robot.setSpeed(-500,-500)
        drive.runTasks()
        drive.robot.update()
    


def finish():
    
    drive.addTask(planBTimer(drive))
    
    drive.toPos(vec2(110,60), connect=[False,True], backwards=True, tolerance=5)
    #drive.circleToPos(vec2(110,55), connect=[False,True], backwards=True)
    drive.circleToPos(vec2(65,62), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(55,84), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(20,84), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(20,52), connect=[True,True], backwards=True)
    drive.toPos(vec2(20,0),connect=[True,False], backwards=True)

    drive.rotate(90)
def bear_rescue():
    #print(drive.robot.hub.m_hub.system.info())
    drive.robot.addDevice(motor(Port.B))
    drive.robot.addDevice(motor(Port.F))
    drive.robot.addDevice(Ultrasonic(Port.D))
    drive.robot.addDevice(Ultrasonic(Port.A))
    
    drive.robot.hub.resetAngle()
    
    drive.setDefaultMode()
    drive.setMotorsToDef()

    bearsetup()
    close()
    drive.robot.hub.addOffset(-90)
    drive.robot.pos = vec2(17,13)
    #close()
    drive.robot.hub.colorAnimate([Color.MAGENTA, Color.NONE,Color.WHITE, Color.NONE], 100)
    while not drive.robot.hub.isButtonPressed(Button.CENTER):
        pass
    drive.robot.hub.color(Color.MAGENTA)
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(-90)
    
    #drive.robot.pos = vec2(30,14)
    
    #drive.setFastMode()
    #drive.toPos(vec2(29,65), connect=[False,True])
    #drive.toPos(vec2(90,30), connect=[False,True],backwards=True)
    #drive.toPos(vec2(130,100))
    #drive.setDefaultMode()
    #wait(500)
    #print(drive.robot.pos)
    
    start()
    while not bear():
        drive.stopTasks()
        openCompletely()
        drive.rotate(90)
        gotbear = False
        sken(distance = 256, value = 155, sample=10)
        drive.stopTasks()
        drive.robot.stop()
        hunt()
        drive.stopTasks()

        drive.robot.stop()
        if drive.robot.pos.y > 249 and drive.robot.pos.x < 109:
            drive.toPos(drive.robot.pos + vec2(20,-10),backwards=True)
        if drive.robot.pos.y < 110 or  (drive.robot.pos.x < 90 and drive.robot.pos.y < 180):
            drive.toPos(vec2(115,160.1), backwards=True)
        elif drive.robot.pos.y < 110 or  drive.robot.pos.x < 90:
            drive.toPos(vec2(115,157.1), backwards=True)
        drive.rotate(90)
    closeCompletely()   
    finish()
    drive.straight(-1000, speed=1000, backwards=True)
    raise SystemExit("Bear rescued!")