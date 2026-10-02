from umath import cos, sin, atan2, pi
from pybricks.tools import StopWatch

class PID:
    def __init__(self, kp, ki, kd, max_integral=100):
        """
        **Info**
        Initialize a PID controller and its internal state.

        **Parameters**
        - kp: Proportional gain.
        - ki: Integral gain.
        - kd: Derivative gain.
        - max_integral: Maximum absolute value of the accumulated integral.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
        self.max_integral = max_integral # Ochrana proti "wind-up" (přetečení integrálu)
        self.timer = StopWatch()

    def compute(self, error):
        """
        **Info**
        Calculate the PID output for the current error and update controller state.

        **Parameters**
        - error: Current difference between the target and measured value.

        **Return**
        - PID output value.
        """
        dt = self.timer.time() / 1000.0 # čas v sekundách od posledního volání
        self.timer.reset()
        
        if dt == 0:
            dt = 0.01 # Ochrana proti dělení nulou při prvním průchodu

        # Proporcionální část (současná chyba)
        p = self.kp * error
        
        # Integrační část (historie chyb - pomáhá překonat tření v závěru)
        self.integral += error * dt
        # Omezení integrálu, aby robot při dlouhé chybě "nevystřelil"
        self.integral = max(-self.max_integral, min(self.integral, self.max_integral))
        i = self.ki * self.integral
        
        # Derivační část (předvídání - brzdí pohyb, když se chyba rychle zmenšuje)
        d = self.kd * ((error - self.prev_error) / dt)
        
        self.prev_error = error
        
        return p + i + d

def generateBezierCurve(p0, p1, p2, p3, num_points=10):
    """
    **Info**
    Generate points on a cubic Bezier curve.

    **Parameters**
        p0 (vec2): The starting point of the curve.
        p1 (vec2): The first control point.
        p2 (vec2): The second control point.
        p3 (vec2): The ending point of the curve.
        num_points (int): The number of points to generate on the curve.

    **Return**
    - List of vec2 points on the curve, including both endpoints.
    """
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        points.append(bezier(t, p0, p1, p2, p3))
    return points

def bezier(t, p0, p1, p2, p3):
    """
    **Info**
    Calculate a point on a cubic Bezier curve.

    **Parameters**
        t (float): The parameter t, where 0 <= t <= 1.
        p0 (vec2): The starting point of the curve.
        p1 (vec2): The first control point.
        p2 (vec2): The second control point.
        p3 (vec2): The ending point of the curve.

    **Return**
    - vec2 point on the curve at parameter t.
    """
    u = 1 - t
    p = u**3 * p0  # (1-t)^3 * P0
    p += 3 * u**2 * t * p1  # 3(1-t)^2 * t * P1
    p += 3 * u * t**2 * p2  # 3(1-t) * t^2 * P2
    p += t**3 * p3  # t^3 * P3

    return p

def sign(x):
    """
    **Info**
    Return the sign of a number.

    **Parameters**
    - x: Number to check.

    **Return**
    - 1 if x is positive, 0 if x is zero, or -1 if x is negative.
    """
    if x >0:
        return 1
    if x == 0:
        return 0
    return -1

def clamp(x, minVal, maxVal):
    """
    **Info**
    Limit a value to the inclusive range from minVal to maxVal.

    **Parameters**
    - x: Value to limit.
    - minVal: Lower bound.
    - maxVal: Upper bound.

    **Return**
    - x limited to the inclusive range from minVal to maxVal.
    """
    if x < minVal:
        return minVal
    if x > maxVal:
        return maxVal
    return x

def maxV(x,v):
    """
    **Info**
    Return x unless it exceeds v, in which case return v.

    **Parameters**
    - x: Value to check.
    - v: Maximum allowed value.

    **Return**
    - The smaller of x and v.
    """
    if x>v:
        return v
    return x

def minV(x,v):
    """
    **Info**
    Return x unless it is below v, in which case return v.

    **Parameters**
    - x: Value to check.
    - v: Minimum allowed value.

    **Return**
    - The larger of x and v.
    """
    if x<v:
        return v
    return x

def avr(*x):
    """
    **Info**
    Calculate the arithmetic mean of the supplied values.

    **Parameters**
    - x: Values as separate arguments or as a single list or tuple. Returns 0
      when no values are supplied.

    **Return**
    - Arithmetic mean of the values, or 0 if no values are supplied.
    """
    if len(x) == 1 and isinstance(x[0], (list, tuple)):
        values = x[0]
    else:
        values = x
    return sum(values) / len(values) if values else 0

def angleDiff(angle1:float, angle2:float, simple = False):
        """
        **Info**
        Calculate the signed angular difference from angle1 to angle2.

        **Parameters**
        - angle1: Starting angle in radians.
        - angle2: Destination angle in radians.
        - simple: If True, return the unnormalized difference; otherwise
          return the shortest signed difference in radians.

        **Return**
        - Signed difference in radians.
        """
        if simple:
            return angle2 - angle1
        a1 = (angle1) % (2*pi)
        a2 = (angle2) % (2*pi)
        return (a2 - a1 + pi) % (2*pi) - pi

class vec2:
    def __init__(self, x: float, y: float):
        """
        **Info**
        Create a two-dimensional vector.

        **Parameters**
        - x: Horizontal component.
        - y: Vertical component.
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        **Info**
        Add another vector component-wise.

        **Parameters**
        - other: Vector to add.

        **Return**
        - New vec2 containing the component-wise sum.
        """
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        **Info**
        Subtract another vector component-wise.

        **Parameters**
        - other: Vector to subtract.

        **Return**
        - New vec2 containing the component-wise difference.
        """
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        """
        **Info**
        Multiply both vector components by a scalar.

        **Parameters**
        - scalar: Number to multiply by.

        **Return**
        - New vec2 with both components multiplied by scalar.
        """
        return vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float):
        """
        **Info**
        Support multiplication with a scalar on the left.

        **Parameters**
        - scalar: Number to multiply by.

        **Return**
        - New vec2 with both components multiplied by scalar.
        """
        return self * scalar

    def __truediv__(self, scalar: float):
        """
        **Info**
        Divide both vector components by a scalar.

        **Parameters**
        - scalar: Number to divide by.

        **Return**
        - New vec2 with both components divided by scalar.
        """
        return vec2(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        """
        **Info**
        Compare this vector with another by component values.

        **Parameters**
        - other: Vector to compare.

        **Return**
        - True if both components match; otherwise False.
        """
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """
        **Info**
        Return the vector's developer-facing string representation.

        **Return**
        - String representation of the vector.
        """
        return f"vec2({self.x}, {self.y})"

    def length(self):
        """
        **Info**
        Calculate the length (magnitude) of the vector.

        **Return**
        - Vector length as a non-negative number.
        """
        return (self.x**2 + self.y**2)**0.5
    
    def normalize(self):
        """
        **Info**
        Return a vector with the same direction and unit length.

        **Return**
        - New vec2 with unit length and the same direction. A zero-length
          vector cannot be normalized.
        """
        length = self.length()
        if length == 0:
            print("Cannot normalize a zero-length vector.")
        return vec2(self.x / length, self.y / length)
    def xAngle(self):
        """
        **Info**
        Calculate the vector's angle from the positive x-axis in radians.

        **Return**
        - Angle from the positive x-axis in radians.
        """
        return atan2(self.y, self.x)

class mat2:
    def __init__(self, a: float, b:float , c:float, d:float):
        """
        **Info**
        Create a 2-by-2 matrix with the supplied row-major elements.

        **Parameters**
        - a: Element in the first row and first column.
        - b: Element in the first row and second column.
        - c: Element in the second row and first column.
        - d: Element in the second row and second column.
        """
        self.m = [[a, b], [c, d]]

    @staticmethod
    def rotation(angle: float):
        """
        **Info**
        Create a 2D rotation matrix for an angle in radians.

        **Parameters**
        - angle: Rotation angle in radians.

        **Return**
        - mat2 rotation matrix for the specified angle.
        """
        c = cos(angle)
        s = sin(angle)
        return mat2(c, -s, s, c)
    
    def identity(self):
        """
        **Info**
        Return a 2-by-2 identity matrix.

        **Return**
        - A 2-by-2 identity matrix.
        """
        return mat2(1, 0, 0, 1)
    
    def __repr__(self):
        """
        **Info**
        Return the matrix's developer-facing string representation.

        **Return**
        - String representation of the matrix.
        """
        return f"mat2({self.m[0][0]}, {self.m[0][1]}, {self.m[1][0]}, {self.m[1][1]})"
    
    def __mul__(self, other):
        """
        **Info**
        Multiply by a matrix, vector, or scalar.

        **Parameters**
        - other: Matrix, vector, or numeric scalar to multiply by.

        **Return**
        - mat2 for matrix/scalar multiplication, vec2 for matrix-vector
          multiplication, or None for an unsupported operand.
        """
        if isinstance(other, mat2):
            a = self.m[0][0] * other.m[0][0] + self.m[0][1] * other.m[1][0]
            b = self.m[0][0] * other.m[0][1] + self.m[0][1] * other.m[1][1]
            c = self.m[1][0] * other.m[0][0] + self.m[1][1] * other.m[1][0]
            d = self.m[1][0] * other.m[0][1] + self.m[1][1] * other.m[1][1]
            return mat2(a, b, c, d)
        elif isinstance(other, vec2):
            x = self.m[0][0] * other.x + self.m[0][1] * other.y
            y = self.m[1][0] * other.x + self.m[1][1] * other.y
            return vec2(x, y)
        elif isinstance(other, (int, float)):
            a = self.m[0][0] * other
            b = self.m[0][1] * other
            c = self.m[1][0] * other
            d = self.m[1][1] * other
            return mat2(a, b, c, d)
        else:
            print("Unsupported operand type(s) for *: 'mat2' and '{}'".format(type(other).__name__))

    def __rmul__(self, other):
        """
        **Info**
        Support multiplication by a scalar on the left.

        **Parameters**
        - other: Numeric scalar to multiply by.

        **Return**
        - Scaled mat2, or None for an unsupported operand.
        """
        if isinstance(other, (int, float)):
            return self * other
        else:
            print("Unsupported operand type(s) for *: '{}' and 'mat2'".format(type(other).__name__))

    def det(self):
        """
        **Info**
        Calculate the matrix determinant.

        **Return**
        - Determinant as a number.
        """
        return self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0]

    def transpose(self):
        """
        **Info**
        Return the transpose of this matrix.

        **Return**
        - Transposed mat2.
        """
        return mat2(self.m[0][0], self.m[1][0], self.m[0][1], self.m[1][1])
    
    def adj(self):
        """
        **Info**
        Return the adjugate matrix.

        **Return**
        - Adjugate mat2.
        """
        return mat2(self.m[1][1], -self.m[0][1], -self.m[1][0], self.m[0][0]) # adj(Matrix) = (Matrix of minors)^T
    
    def inverse(self):
        """
        **Info**
        Return the inverse matrix, or raise ValueError if it is singular.

        **Return**
        - Inverse mat2. Raises ValueError if the matrix is singular.
        """
        det = self.det() # det^(-1)*adj(Matrix) = Matrix^(-1)
        if det == 0:
            raise ValueError("Matrix is singular and cannot be inverted.")
        return 1/det * self.adj()
    
class Line:
    def __init__(self, a: vec2, b: vec2):
        """
        **Info**
        Create a line from two points and calculate its direction and normal.

        **Parameters**
        - a: First point on the line.
        - b: Second point on the line.
        """
        self.a = a
        self.b = b
        self.direction = (b - a).normalize()
        self.normal = vec2(-self.direction.y, self.direction.x)
        self.parC = - self.normal.x * self.a.x - self.normal.y * self.a.y
        self.orientation = self.direction.xAngle()

    def move(self, shift: vec2):
        """
        **Info**
        Move both stored endpoints by the supplied vector.

        **Parameters**
        - shift: Translation vector.
        """
        self.a += shift
        self.b += shift

    def translated(self, shift: vec2):
        """
        **Info**
        Return a parallel line translated by the supplied vector.

        **Parameters**
        - shift: Translation vector.

        **Return**
        - New Line parallel to this line and translated by shift.
        """
        return Line(self.a + shift, self.b + shift)