from setup import *    
from umath import atan2, pi


def slalom():
    drive.toPos(vec2(30,15))
    drive.rotate(0)
    max = 1000
    acc = 0.5
    drive.defspeed = 400
    drive.circleToPos(vec2(45,0), connect=[False,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(60,-15),connect=[True,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(75,0),connect=[True,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(90,15),connect=[True,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(105,0),connect=[True,True], speed = max, accuracy=acc)
    drive.setDefaultMode()
    drive.toPos(vec2(105,-15), connect=[True,False])

def slalomRev():
    drive.toPos(vec2(15,30))
    drive.rotate(90)
    max = 1000
    acc = 0.5
    drive.defspeed = 400
    drive.circleToPos(vec2(0,45), connect=[False,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(-15,30),connect=[True,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(-30,15),connect=[True,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(-45,30),connect=[True,True], speed = max, accuracy=acc)
    drive.circleToPos(vec2(-60,45),connect=[True,True], speed = max, accuracy=acc)
    drive.setDefaultMode()
    drive.toPos(vec2(-75,45), connect=[True,False])
    
def sprint():
    drive.toPos(vec2(30,15))
    drive.rotate(0)

    drive.toPos(vec2(30*20,0), background=True)
    red = False
    while not drive.robot.pos.x >= 120:
        drive.runTasks()
    drive.stopTasks()
    drive.robot.stop(False)
    drive.straight(15)

def sprintRev():
    drive.toPos(vec2(0,15))
    drive.rotate(180)

    drive.toPos(vec2(-30*20,0), background=True)
    red = False
    while not drive.robot.pos.x <= -120:
        drive.runTasks()
    drive.stopTasks()
    drive.robot.stop(False)
    drive.straight(15)

def down(background=False):
    drive.turnMotor(0, 120, background=background)  

def up(background=False):
    drive.turnMotor(0, 0, background=background)

def mid(background=False):
    drive.turnMotor(0, 85, background=background)

def medved():
    down(True)
    drive.toPos(vec2(30,15))
    drive.rotate(0)
    drive.toPos(vec2(60,15))
    drive.circleToPos(vec2(75,0))
    drive.toPos(vec2(75,-35))
    
    up(True)
    drive.toPos(vec2(75,0), backwards=True)
    drive.rotate(90)
    drive.circleToPos(vec2(45,0))
    drive.toPos(vec2(45,-15))
    
def medvedRev():
    down(True)
    drive.toPos(vec2(15,30))
    drive.rotate(90)
    drive.circleToPos(vec2(45,30))
    
    drive.toPos(vec2(45,-10))
    up(True)
    drive.toPos(vec2(45,45), backwards=True)
    drive.toPos(vec2(-15,45))    

def kulicky():
    mid(True)
    drive.defspeed = 400
    drive.toPos(vec2(15,15))
    drive.rotate(-90)
    s = 10
    
    drive.straight(s)
    drive.straight(-s, backwards=True)
    
    drive.toPos(vec2(45,15))
    drive.rotate(-90)
    
    drive.straight(s)
    drive.straight(-s, backwards=True)
    
    drive.toPos(vec2(75,15))
    drive.rotate(-90)
    
    drive.straight(s)
    
    up(True)
    drive.toPos(vec2(75,45), backwards=True)
    
    drive.setDefaultMode()

def kulickyRev():
    mid(True)
    drive.defspeed = 400
    drive.toPos(vec2(15,-15))
    drive.rotate(-90)
    s = 10
    
    drive.straight(s)
    drive.straight(-s, backwards=True)
    
    drive.toPos(vec2(-15,-15))
    drive.rotate(-90)
    
    drive.straight(s)
    drive.straight(-s, backwards=True)
    
    drive.toPos(vec2(-45,-15))
    drive.rotate(-90)
    
    drive.straight(s)
    drive.straight(-s, backwards=True)
    up()
    drive.setDefaultMode()

def checkWall():
    drive.robot.hub.beep(220, 40)
    
    if drive.robot.devices[1].distance() < 15:
        drive.robot.hub.beep(220, 40)
        return True
    
    return False

def bludiste():
    field = [[0,0,0],[0,0,0],[0,0,0]]
    pos : vec2 = vec2(0,2)
    end = vec2(2,0)
    
    def printField(field, pos):
        for y in range(len(field) - 1, -1, -1):
            print([2 if (x, y) == (int(pos.x), int(pos.y)) else field[x][y] for x in range(len(field[0]))])

    def toPos(pos : vec2):
        drive.toPos(vec2(pos.x*30+45, pos.y*30-45))
    
    drive.defspeed = 400


    toPos(pos)  
    while pos != end:
        printField(field, pos)
        next : vec2 = nextMove(field, pos, end)
        
        if next.x == -1 and next.y == -1:
            field = [[0,0,0],[0,0,0],[0,0,0]]
            next = nextMove(field, pos, end)
        
        angle = atan2((next.y - pos.y), (next.x - pos.x))
        print("Next:", next, "Angle:", angle*180/pi)
        drive.rotateRad(angle)
        
        if checkWall():
            field[int(next.x)][int(next.y)] = 1
        else:
            toPos(next)
            pos = next
    toPos(pos + vec2(1, 0))    
    
def bludisteRev():
    field = [[0,0,0],[0,0,0],[0,0,0]]
    pos : vec2 = vec2(2,0)
    end = vec2(0,2)
    
    def printField(field, pos):
        for y in range(len(field) - 1, -1, -1):
            print([2 if (x, y) == (int(pos.x), int(pos.y)) else field[x][y] for x in range(len(field[0]))])

    def toPos(pos : vec2):
        drive.toPos(vec2(pos.x*30 - 75, pos.y*30 + 15))
    
    drive.defspeed = 400


    toPos(pos)  
    while pos != end:
        printField(field, pos)
        next : vec2 = nextMove(field, pos, end)
        
        if next.x == -1 and next.y == -1:
            field = [[0,0,0],[0,0,0],[0,0,0]]
            next = nextMove(field, pos, end)
        
        angle = atan2((next.y - pos.y), (next.x - pos.x))
        print("Next:", next, "Angle:", angle*180/pi)
        drive.rotateRad(angle)
        
        if checkWall():
            field[int(next.x)][int(next.y)] = 1
        else:
            toPos(next)
            pos = next
    toPos(pos - vec2(1, 0)) 

def nextMove(field, start :vec2, end :vec2) -> vec2:
    start_xy = int(start.x), int(start.y)
    end_xy = int(end.x), int(end.y)
    if start_xy == end_xy:
        return start
    q = [start_xy]
    prev: dict[tuple[int, int], tuple[int, int] | None] = {start_xy: None}
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    max_x = len(field)
    max_y = len(field[0]) if field else 0

    def in_bounds(x, y):
        return 0 <= x < max_x and 0 <= y < max_y

    while q:
        x, y = q.pop(0)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not in_bounds(nx, ny):
                continue
            # field is indexed as field[x][y]
            if field[nx][ny] == 1:  # wall
                continue
            if (nx, ny) in prev:
                continue
            prev[(nx, ny)] = (x, y)
            if (nx, ny) == end_xy:
                q.clear()
                break
            q.append((nx, ny))

    if end_xy not in prev:
        drive.robot.hub.beep(440, 200)
        drive.robot.hub.beep(220, 200)
        drive.robot.hub.beep(440, 200)
        return vec2(-1, -1)  # no path found

    # reconstruct one step from end back to start
    cur = end_xy
    while True:
        parent = prev.get(cur)
        if parent is None or parent == start_xy:
            break
        cur = parent
    return vec2(cur[0], cur[1])

def allignePos():
    pos = drive.robot.pos 
    pos = vec2(pos.x%30, pos.y%30)
    print("Before align:", pos)
    halfs = round(drive.angleDiff(0,drive.robot.hub.angleRad())/(pi/2))
    drive.robot.pos = pos
    drive.robot.hub.addOffset(halfs*90)
    

def vyzvainit():
    drive.robot.hub.m_hub.light.on(Color.RED)
    #drive.robot.hub.m_hub.system.set_stop_button(Button.CENTER)
    wait(10000)

def mbludiste():
    vyzvainit()
    bludiste()

def msprint():
    vyzvainit() 
    sprint()

def mslalom():
    vyzvainit()
    slalom()

def mmedved():
    vyzvainit()
    medved()

def mkulicky():
    vyzvainit()
    kulicky()

def vyzva():
    bludiste()

    pass