
from imgs import *
from Device_manager.screen import *
from vyzva import *
from wro2026 import *

menu = Screen(drive.robot.hub)
menu.addPage(Page(wro, icon=vyzvai, image=arrow, delta=110))
menu.addPage(Page(vyzva, icon=vyzvai, image=arrow, delta=110))
menu.addPage(Page(msprint, icon=rovni, image=arrow, delta=110))
menu.addPage(Page(mslalom, icon=slalomi, image=arrow, delta=110))
menu.addPage(Page(mmedved, icon=medvedi, image=arrow, delta=110))
menu.addPage(Page(mkulicky, icon=kulickyi, image=arrow, delta=110))
menu.addPage(Page(mbludiste, icon=labirinti, image=arrow, delta=110))
menu.addPage(Page(rotate, icon= fish, image = [fish,fish1], delta = 500))
menu.addPage(Page(lambda: play(megalovania, 1), icon=smile, image=[skull, skull,skull, skull, skull2], delta=500))


menu.start()
while True:
    menu.update()


