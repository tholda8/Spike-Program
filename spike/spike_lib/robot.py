from pybricks.parameters import *
from pybricks.pupdevices import *
from pybricks.hubs import PrimeHub
from pybricks.tools import *
from spike_lib.maths import vec2, mat2
from umath import pi

    
class Rdevice:
    def __init__(self, port: Port):
        """
        **Info**
        Initialize a device attached to a hub port.

        **Parameters**
        - port: Hub port connected to the device.
        """
        self.port = port

class Robot:
    def __init__(self, leftPort, rightPort, wDiameter, axle, topSide: Axis = Axis.Z, frontSide: Axis = Axis.X, pos = vec2(0,0)):
        """
        **Info**
        Initialize a two-motor robot and its hub orientation and position.

        **Parameters**
        - leftPort: Port connected to the left drive motor.
        - rightPort: Port connected to the right drive motor.
        - wDiameter: Drive wheel diameter, in the same distance units used for
          position updates.
        - axle: Distance between the drive wheels.
        - topSide: Hub axis treated as its top direction.
        - frontSide: Hub axis treated as its front direction.
        - pos: Initial robot position as a vec2.
        """
        self.hub = Hub(topSide, frontSide)
        self.lM = motor(leftPort)
        self.rM = motor(rightPort)
        self.devices = []
        self.pos = pos
        self.Diameter = wDiameter
        self.axle = axle
        
    def setSpeed(self, lSpeed: float, rSpeed: float):
        """
        **Info**
        Set the speed of the left and right drive motors.

        **Parameters**
        - lSpeed: Left motor speed, in the motor API's speed units.
        - rSpeed: Right motor speed, in the motor API's speed units.
        """
        self.lM.setSpeed(lSpeed)
        self.rM.setSpeed(rSpeed)
        pass
    
    def stop(self, brake = True):
        """
        **Info**
        Stop both drive motors. When brake is True, hold briefly before braking.

        **Parameters**
        - brake: If True, hold both motors for 200 ms and then brake; if False,
          brake immediately.
        """
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
    
    def addDevice(self, device:Rdevice):
        """
        **Info**
        Register a device in the robot's device list.

        **Parameters**
        - device: Device instance to add.
        """
        self.devices.append(device)
        
    def update(self):
        """
        **Info**
        Update the stored position using drive-motor movement and hub heading.
        """
        self.pos += navigate(self.lM, self.rM, self.hub, self.Diameter)
    pass

class Ultrasonic(Rdevice):
    def __init__(self, port: Port):
        """
        **Info**
        Create an ultrasonic sensor on the specified hub port.

        **Parameters**
        - port: Port connected to the ultrasonic sensor.
        """
        super().__init__(port)
        self.m_sensor = UltrasonicSensor(port)
        
    def distance(self):
        """
        **Info**
        Read the sensor distance and convert it from millimetres to centimetres.

        **Return**
        - Distance in centimetres.
        """
        return self.m_sensor.distance()/10
    
    def angle(self):
        """
        **Info**
        Read the ultrasonic sensor's angle in degrees.

        **Return**
        - Sensor angle in degrees.
        """
        return self.m_sensor.angle()
    
    def angleRad(self):
        """
        **Info**
        Read the ultrasonic sensor's angle in radians.

        **Return**
        - Sensor angle in radians.
        """
        return self.m_sensor.angle()/180 * pi

class motor(Rdevice):
    def __init__(self, port: Port):
        """
        **Info**
        Create a motor wrapper and initialize its angle-tracking state.

        **Parameters**
        - port: Port connected to the motor.
        """
        super().__init__(port)
        self.reverse = False
        self.offset = 0
        self.switchDir = False
        self.m_motor = Motor(port)
        self.deltaAngle = 0
        self.lastAngle = self.angleRad()
    
    def setDefAngle(self, angle = 0):
        """
        **Info**
        Set a reference angle offset for the motor's reported angle.

        **Parameters**
        - angle: Reference angle in degrees.
        """
        self.offset = angle/180*pi + self.angleRad()

    def setSpeed(self, speed: float):
        """
        **Info**
        Run the motor at the requested speed, accounting for reverse mode.

        **Parameters**
        - speed: Motor speed in the motor API's speed units.
        """
        if self.reverse:
            self.m_motor.run(-speed)
        else:
            self.m_motor.run(speed)
        pass

    def stop(self):
        """
        **Info**
        Stop the motor using the underlying motor's stop behavior.
        """
        self.m_motor.stop()
        pass
    
    def Update(self):
        """
        **Info**
        Update the motor's signed angle change since its previous update.
        """
        if self.reverse:
            self.deltaAngle = -self.angleRad() + self.lastAngle
        else:
            self.deltaAngle = self.angleRad() - self.lastAngle
        self.lastAngle = self.angleRad()
        pass
    
    def brake(self):
        """
        **Info**
        Brake the motor.
        """
        self.m_motor.brake()
        pass
    
    def hold(self):
        """
        **Info**
        Hold the motor at its current position.
        """
        self.m_motor.hold()
        pass
    
    def angle(self):
        """
        **Info**
        Return the motor angle relative to its configured reference, in degrees.

        **Return**
        - Motor angle in degrees.
        """
        return float(self.m_motor.angle()) - self.offset/pi * 180

    def angleRad(self):
        """
        **Info**
        Return the motor angle relative to its configured reference, in radians.

        **Return**
        - Motor angle in radians.
        """
        return float(self.m_motor.angle())/180 * pi - self.offset

