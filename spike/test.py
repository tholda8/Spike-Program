from pybricks.parameters import *
from pybricks.pupdevices import *
from pybricks.hubs import PrimeHub
from maths import *
from umath import pi
from pybricks.tools import *

m = Motor(Port.A)

hub = PrimeHub()

while True:
    if Button.LEFT in hub.buttons.pressed():
        m.run(-1000)
    elif Button.RIGHT in hub.buttons.pressed():
        m.run(1000)