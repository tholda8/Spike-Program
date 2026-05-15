from maths import *
from setup import *
from umath import *
from robot import *
from pybricks.tools import wait
acc = 100
deacc = 300
defspeed = 80
turnCoeff = pi/12

def toPos(pos, speed = 1000, brake = True):
    offset = r.pos
    #isn't it inpractical to always name robots r?
    #r = robot
    rotMat = mat2.rotation(-atan2((pos-offset).y,(pos-offset).x))
    length = rotMat*(pos - offset)
    swap = sign(length.x - (rotMat*r.pos).x)
    print((rotMat*(r.pos-offset)).x*swap ," < ", length.x*swap)
    while((rotMat*(r.pos-offset)).x*swap < length.x*swap):
        #print(rotMat*(r.pos-offset), r.pos)
        calcDir(rotMat*(r.pos-offset), length.x, calcSpeed(rotMat*r.pos, length.x, speed),swap)
        r.update()
    r.stop(brake)
    
def calcDir(pos, length, speed, swap):
    #angle = r.hub.angleRad() - atan2(pos.y, pos.x)
    a2 = r.hub.angleRad() % (2*pi)
    a1 = atan2(pos.y, pos.x) % (2*pi)
    angle = (a2 - a1 + pi) % (2*pi) - pi
    angle *= swap
    speedM = speed * minV(1-fabs(angle)*turnCoeff,-1)
    #print(r.pos)
    if sign(angle) > 0:
        r.setSpeed(speed, speedM)
        #print("l, ", speed, " ", speedM, " | ", r.pos, " | ", r.hub.angle(), (angle/pi *180))
    else:
        r.setSpeed(speedM, speed)
        #print("p, ", speedM, " ", speed, " | ", r.pos, " | ", r.hub.angle(), (angle/pi *180))


def calcSpeed(pos, length, speed):
    accSpeed = -fabs((pos.x-length/2)*acc) + acc*length/2 + defspeed
    #print(accSpeed, pos.x, length)
    return clamp(fabs(accSpeed), defspeed ,speed) * sign(accSpeed)