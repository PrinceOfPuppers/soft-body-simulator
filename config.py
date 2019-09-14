class Config:
    def __init__(self):
        self.fps=60
        self.pointSpaceing= 40
        self.dimensions=(5,5)
        self.bodyStart=500+10j
        self.pointMass=0.1
        self.springConst=100

        self.gravity=0j*self.pointMass
        self.screenSize=(1500,700)

        self.damping=1
        self.collisionDamping=0.3
        self.friction=0.3

        self.circleRadius=6