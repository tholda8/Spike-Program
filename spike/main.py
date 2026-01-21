
from imgs import *
from screen import *
from vyzva import *


menu = Screen(drive.robot.hub)
menu.addPage(Page(vyzva, icon=vyzvai, image=arrow, delta=110))
menu.addPage(Page(rotate, icon= fish, image = [fish,fish1], delta = 500))
menu.addPage(Page(lambda: play(megalovania, 1), icon=smile, image=[skull, skull,skull, skull, skull2], delta=500))

menu.start()
while True:
    menu.update()


