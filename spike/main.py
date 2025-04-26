from setup import *                                                                                                                                                                                                                                                                                
from pybricks.tools import wait

def test():
    drive.toPos(vec2(0,10))
    drive.toPos(vec2(30,0))
    drive.toPos(vec2(0,0), backwards=True)
    drive.rotate(0)

# drive.setPreciseMode()
# test()

drive.setDefaultMode()
test()

# drive.setFastMode()
# test()

# drive.setAggressiveMode()
# test()

# drive.straight(20)

wait(1000)
print(r.pos, " | ", r.hub.angle(), "°")
wait(1000)