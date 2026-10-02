from setup import drive
from resources.megalovania import megalovania
from down import downFunc
from resources.imgs import wroimg, fish, fish1, smile, skull, skull2, downimg, play, rotate
from spike_lib.screen import Screen, Page
from wroportorico import wroportorico
from calibration import calibration, calibrationI

menu = Screen(drive.robot.hub)
menu.addPage(Page(wroportorico, icon=wroimg, image = [fish,fish1], delta = 500))
menu.addPage(Page(downFunc, icon=downimg, image = [fish,fish1], delta = 500))
menu.addPage(Page(rotate, icon= fish, image = [fish,fish1], delta = 500))
menu.addPage(Page(lambda: play(megalovania, 1), icon=smile, image=[skull, skull,skull, skull, skull2], delta=500))
menu.addPage(Page(calibration, icon=calibrationI, image=[fish,fish1], delta=500))

menu.start()
while True:
    menu.update()

