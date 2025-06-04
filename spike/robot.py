from pybricks.parameters import *
from pybricks.pupdevices import *
from pybricks.hubs import PrimeHub
from maths import *
from umath import pi
from pybricks.tools import *
    

class rdevice:
    def __init__(self, port: Port):
        self.port = port


class robot:
    def __init__(self, leftPort, rightPort,wDiameter,axle, pos = vec2(0,0)):
        self.hub = hub()
        self.lM = motor(leftPort)
        self.rM = motor(rightPort)
        self.devices = []
        self.pos = pos
        self.Diameter = wDiameter
        self.axle = axle
        
    def setSpeed(self, lSpeed: float, rSpeed: float):
        self.lM.setSpeed(lSpeed)
        self.rM.setSpeed(rSpeed)
        pass
    
    
    def stop(self, brake = True):
        if brake:
            self.lM.hold()
            self.rM.hold()
            wait(200)
            self.lM.brake()
            self.rM.brake()
        else:
            self.lM.brake()
            self.rM.brake()
        pass
    
    def addDevice(self, device:rdevice):
        self.devices.append(device)
        
    def update(self):
        self.pos += navigate(self.lM, self.rM, self.hub, self.Diameter)
    pass

class Ultrasonic(rdevice):
    def __init__(self, port: Port):
        super().__init__(port)
        self.m_sensor = UltrasonicSensor(port)
        
    def distance(self):
        return self.m_sensor.distance()/10
    
    def angle(self):
        return self.m_sensor.angle()
    
    def angleRad(self):
        return self.m_sensor.angle()/180 * pi

class motor(rdevice):
    def __init__(self, port: Port):
        super().__init__(port)
        self.reverse = False
        self.offset = 0
        self.switchDir = False
        self.m_motor = Motor(port)
        self.deltaAngle = 0
        self.lastAngle = self.angleRad()
    
    def setDefAngle(self, angle = 0):
        self.offset = angle/180*pi + self.angleRad()
    
    def setSpeed(self, speed: float):
        if self.reverse:
            self.m_motor.run(-speed)
        else:
            self.m_motor.run(speed)
        pass

    def stop(self):
        self.m_motor.stop()
        pass
    
    def Update(self):
        if self.reverse:
            self.deltaAngle = -self.angleRad() + self.lastAngle
        else:
            self.deltaAngle = self.angleRad() - self.lastAngle
        self.lastAngle = self.angleRad()
        pass
    
    def brake(self):
        self.m_motor.brake()
        pass
    
    def hold(self):
        self.m_motor.hold()
        pass
    
    def angle(self):
        return float(self.m_motor.angle()) - self.offset/pi * 180
    def angleRad(self):
        return float(self.m_motor.angle())/180 * pi - self.offset

# tvoje máma
class hub:
    def __init__(self):
        self.m_hub = PrimeHub()
        self.angleOffset = 0
        self.resetAngle()
        self.setOffButton(Button.BLUETOOTH)
    def addOffset(self, offset):
        self.angleOffset += offset    
    
    def angle(self):
        return self.m_hub.imu.rotation(Axis.Z) - self.angleOffset
    
    def angleRad(self):
        return (self.m_hub.imu.rotation(Axis.Z) - self.angleOffset) / 180 * pi
    
    def resetAngle(self):
        self.angleOffset = self.m_hub.imu.rotation(Axis.Z)
        
    def pixel(self,x,y, brigthness=100):
        self.m_hub.display.pixel(y, x, brigthness)
    
    def beep(self, freq, duration):
        self.m_hub.speaker.beep(freq, duration)
    
    def setVolume(self, volume):
        self.m_hub.speaker.volume(volume)
    
    def notes(self, notes, tempo=120):
        self.m_hub.speaker.play_notes(notes, tempo)
    
    def isButtonPressed(self, button: Button):
        return True if button in self.m_hub.buttons.pressed() else False
    
    def setOffButton(self, button: Button):
        self.m_hub.system.set_stop_button(button)
    
    def color(self, color: Color):
        self.m_hub.light.on(color)
        
    def animate(self, animation, delta):
        self.m_hub.display.animate(animation, delta)
    def image(self, image):
        self.m_hub.display.icon(image)
    def clear(self):
        self.m_hub.display.off()

def navigate(lM:motor, rM:motor, hub:hub, diameter):
    scalar = (lM.deltaAngle*diameter + rM.deltaAngle*diameter) * 0.25
    vec = scalar * mat2.rotation(hub.angleRad()) * vec2(1, 0)
    lM.Update()
    rM.Update()
    
    return vec