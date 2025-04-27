from umath import cos, sin




def generateBezierCurve(p0, p1, p2, p3, num_points=10):
    """Generate points on a cubic Bezier curve.

    Args:
        p0 (vec2): The starting point of the curve.
        p1 (vec2): The first control point.
        p2 (vec2): The second control point.
        p3 (vec2): The ending point of the curve.
        num_points (int): The number of points to generate on the curve.

    Returns:
        list: A list of vec2 points on the cubic Bezier curve.
    """
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        points.append(bezier(t, p0, p1, p2, p3))
    return points

def bezier(t, p0, p1, p2, p3):
    """Calculate a point on a cubic Bezier curve.

    Args:
        t (float): The parameter t, where 0 <= t <= 1.
        p0 (vec2): The starting point of the curve.
        p1 (vec2): The first control point.
        p2 (vec2): The second control point.
        p3 (vec2): The ending point of the curve.

    Returns:
        vec2: A point on the cubic Bezier curve at parameter t.
    """
    u = 1 - t
    p = u**3 * p0  # (1-t)^3 * P0
    p += 3 * u**2 * t * p1  # 3(1-t)^2 * t * P1
    p += 3 * u * t**2 * p2  # 3(1-t) * t^2 * P2
    p += t**3 * p3  # t^3 * P3

    return p

def sign(x):
    if x >0:
        return 1
    if x == 0:
        return 0
    return -1

def clamp(x, minVal, maxVal):
    if x < minVal:
        return minVal
    if x > maxVal:
        return maxVal
    return x

def maxV(x,v):
    if x>v:
        return v
    return x

def minV(x,v):
    if x<v:
        return v
    return x

class vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float):
        return self * scalar

    def __truediv__(self, scalar: float):
        return vec2(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"vec2({self.x}, {self.y})"

    def length(self):
        """Calculate the length (magnitude) of the vector."""
        return (self.x**2 + self.y**2)**0.5

class mat2:
    def __init__(self, a: float, b:float , c:float, d:float):

        self.m = [[a, b], [c, d]]

    def rotation(angle: float):
        c = cos(angle)
        s = sin(angle)
        return mat2(c, -s, s, c)
    
    def identity():
        return mat2(1, 0, 0, 1)
    
    def __repr__(self):
        return f"mat2({self.m[0][0]}, {self.m[0][1]}, {self.m[1][0]}, {self.m[1][1]})"
    
    def __mul__(self, other):
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
        if isinstance(other, (int, float)):
            return self * other
        else:
            print("Unsupported operand type(s) for *: '{}' and 'mat2'".format(type(other).__name__))

    def det(self):
        return self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0]

    def transpose(self):  return mat2(self.m[0][0], self.m[1][0], self.m[0][1], self.m[1][1])
    
    def adj(self):
        return mat2(self.m[1][1], -self.m[0][1], -self.m[1][0], self.m[0][0]) # adj(Matrix) = (Matrix of minors)^T
    
    def inverse(self):
        det = self.det() # det^(-1)*adj(Matrix) = Matrix^(-1)
        if det == 0:
            raise ValueError("Matrix is singular and cannot be inverted.")
        return 1/det * self.adj()