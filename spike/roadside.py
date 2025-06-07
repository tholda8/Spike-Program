from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *

#setup class
def hook_align():
    drive.robot.devices[0].run(100)
    drive.robot.devices[1].run(-100)
    wait(1000)  # wait for hooks to align
    drive.device[0].stop()
    drive.device[1].stop()
    drive.setMotorsToDef()

def roadside_setup():
    drive.robot.devices.append(ColorSensor(Port.C)) #??? color sensor class???
    drive.side = 1 # 1 = blue, -1 = red
    drive.hooks = [False, False]
    if drive.side == 1:
        drive.side_color = Color.BLUE
    else:
        drive.side_color = Color.RED
    ###měnič orientace souřadnicového pole, měnič orientace robota
    drive.robot.pos = vec2(12, 50) # reset position
    hook_align()

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
        drive.straight(distance)
        if drive.robot.devices[3].color() == drive.side_color:
            return i

#hook class
def hook_pickup(): ##otestovat!
    drive.robot.devices[0].target(100)
    drive.robot.devices[1].target(-100)
    drive.hooks = [True, True]

def hook_drop(N: int):
    N = clamp(N, 0, 1)
    drive.robot.devices[N].target
    drive.hooks[N] = False

def battery_pickup(pickup_pos):
    drive.toPos(vec2(pickup_pos.x, pickup_pos.y - 5))
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
    drive.toPos(vec2(Starting_pos.x + car_number * car_distance + hook, Starting_pos.y))
    hook_drop(N)
    return(True)

#main class
def m1():
    #start
    drive.circleToPos(vec2(50, 90), connect=[False, True])
    drive.toPos(vec2(50, 180), connect=[True, False])
    ###ninja moves
    drive.rotate(180)
    #zarovnání zpět
    ###?
    drive.toPos(vec2(50, 10), backwards=True)
    #nájezd na křižovatku m1 m2
    drive.circleToPos(vec2(100, 40), connect=[False, True])

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
    drive.toPos(vec2(20, 30))

#main 
roadside_setup()
m1()
if enemy_sken() == False:
    m2()
else:
    m3()
mF()