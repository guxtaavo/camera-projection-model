import matplotlib.pyplot as plt

class Ploter():
    def __init__(self):
        pass

    ### Function to create a figure with 3D graphic
    @staticmethod
    def set_plot(ax=None,figure = None,lim=[-2,2]):
        if figure ==None:
            figure = plt.figure(figsize=(8,8))
        if ax==None:
            ax = plt.axes(projection='3d')

        ax.set_xlim(lim)
        ax.set_xlabel("x axis")
        ax.set_ylim(lim)
        ax.set_ylabel("y axis")
        ax.set_zlim(lim)
        ax.set_zlabel("z axis")
        return ax

    #Adding quivers to a plot
    @staticmethod
    def draw_arrows(point,base,axis,length=1.5):
        # The object base is a matrix, where each column represents the vector
        # of one of the axis, written in homogeneous coordinates (ax,ay,az,0)

        # Plot vector of x-axis
        axis.quiver(point[0],point[1],point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
        # Plot vector of y-axis
        axis.quiver(point[0],point[1],point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
        # Plot vector of z-axis
        axis.quiver(point[0],point[1],point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)

        return axis
