from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *

#setup class
def hook_align(speed = 500):
    drive.robot.devices[0].setSpeed(-speed)
    drive.robot.devices[1].setSpeed(speed)
    wait(1000)  # wait for hooks to align
    drive.robot.devices[0].stop()
    drive.robot.devices[1].stop()
    drive.setMotorsToDef()

def side_decider():
    page = 0    
    while True:
        if drive.robot.hub.isButtonPressed(Button.LEFT):
            page = -1
            drive.robot.hub.beep(400, 250)
            drive.robot.hub.color(Color.RED)
        elif drive.robot.hub.isButtonPressed(Button.RIGHT):
            page = 1
            drive.robot.hub.beep(800, 250)
            drive.robot.hub.color(Color.BLUE)
        elif drive.robot.hub.isButtonPressed(Button.CENTER):
            drive.robot.hub.beep(600, 500)
            print("page", page)
            return page

def roadside_setup(side):
    drive.robot.devices.append(ColorSensor(Port.C)) #??? color sensor class???
    drive.hooks = [False, False]
    if side == 1:
        drive.side_color = Color.BLUE
        drive.side = 1
        print("Blue side selected")
    else:
        drive.side_color = Color.RED
        drive.side = -1
        print("Red side selected")
        #drive.robot.lM.reverse = False
        #drive.robot.rM.reverse = True
    drive.robot.pos = vec2(11 * drive.side, 33) # reset position
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(180)  # set angle offset
    print(drive.robot.pos, drive.robot.hub.angle())
    hook_align(-500)

#sken class
def enemy_sken(ang = 0, val = 150): 
    drive.rotate(ang, 1000)
    for i in range(5):
        if drive.robot.devices[2].distance > val:
            wait(1000) ### domyslet!
        else:
            return False
    return True
        
def car_sken(distance = 5): ##otestovat!
    for i in range (4):
        drive.straight(distance, backwards=True)
        if drive.robot.devices[3].color() == drive.side_color:
            return i

#hook class
def hook_pickup(): ##otestovat!
    drive.robot.devices[0].target(500)
    drive.robot.devices[1].target(-500)
    drive.hooks = [True, True]

def hook_drop(N: int):
    N = clamp(N, 0, 1)
    drive.robot.devices[N].target
    drive.hooks[N] = False

def battery_pickup(pickup_pos):
    drive.toPos(vec2(pickup_pos.x  * drive.side, pickup_pos.y - 5), speed = cspeed, backwards=True)
    drive.rotate(-90)
    drive.straight(5)
    hook_pickup()

def battery_delivery(car_number, Starting_pos = vec2(100, 40), car_distance = 5, hook_shift = 3):
    if drive.hooks[0] == True:
        N = 0
        hook = -hook_shift
    elif drive.hooks[1] == True:
        N = 1
        hook = hook_shift
    else:
        return False
    drive.toPos(vec2(Starting_pos.x + car_number * car_distance + hook, Starting_pos.y), speed = cspeed, backwards=True)
    hook_drop(N)
    return(True)

#main class
cspeed = 800
def m1():
    #start
    #drive.circleToPos(vec2(50, 70), connect=[False, True], speed = cspeed, backwards=True)
    #drive.straight(5, backwards=False, speed = cspeed)
    
    drive.toPos(vec2(60 * drive.side, 30), speed = cspeed, backwards=True)
    
    drive.toPos(vec2(50 * drive.side, 160), backwards=False, speed = cspeed)
    #ninja moves
    drive.rotate(220)
    #zarovnání zpět
    ###?
    drive.toPos(vec2(50 * drive.side, 15), backwards = False)
    #nájezd na křižovatku m1 m2
    drive.circleToPos(vec2(100  * drive.side, 40), connect=[False, True], speed = cspeed, backwards=True)

def m2():
    #nájezd na auta
    car_N = car_sken(10)
    cars = [car_N, 4, 5, 6, 7].remove(car_N + 4)
    for car in cars:
        if battery_delivery(car) == False:
            battery_pickup("?")
            ### | dodělat! + check?
            battery_delivery(car)
def m3():
    pass

def mF():
    drive.toPos(vec2(20 * drive.side, 30))

#main 
def Roadmain():    
    roadside_setup(side_decider())
    m1()
    #if enemy_sken() == False:
    #    hook_align()
    #    m2()
    #else:
    #    m3()
    mF()