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
    print("Hooks aligned")

def hook_setup(angle = 130, speed = -500):
    print("Hook setuping")
    drive.turnMotor(0, angle, speed, simple=True)
    drive.turnMotor(1, -angle, speed, simple=True)

def side_decider():
    page = 0    
    while True:
        if drive.robot.hub.isButtonPressed(Button.LEFT):
            page = -1 #-1
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
    drive.robot.devices.append(ColorSensor(Port.C))
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
    drive.robot.pos = vec2(11, 33 * drive.side) # reset position
    drive.robot.hub.resetAngle()
    drive.robot.hub.addOffset(180)  # set angle offset
    print(drive.robot.pos, drive.robot.hub.angle())
    #hook_align(-500)

#sken class
def enemy_sken(ang = 180, val = 150, patience = 5, sample = 500): 
    drive.rotate(ang, 500)
    strike = 3
    for j in range(patience):
        for z in range(sample):
            if drive.robot.devices[2].distance() < val:
                drive.robot.hub.beep(1000, 200)
                wait(500) ### domyslet!
                strike += 1
                break
        strike -= 1
        wait(500)
        print("strike", strike)
        if strike == 0:
            return False
    drive.robot.hub.beep(1300, 500)
    return True

        
def car_sken(pos, distance = 20): ##otestovat!
    for i in range (4):
        enemy_sken(ang=180, val=70, sample=5)  # check for enemy robots
        drive.toPos(vec2((pos.x + distance * i), pos.y * drive.side), speed = cspeed, backwards=True)
        color = drive.robot.devices[3].color()
        c = 0
        while color == Color.NONE:
            c += 1
            drive.toPos(vec2((pos.x + distance * i + c), (pos.y - c)  * drive.side), speed = cspeed, backwards=True)
            drive.rotate(180, 500)
            color = drive.robot.devices[3].color()
        print("color", i, color)
        if color == drive.side_color:
            return i

def ultra_align(shift = 5):
    drive.rotate(180, 1000)  # rotate to align with the ultrasonic sensor
    x = drive.robot.devices[2].distance  # get the distance from the ultrasonic sensor
    drive.rotate(-90 * drive.side, 1000)  # rotate to align with the battery pickup position
    y = drive.robot.devices[2].distance  # get the distance from the ultrasonic sensor
    drive.robot.pos = vec2((x + shift), (y + shift) * drive.side)  # set the robot position

#hook class
def hook_pickup(): ##otestovat!
    hook_setup(300)
    drive.hooks = [True, True]

def hook_drop(N: int):
    N = clamp(N, 0, 1)
    drive.turnMotor(N, 100 * drive.hook_speeds[N], simple=True)
    drive.hooks[N] = False

def battery_pickup(pickup_pos):
    hook_setup()
    drive.toPos(vec2(pickup_pos.x, (pickup_pos.y - 13)  * drive.side), speed = cspeed)
    drive.rotate(90 * drive.side)
    drive.toPos(vec2(pickup_pos.x, pickup_pos.y * drive.side), speed = cspeed)
    hook_pickup()

def battery_delivery(car_number, Starting_pos = vec2(80, 35), car_distance = 20, hook_shift = 2, both = False): #75 22
    if drive.hooks[0] == True:
        N = 0
        hook = hook_shift
    elif drive.hooks[1] == True:
        N = 1
        hook = -hook_shift
    else:
        return False
    drive.toPos(vec2((Starting_pos.x + car_number * car_distance + hook), Starting_pos.y * drive.side), speed = 500)
    drive.rotate(-90 * drive.side, 500)
    if both == False:
        hook_drop(N)
    else:
        hook_setup()
    drive.toPos(vec2((Starting_pos.x + car_number * car_distance + hook), (Starting_pos.y+10) * drive.side), speed = 500, backwards=True)
    hook_setup(300)
    return(True)

#main class
cspeed = 750
def m1():
    #start
    #drive.circleToPos(vec2(50, 70), connect=[False, True], speed = cspeed, backwards=True)
    #drive.straight(5, backwards=False, speed = cspeed)
    drive.toPos(vec2(60, 40 * drive.side), speed = cspeed, backwards=True)
    drive.toPos(vec2(50, 160 * drive.side), backwards=False, speed = cspeed)

    #ninja moves
    drive.rotate(45 * drive.side)
    #hook_align()
    #drive.rotate(90)
    #drive.toPos(vec2(50, 165 * drive.side))

    #zarovnání zpět
    drive.toPos(vec2(50, 50 * drive.side), backwards = False)
    #nájezd na křižovatku m1 m2
    #drive.circleToPos(vec2(100  * drive.side, 40), connect=[False, True], speed = cspeed, backwards=True)
    #drive.toPos(vec2(50, 50 * drive.side), speed = cspeed, backwards=True)

def m2():
    #nájezd na auta
    car_N = car_sken(vec2(81 ,34), 20)
    hook_align()
    hook_setup()
    print(car_N)
    battery_shift = 0
    cars = [car_N, 4, 5, 6, 7]
    cars.pop(len(cars) - 1 - car_N)  # remove car_N from the list
    print("cars", cars)
    
    for car in cars:
        if battery_delivery(car) == False:
            print("pickup")
            battery_pickup(vec2(142, (48 + battery_shift)))  # pickup position
            battery_shift += 6
            ### | dodělat! + check?
            battery_delivery(car)

def m22():
    #nájezd na auta
    car_N = car_sken(vec2(81 ,34), 20)
    hook_align()
    hook_setup()
    print(car_N)
    battery_shift = 0
    cars = [car_N, 4, 5, 6, 7]
    cars.pop(len(cars) - 1 - car_N)  # remove car_N from the list
    print("cars", cars)
    
    car = cars[0]
    if battery_delivery(car, both = True) == False:
        print("pickup")
        battery_pickup(vec2(142, (48 + battery_shift)))  # pickup position
        battery_shift += 6
        ### | dodělat! + check?
        battery_delivery(car)

def m3():
    pass

def mF():
    drive.toPos(vec2(25, 40 * drive.side))

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

def shortroad():
    roadside_setup(side_decider())
    m1()
    mF()

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

def ultraroad():
    m1()
    m22()
    #if enemy_sken() == False:
    #    hook_align()
    #    m2()
    #else:
    #    m3()
    mF()