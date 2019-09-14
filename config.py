import tkinter
class Config:
    def __init__(self):
        self.fps=60
        self.pointSpaceing= 40
        self.dimensions=(5,7)

        self.pointMass=0.1
        self.springConst=100

        self.gravity=400j*self.pointMass

        self.damping=1
        self.collisionDamping=0.3
        self.friction=0.3

        self.circleRadius=6


        #screen dimensions and scaling
        root=tkinter.Tk()
        self.devScreenWidth=1500
        screenWidth=root.winfo_screenwidth()-100
        screenHeight=root.winfo_screenheight()-100
        self.screenSize=[screenWidth,screenHeight]

        self.widthRatio=screenWidth/self.devScreenWidth
        self.scaleToScreenWidth()

    def scaleToScreenWidth(self):
        self.pointSpaceing*=self.widthRatio


        self.gravity*=self.widthRatio
        self.circleRadius*=self.widthRatio
        self.circleRadius=int(self.circleRadius)


        self.bodyStart=(self.screenSize[0]-self.dimensions[0]*self.pointSpaceing)/2 +(self.screenSize[1]-self.dimensions[1]*self.pointSpaceing)*1j/2