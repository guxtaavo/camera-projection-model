import numpy as np

class Camera():
    def __init__(self):
        #Intrinsic Params
        self.focalDist = 15
        self.ccdx = 36
        self.ccdy = 24
        self.widthPixels = 1280
        self.heightPixels = 720
        self.sTheta = 0
        self.M = np.eye(4)

    def get_params_intrinsc(self):
        intrinsic = np.array([[self.focalDist*(self.widthPixels/self.ccdx), self.focalDist*(self.sTheta), self.widthPixels/2],
                              [0 , self.focalDist*(self.heightPixels/self.ccdy), self.heightPixels/2], 
                              [0, 0, 1]])
        
        return intrinsic

    def update_params_intrinsc(self, line_edits):
        params_list = [self.widthPixels,self.heightPixels,self.ccdx,self.ccdy,
                       self.focalDist,self.sTheta]
        
        for param in range(len(line_edits)):
            if line_edits[param].text() != '':
                params_list[param] = float(line_edits[param].text())
        
        self.define_widthPixels(params_list[0])
        self.define_heightPixels(params_list[1])
        self.define_ccdx(params_list[2])
        self.define_ccdy(params_list[3])
        self.define_focalDist(params_list[4])
        self.define_sTheta(params_list[5])