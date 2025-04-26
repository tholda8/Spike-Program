from pybricks.parameters import *
from maths import *
from driveFunc import driveManager
from robot import robot

r = robot(Port.B, Port.A, 5.7)
drive = driveManager(r)