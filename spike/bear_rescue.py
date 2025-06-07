from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *

def bear():
    if drive.robot.devices[3].distance() > 30:
        return True
    return False

def start():
    drive.circleToPos(vec2(17,75), connect=[False,True])
    drive.circleToPos(vec2(60,75), connect=[True,True])
    drive.circleToPos(vec2(60,65), connect=[True,True])
    drive.circleToPos(vec2(110,65), connect=[True,True])
    drive.circleToPos(vec2(115,100), connect=[True,True])
    drive.circleToPos(vec2(117,155), connect=[True,False])
    drive.open(background=False)
    drive.rotate(90)
    drive.stopTasks()

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
    #drive.robot.pos = vec2(17,11.3)
    #drive.robot.hub.addOffset(-90)
    drive.setDefaultMode()
    drive.setMotorsToDef()
    
    
    
    
    drive.close()
    
    drive.robot.hub.colorAnimate([Color.MAGENTA, Color.NONE,Color.WHITE, Color.NONE], 100)
    while not drive.robot.hub.isButtonPressed(Button.CENTER):
        pass
    drive.robot.hub.color(Color.MAGENTA)
    start()
    while not bear():
        drive.open()
        drive.gotbear = False
        drive.sken(distance = 250, value = 175, sample=10)
        drive.stopTasks()
        drive.robot.stop()
        drive.hunt(distance = 105)
        drive.stopTasks()
        drive.robot.stop()
        print(drive.robot.pos)
        if drive.robot.pos.y < 130 or  drive.robot.pos.x < 90:
            drive.toPos(vec2(115,160), backwards=True)
        drive.rotate(90)
        
    finish()
    raise SystemExit
    drive.toPos(vec2(120,210))

    
    if bear():
        drive.close()
        finish()
        raise SystemExit

    # chytani tak nejak
    drive.toPos(vec2(115,260),background=True)
    while drive.isTasksRunning() and not drive.robot.devices[2].distance() < 200 and not bear():
        drive.runTasks()
    drive.stopTasks()
    drive.robot.stop()

    if (drive.robot.pos - vec2(115,260)).length() < 2 and not bear():
        drive.toPos(vec2(15,drive.robot.pos.y),background=True)
        while drive.isTasksRunning() and not bear:
            drive.runTasks()
        drive.close()
        drive.toPos(vec2(115,150),backwards=True)
    elif not bear():
        drive.toPos(vec2(15,drive.robot.pos.y),background=True)
        while drive.isTasksRunning() and not bear():
            drive.runTasks()
        drive.close()
        drive.toPos(vec2(115,150),backwards=True)
    elif bear():
        drive.close()
        drive.toPos(vec2(115,150),backwards=True)

    finish()

    wait(1000)
    print(drive.robot.pos, " | ", drive.robot.hub.angle(),"°")
    wait(1000)