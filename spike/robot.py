from pybricks.parameters import *
from pybricks.pupdevices import *
from pybricks.hubs import PrimeHub
from maths import *
from umath import pi

    

class rdevice:
    def __init__(self, port: Port):
        self.port = port


class robot:
    def __init__(self, leftPort, rightPort,wDiameter, pos = vec2(0,0)):
        self.hub = hub()
        self.lM = motor(leftPort)
        self.rM = motor(rightPort)
        self.devices = []
        self.pos = pos
        self.Diameter = wDiameter
        
    def setSpeed(self, lSpeed: float, rSpeed: float):
        self.lM.setSpeed(-lSpeed)
        self.rM.setSpeed(rSpeed)
        pass
    def stop(self, brake = True):
        if brake:
            self.lM.brake()
            self.rM.brake()
        else:
            self.lM.stop()
            self.rM.stop()
        pass
    
    def addDevice(self, device:rdevice):
        self.devices.append(device)
        
    def update(self):
        self.pos += navigate(self.lM, self.rM, self.hub, self.Diameter)
    pass

class motor(rdevice):
    def __init__(self, port: Port):
        super().__init__(port)
        self.m_motor = Motor(port)
        self.lastAngle = self.angleRad()
        self.deltaAngle = 0
        
    def setSpeed(self, speed: float):
        self.m_motor.run(speed)
        pass

    def stop(self):
        self.m_motor.stop()
        pass
    
    def Update(self):
        self.deltaAngle = self.angleRad() - self.lastAngle
        self.lastAngle = self.angleRad()
        #print("deltaAngle: ", self.deltaAngle, " | ", self.angleRad(), " | ", self.lastAngle, " ",pi)
        pass
    
    def brake(self):
        self.m_motor.brake()
        pass
    

    
    def angle(self):
        return float(self.m_motor.angle())
    def angleRad(self):
        return float(self.m_motor.angle())/180 * pi

class hub:
    def __init__(self):
        self.m_hub = PrimeHub()
        self.m_hub.display.pixel(0,0)
        self.angleOffset = 0
        self.resetAngle()
    def angle(self):
        return self.m_hub.imu.rotation(Axis.Z) - self.angleOffset
    def angleRad(self):
        return (self.m_hub.imu.rotation(Axis.Z) - self.angleOffset) / 180 * pi
    def resetAngle(self):
        self.angleOffset = self.m_hub.imu.rotation(Axis.Z)

def navigate(lM:motor, rM:motor, hub:hub, diameter):
    scalar = (-lM.deltaAngle + rM.deltaAngle) / 4 * diameter
    vec = scalar * mat2.rotation(-hub.angleRad()) * vec2(1, 0)
    lM.Update()
    rM.Update()
    
    return vec