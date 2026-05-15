from umath import cos, sin



def sign(x):
    '''
    Parameters:
        x : number to be checked
    Returns:
        1 if x > 0, -1 if x < 0, and 0 if x == 0.
    '''
    if x >0:
        return 1
    if x == 0:
        return 0
    return -1

def clamp(x: float, minVal: float, maxVal: float) -> float:
    '''
    Parameters:
        x : number to be clamped
        minVal : minimum value
        maxVal : maximum value
    Returns:
        the clamped value of x between minVal and maxVal.
    '''
    if x < minVal:
        return minVal
    if x > maxVal:
        return maxVal
    return x

#def maxV(x,v):
#    if x>v:
#        return v
#    return x

def maxV(*x: float) -> float:
    '''
    Parameters:
        x : list of numbers
    Returns:
        the largest number in a list of numbers.
    '''
    m = x[0]
    for i in x:
        if i > m:
            m = i
    return m

#def minV(x,v):
#    if x<v:
#        return v
#    return x

def minV(*x: float) -> float:
    '''
    Parameters:
        x : list of numbers
    Returns:
        the smallest number in a list of numbers.
    '''
    m = x[0]
    for i in x:
        if i < m:
            m = i
    return m

def avrV(*x: float) -> float:
    '''
    Parameters:
        x : list of numbers
    Returns:
        the average of a list of numbers.
    '''
    s = 0
    for i in x:
        s += i
    return s/len(x)

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

    def __truediv__(self, scalar: float):
        return vec2(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"vec2({self.x}, {self.y})"

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