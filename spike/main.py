
from driveFunc import *
from setup import *
from maths import *
from pybricks.tools import wait

 
print("start")

toPos(vec2(10,10), 400) 
wait(1000)
print(r.pos)
#toPos(vec2(0,10), 400) 
r.update()
wait(1000)
                    