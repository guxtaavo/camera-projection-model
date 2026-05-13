import numpy as np

def image_project(intrisicMatrix,cam,obj):
    CanProjMatrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],])
    IntrisicMatrix = intrisicMatrix
    ExtrinsicMatrix = np.linalg.inv(cam)

    P = IntrisicMatrix@CanProjMatrix@ExtrinsicMatrix

    P_img = P @ obj

    P_img = P_img/P_img[2]

    return P_img