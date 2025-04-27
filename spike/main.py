from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait

def test():
    drive.toPos(vec2(0,0),backwards=True)
    drive.toPos(vec2(0,10))
    drive.toPos(vec2(30,0))
    drive.toPos(vec2(0,0), backwards=True)
    drive.rotate(0)

drive.setDefaultMode()
# drive.bezier(vec2(0,0), vec2(26,50), vec2(69,-36), vec2(100,0),20) #/\/
drive.bezier(vec2(0,0), vec2(20,32), vec2(40,31), vec2(60,0),20) #/\
test()

wait(1000)
print(r.pos, " | ", r.hub.angle(),"°")
wait(1000)