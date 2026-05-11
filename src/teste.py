from math import pi,cos,sin
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from object import Object
from pathlib import Path
from transformable import Transformable
from ploter import Ploter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OBJECT_NAME = "bulbasaur"
OBJECT_STL_PATH = PROJECT_ROOT / "assets" / "models" / f"{OBJECT_NAME}.stl"

def main():
    # base vector values
    e1 = np.array([[1],[0],[0],[0]]) # X
    e2 = np.array([[0],[1],[0],[0]]) # Y
    e3 = np.array([[0],[0],[1],[0]]) # Z
    base = np.hstack((e1,e2,e3))
    #origin point
    origin =np.array([[0],[0],[0],[1]])

    # Create camera and world frames
    cam  = np.hstack([base,origin])
    world = np.hstack([base,origin])

    print ('Camera Reference Frame: \n', cam)
    print ('World Reference Frame: \n', world)

    cam_transf = Transformable(cam)
    cam_transf.x_rotation(145)        # agora aplica de verdade
    cam_transf.z_rotation(-20)
    cam_transf.move(-2,-2,-2)
    cam = cam_transf.ref

    # Ploting the world reference frame and the camera frame
    ploter = Ploter()
    axis = Ploter.set_plot(lim=[-5,5])
    axis = Ploter.draw_arrows(world[:,-1],world[:,0:3],axis,3)
    axis = Ploter.draw_arrows(cam[:,-1],cam[:,0:3],axis,1.5)
    axis.set_title("Camera and World Reference Frames")

    obj = Object(OBJECT_STL_PATH)

    obj_transf = Transformable(obj.obj)
    obj_transf.x_rotation(145)        # agora aplica de verdade
    obj_transf.z_rotation(-20)
    obj_transf.move(-2,-2,-2)
    triangles = obj_transf.ref[:3, :].T.reshape(-1, 3, 3)

    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    poly = Poly3DCollection(triangles, alpha=0.4)
    poly.set_facecolor('cyan')
    poly.set_edgecolor('gray')
    axis.add_collection3d(poly)

    plt.show()

if __name__ == "__main__":
    main()
