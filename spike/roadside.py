from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait
from tester import *

def roadside_setup():
    drive.robot.devices.append(ColorSensor(Port.C)) #??? color sensor class???
    drive.side = 1 # 1 = blue, -1 = red
    if drive.side == 1:
        drive.side_color = Color.BLUE
    else:
        drive.side_color = Color.RED
    #měnič orientace souřadnicového pole, měnič orientace robota
    drive.robot.pos = vec2(12, 50) # reset position

def enemy_sken():
    pass

def car_sken(distance = 5):
    for i in range (4):
        drive.straight(distance)
        if drive.robot.devices[3].color() == drive.side_color:
            return i

def m1():
    #start
    drive.circleToPos(vec2(50, 90), connect=[False, True])
    drive.toPos(vec2(50, 180), connect=[True, False])
    #ninja moves
    drive.rotate(180)
    #zarovnání zpět
    drive.toPos(vec2(50, 10), backwards=True)

def battery_delivery(car_number, L_hook, Starting_pos = vec2(100, 40), car_distance = 5, hook_shift = 3):
    if L_hook == True: #???
        hook = -hook_shift
    else:
        hook = hook_shift
    drive.toPos(vec2(Starting_pos.x + car_number * car_distance + hook, Starting_pos.y))
    #droop battery ### add!

def m2():
    #nájezd na auta
    drive.circleToPos(vec2(100, 40), connect=[False, True])
    car_N = car_sken(10)
    cars = [car_N, 4, 5, 6, 7].remove(car_N + 4)
 