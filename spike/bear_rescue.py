from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait


def bear():
    if drive.robot.devices[3].distance() > 190:
        return True
    return False

def start():
    drive.circleToPos(vec2(17,65), connect=[False,True])
    drive.circleToPos(vec2(65,65), connect=[True,True])
    drive.circleToPos(vec2(110,65), connect=[True,True])
    drive.open(background=True)
    drive.circleToPos(vec2(115,100), connect=[True,False])

def finish():
    drive.circleToPos(vec2(110,65), connect=[False,True], backwards=True)
    drive.circleToPos(vec2(65,65), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(65,72), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(17,72), connect=[True,True], backwards=True)
    drive.circleToPos(vec2(17,50), connect=[True,True], backwards=True)
    drive.toPos(vec2(17,11.3),connect=[True,False], backwards=True)


def bear_rescue():
    drive.setDefaultMode()
    drive.setMotorsToDef()

    start()

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