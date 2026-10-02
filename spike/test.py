from pybricks.parameters import Button, Port
from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub

m = Motor(Port.A)

hub = PrimeHub()

while True:
    if Button.LEFT in hub.buttons.pressed():
        m.run(-1000)
    elif Button.RIGHT in hub.buttons.pressed():
        m.run(1000)