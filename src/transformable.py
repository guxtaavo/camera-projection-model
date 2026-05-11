import numpy as np
from math import pi, cos, sin

class Transformable():
    def __init__(self, ref):
        self.ref = ref.copy()

    def move(self, dx, dy, dz):
        T = np.eye(4)
        T[0,-1]=dx; T[1,-1]=dy; T[2,-1]=dz
        self.ref = T @ self.ref
        return self

    def x_rotation(self, angle):
        a = angle*pi/180
        R = np.array([[1,0,0,0],[0,cos(a),-sin(a),0],[0,sin(a),cos(a),0],[0,0,0,1]])
        self.ref = R @ self.ref
        return self

    def y_rotation(self, angle):
        a = angle*pi/180
        R = np.array([[cos(a),0,sin(a),0],[0,1,0,0],[-sin(a),0,cos(a),0],[0,0,0,1]])
        self.ref = R @ self.ref
        return self

    def z_rotation(self, angle):
        a = angle*pi/180
        R = np.array([[cos(a),-sin(a),0,0],[sin(a),cos(a),0,0],[0,0,1,0],[0,0,0,1]])
        self.ref = R @ self.ref
        return self