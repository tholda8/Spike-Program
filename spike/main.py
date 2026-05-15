from bear_rescue import bear_rescue
from imgs import *
from screen import *
from vyzva import *
from wro import *



menu = Screen(drive.robot.hub)
menu.addPage(Page(WRO, icon=wroimg, image=arrow, delta=110))
menu.addPage(Page(bear_rescue, icon=smile, image=arrow, delta=110))
menu.addPage(Page(test0, icon=test, image=arrow, delta=110))
menu.addPage(Page(vyzva, icon=vyzvai, image=arrow, delta=110))
menu.addPage(Page(rotate, icon= fish, image = [fish,fish1], delta = 500))
menu.addPage(Page(lambda: play(megalovania, 1), icon=smile, image=[skull, skull,skull, skull, skull2], delta=500))


menu.start()
while True:
    menu.update()


