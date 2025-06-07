from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *

#setup class
drive.hook_speeds = [1, -1]

def hook_align(speed = 500):
    drive.robot.devices[0].setSpeed(-speed)
    drive.robot.devices[1].setSpeed(speed)
    wait(1000)  # wait for hooks to align
    drive.robot.devices[0].stop()
    drive.robot.devices[1].stop()
    drive.setMotorsToDef()

def hook_setup():
    drive.turnMotor(0, 130, simple=True)
    drive.turnMotor(1, -130, simple=True)

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
        
def car_sken(pos, distance = 20): ##otestovat!
    for i in range (4):
        drive.toPos(vec2((pos.x + distance * i)*drive.side, pos.y), speed = cspeed, backwards=True)
        print("car sken", i, drive.robot.devices[3].color())
        if drive.robot.devices[3].color() == drive.side_color:
            return i

#hook class
def hook_pickup(): ##otestovat!
    drive.turnMotor(0, 300, simple=True)
    drive.turnMotor(1, -300, simple=True)
    drive.hooks = [True, True]

def hook_drop(N: int):
    N = clamp(N, 0, 1)
    drive.turnMotor(N, 100 * drive.hook_speeds[N], simple=True)
    drive.hooks[N] = False

def battery_pickup(pickup_pos):
    hook_setup()
    drive.toPos(vec2(pickup_pos.x  * drive.side, pickup_pos.y - 5), speed = cspeed, backwards=True)
    drive.rotate(-90)
    drive.straight(5)
    hook_pickup()

def battery_delivery(car_number, Starting_pos = vec2(85, 35), car_distance = 20, hook_shift = 3): #75 22
    if drive.hooks[0] == True:
        N = 0
        hook = -hook_shift
    elif drive.hooks[1] == True:
        N = 1
        hook = hook_shift
    else:
        return False
    drive.toPos(vec2((Starting_pos.x + car_number * car_distance + hook)*drive.side, Starting_pos.y), speed = cspeed, backwards=True)
    hook_drop(N)
    return(True)

#main class
cspeed = 750
def m1():
    #start
    #drive.circleToPos(vec2(50, 70), connect=[False, True], speed = cspeed, backwards=True)
    #drive.straight(5, backwards=False, speed = cspeed)
    drive.toPos(vec2(60 * drive.side, 40), speed = cspeed, backwards=True)
    drive.toPos(vec2(50 * drive.side, 160), backwards=False, speed = cspeed)

    #ninja moves
    drive.rotate(45)
    hook_align()
    drive.rotate(90)
    drive.toPos(vec2(50 * drive.side, 165))

    #zarovnání zpět
    drive.toPos(vec2(50 * drive.side, 30), backwards = False)
    #nájezd na křižovatku m1 m2
    #drive.circleToPos(vec2(100  * drive.side, 40), connect=[False, True], speed = cspeed, backwards=True)
    drive.toPos(vec2(100 * drive.side, 40), speed = cspeed, backwards=True)

def m2():
    #nájezd na auta
    car_N = car_sken(vec2(83 ,36), 20)
    print(car_N)
    battery_shift = 0
    cars = [car_N, 4, 5, 6, 7]
    cars.pop(len(cars) - 1 - car_N)  # remove car_N from the list
    print("cars", cars)
    
    for car in cars:
        if battery_delivery(car) == False:
            battery_pickup(vec2(144 * drive.side, 40 + battery_shift))  # pickup position
            battery_shift += 6
            ### | dodělat! + check?
            battery_delivery(car)
def m3():
    pass

def mF():
    drive.toPos(vec2(20 * drive.side, 30))

#main 
def Roadmain1():
    hook_align()
    wait(1000)  # wait for hooks to align
    hook_setup()
    wait(1000)  # wait for hooks to setup
    hook_pickup()
    wait(1000)  # wait for hooks to pick up
    hook_drop(0)
    hook_drop(1)


def Roadmain():    
    roadside_setup(side_decider())
    #m1()
    m2()
    #if enemy_sken() == False:
    #    hook_align()
    #    m2()
    #else:
    #    m3()
    mF()