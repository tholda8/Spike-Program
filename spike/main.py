#from bear_rescue import bear_rescue
from audio import megalovania
from down import downFunc
from imgs import *
from spike_lib.screen import Screen, Page
from wroportorico import wroportorico

menu = Screen(drive.robot.hub)
#menu.addPage(Page(wro2, icon=wroimg, image = [fish,fish1], delta = 500))
menu.addPage(Page(wroportorico, icon=wroimg, image = [fish,fish1], delta = 500))
menu.addPage(Page(downFunc, icon=downimg, image = [fish,fish1], delta = 500))
#menu.addPage(Page(vyzvajesenik2, icon=smile, image = [fish,fish1], delta = 500))
#menu.addPage(Page(vyzvajesenik3, icon=sad, image = [fish,fish1], delta = 500))
#menu.addPage(Page(bear_rescue, icon=smile, image=arrow, delta=110))
#menu.addPage(Page(WRO, icon=wroimg, image=arrow, delta=110))
#menu.addPage(Page(test0, icon=test, image=arrow, delta=110))
#menu.addPage(Page(vyzva, icon=vyzvai, image=arrow, delta=110))
menu.addPage(Page(rotate, icon= fish, image = [fish,fish1], delta = 500))
menu.addPage(Page(lambda: play(megalovania, 1), icon=smile, image=[skull, skull,skull, skull, skull2], delta=500))


menu.start()
while True:
    menu.update()

