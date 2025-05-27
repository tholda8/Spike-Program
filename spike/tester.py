from setup import *  
from math import *                                                                                                                                                                                                                                                                            
from pybricks.tools import wait


def bearsetup(self):
    self.gotbear = False

def hunter(self, value=40):
    if self.robot.devices[3].distance() < value:
        self.close()
        self.stop()
        self.gotbear = True
        return True
    
def skener(self, uvalues, sample = 10, value=40):
    uvalues.append(self.robot.devices[2].distance())
    if len(uvalues) > sample:
        uvalues.pop(0)
    if avr(uvalues) > value:
        self.stop()
        return True
      
def sken(self, distance, value, sample=10):
    uvalues = []
    self.straight(distance, backround=True)
    while self.isTaskRunning():
        if self.hunter() or self.skener(uvalues, sample, value):
            return None
        self.runTask()
        
def hunt(self, distance):
    if self.gotbear:
        return None
    self.straight(distance, backround=True)
    while self.isTaskRunning():
        if self.hunter():
            return None
        self.runTask()

def ultrasign(distance):
    statistic = []
    for i in range(100):
        print()
    drive.straight(distance, background=True,speed=500)
    while drive.isTasksRunning():
        statistic.append(drive.robot.devices[2].distance())
        drive.runTasks()
    return statistic

#statistic = ultrasign(120)

#with open("statistic.txt", "a") as f:
#    for line in statistic:
#        f.write(str(line)+"\n")

# for line in statistic:
#     print(line)
# drive.toPos(vec2(0,0), backwards=True)
# drive.rotate(0)
# drive.setMotorsToDef()
# drive.close(background=True)
# drive.straight(20,speed=100)

wait(1000)
print(drive.robot.pos, " | ", drive.robot.hub.angle(),"°")
wait(1000)