class Hub:
    def __init__(self, topSide: Axis = Axis.Z, frontSide: Axis = Axis.X):
        """
        **Info**
        Initialize the hub wrapper, orientation axes, and stop button.

        **Parameters**
        - topSide: Hub axis used for heading measurements.
        - frontSide: Hub axis configured as the front direction.
        """
        self.m_hub = PrimeHub() #(topSide, frontSide) 
        self.topSide = topSide #Z nějakého důvodu zakomentované argumenty výše mění názvy všech os
        self.frontSide = frontSide
        self.angleOffset = 0
        self.resetAngle()
        self.setOffButton(Button.BLUETOOTH)
        self.switch = False
        
    def addOffset(self, offset):
        """
        **Info**
        Add an offset to the hub heading reference.

        **Parameters**
        - offset: Heading offset in degrees.
        """
        self.angleOffset += offset    
    
    def angle(self):
        """
        **Info**
        Return the hub heading relative to its offset, in degrees.

        **Return**
        - Heading in degrees, with sign adjusted when switch is enabled.
        """
        if self.switch:
            return - (self.m_hub.imu.rotation(self.topSide) - self.angleOffset)
        return self.m_hub.imu.rotation(self.topSide) - self.angleOffset
    
    def angleRad(self):
        """
        **Info**
        Return the hub heading relative to its offset, in radians.

        **Return**
        - Heading in radians, with sign adjusted when switch is enabled.
        """
        if self.switch:
            return -(self.m_hub.imu.rotation(self.topSide) - self.angleOffset) / 180 * pi
        return (self.m_hub.imu.rotation(self.topSide) - self.angleOffset) / 180 * pi
    
    def resetAngle(self):
        """
        **Info**
        Set the current hub heading as the zero-angle reference.
        """
        self.angleOffset = self.m_hub.imu.rotation(self.topSide)
        
    def pixel(self,x,y, brigthness=100):
        """
        **Info**
        Set the brightness of a display pixel.

        **Parameters**
        - x: Pixel x-coordinate (passed as the display row).
        - y: Pixel y-coordinate (passed as the display column).
        - brigthness: Pixel brightness.
        """
        self.m_hub.display.pixel(y, x, brigthness)
    
    def beep(self, freq, duration):
        """
        **Info**
        Play a tone through the hub speaker.

        **Parameters**
        - freq: Tone frequency in hertz.
        - duration: Tone duration in milliseconds.
        """
        self.m_hub.speaker.beep(freq, duration)
    
    def setVolume(self, volume):
        """
        **Info**
        Set the hub speaker volume.

        **Parameters**
        - volume: Volume level accepted by the hub speaker API.
        """
        self.m_hub.speaker.volume(volume)
    
    def notes(self, notes, tempo=120):
        """
        **Info**
        Play a sequence of musical notes through the hub speaker.

        **Parameters**
        - notes: Note sequence in the format expected by the hub speaker API.
        - tempo: Playback tempo in beats per minute.
        """
        self.m_hub.speaker.play_notes(notes, tempo)

    def playNotes(self, notes,  mult = 1):
        """
        **Info**
        Repeatedly play a sequence of tones without returning.

        **Parameters**
        - notes: Iterable of (frequency, duration) pairs.
        - mult: Multiplier applied to each duration.
        """
        self.setVolume(1000)
        while True:
            for freq, duration in notes:
                self.beep(freq, duration * mult)
                #wait(duration)

    def isButtonPressed(self, button: Button):
        """
        **Info**
        Check whether a specified hub button is currently pressed.

        **Parameters**
        - button: Hub button to check.

        **Return**
        - True if the button is pressed; otherwise False.
        """
        return True if button in self.m_hub.buttons.pressed() else False
    
    def setOffButton(self, button: Button):
        """
        **Info**
        Select the hub button that stops the running program.

        **Parameters**
        - button: Button to configure as the program stop button.
        """
        self.m_hub.system.set_stop_button(button)
    
    def color(self, color: Color):
        """
        **Info**
        Set the hub light to a color.

        **Parameters**
        - color: Color to display on the hub light.
        """
        self.m_hub.light.on(color)
    
    def colorAnimate(self, colors, duration=100):
        """
        **Info**
        Animate the hub light through a sequence of colors.

        **Parameters**
        - colors: Sequence of colors for the animation.
        - duration: Duration value passed to the hub light API.
        """
        self.m_hub.light.animate(colors, duration)

    def animate(self, animation, delta):
        """
        **Info**
        Play a display animation.

        **Parameters**
        - animation: Animation data accepted by the hub display API.
        - delta: Animation timing or step value accepted by the API.
        """
        self.m_hub.display.animate(animation, delta)

    def image(self, image):
        """
        **Info**
        Display an icon on the hub display.

        **Parameters**
        - image: Icon data accepted by the hub display API.
        """
        self.m_hub.display.icon(image)

    def clear(self):
        """
        **Info**
        Turn off the hub display.
        """
        self.m_hub.display.off()

def navigate(lM:motor, rM:motor, hub: Hub, diameter):
    """
    **Info**
    Estimate the robot's displacement since the previous motor update.

    The distance estimate uses the average wheel rotation and rotates the
    displacement by the hub heading.

    **Parameters**
    - lM: Left motor wrapper with an updated deltaAngle.
    - rM: Right motor wrapper with an updated deltaAngle.
    - hub: Hub wrapper providing the current heading.
    - diameter: Drive wheel diameter in the distance units of the position.

    **Return**
    - vec2 displacement estimated since the previous motor update.
    """
    scalar = (lM.deltaAngle*diameter + rM.deltaAngle*diameter) * 0.25
    vec = scalar * mat2.rotation(hub.angleRad()) * vec2(1, 0)
    lM.Update()
    rM.Update()
    
    return vec