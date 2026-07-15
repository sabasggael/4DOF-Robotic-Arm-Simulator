from math import *

class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def magnitud(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))
    
    def normalizar(self):
        mag = self.magnitud()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)
    
    def __add__(self, otro):
        return Vector3D(self.x + otro.x, self.y + otro.y, self.z + otro.z)
    
    def __sub__(self, otro):
        return Vector3D(self.x - otro.x, self.y - otro.y, self.z - otro.z)
    
    def __mul__(self, escalar):
        return Vector3D(self.x * escalar, self.y * escalar, self.z * escalar)
    
    def __truediv__(self, escalar):
        return Vector3D(self.x / escalar, self.y / escalar, self.z / escalar)
    
    def producto_punto(self, otro):
        return self.x * otro.x + self.y * otro.y + self.z * otro.z
    
    def producto_cruz(self, otro):
        return Vector3D(
            self.y * otro.z - self.z * otro.y,
            self.z * otro.x - self.x * otro.z,
            self.x * otro.y - self.y * otro.x)
    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
    def __repr__(self):
        return f"Vector3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco