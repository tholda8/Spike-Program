from pybricks.hubs import PrimeHub
from spike.resources.imgs import *
from spike_lib.screen import *
from test import Itest, test
from spike_lib.robot import Hub

print("Starting program")
menu = Screen(Hub())
menu.addPage(Page(test, icon=Itest, image=arrow, delta=110))


menu.start()
while True:
    menu.update()


