from math import *

def factors(x) -> list[int]:
    f = []

    for i in range(1, floor(x / 2)):
        if x % i == 0:
            f += [i, x/i]

    return list(set(f))

def distance(x1: float, y1: float, x2: float=None, y2: float=None) -> float: # doubles as pythagoras func
    x2 = x1 * 2 if x2 is None else x2
    y2 = y1 * 2 if y2 is None else y2

    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def findleg(l: float, h: float) -> float:
    return sqrt(h**2 - l**2)

def angle(x1, y1, x2, y2):
    return atan2(y2 - y1, x2 - x1) * 180 / pi

def deg2rad(d: float) -> float:
    return d * pi / 180

def rad2deg(r: float) -> float:
    return r * 180 / pi

def quad(a: float, b: float, c: float, pos=True) -> float:
    return (-b + (sqrt(b**2 - (a * c * 4))) * ((pos * 2) - 1)) / (a * 2)

class volume:
    def sphere(r):
        return 4 / 3 * pi * r**2

    def cone(r, h):
        return pi * r**2 * (h / 3)

    def cylinder(r, h):
        return pi * r**2 * h
    
    def rect_cuboid(h, w, d):
        return h * w * d
    
    def sqr_pyramid(w, h):
        return w**2 * (h / 3)

class area:
    def circle(r):
        return pi * r**2

    def right_tri(a, b):
        return a * b / 2
    
    def ellipse(a, b):
        return pi * a * b
    
    def rect(w, h):
        return w * h
    
    def reg_polygon(sides, sidelength):
        return (sides * sidelength * (sidelength / (2 * tan(180 / sides))))/2

if __name__ == "__main__":
    while True:
        x = input("> ")
        t, a, b = x.split(" ")
        if t == "l":
            x = findleg(float(a), float(b))
        elif t == "h":
            x = distance(float(a), float(b))
        print(x)