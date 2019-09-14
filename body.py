from numpy import zeros,around,conj,inf,array
from math import floor
import pygame as pg
from math import sqrt
class Body:
    def __init__(self,config):
        self.points=zeros(config.dimensions,dtype=complex)
        self.pointVels=zeros(config.dimensions,dtype=complex)
        self.dimensions=config.dimensions
        self.pointSpaceing=config.pointSpaceing

        self.gravity=config.gravity
        self.pointMass=config.pointMass
        self.springConst=config.springConst
        self.damping=config.damping
        self.constructBody(config.bodyStart)

        self.screenSize=config.screenSize
        self.collisionDamping=config.collisionDamping
        self.friction=config.friction

        self.pointIsTeathered=False
        self.pointTeatheredIndex=array((-1,-1),dtype=int)
        self.teatherLength=-1
        self.circleRadius=config.circleRadius
    def constructBody(self,topLeftPoint):
        for xIndex in range(0,self.dimensions[0]):
            for yIndex in range(0,self.dimensions[1]):
                self.points[xIndex,yIndex]=topLeftPoint+xIndex*self.pointSpaceing+yIndex*self.pointSpaceing*1j
                self.pointVels[xIndex,yIndex]=0

    def applyForces(self,deltaT,externalForces,display):
        #external forces are things applied uniformly to each point (ie gravity)

        #for each point...
        for xIndex in range(0,self.dimensions[0]):
            for yIndex in range(0,self.dimensions[1]):
                #...apply acceleration caused by all adjacent points
                for offsets in ((1,0),(1,1),(0,1),(-1,1)): 
                    offsetX=offsets[0]
                    offsetY=offsets[1]
                    #checks if index is valid
                    if xIndex+offsetX>=0 and yIndex+offsetY>=0:
                        if xIndex+offsetX<self.dimensions[0] and yIndex+offsetY<self.dimensions[1]:
                            #actually applies the force
                            offsetLen=round(sqrt(offsetX**2+offsetY**2),5)
                            displacementVec=self.points[xIndex+offsetX,yIndex+offsetY]-self.points[xIndex,yIndex]
                            displacement=abs(displacementVec)

                            velVec=self.pointVels[xIndex+offsetX,yIndex+offsetY]-self.pointVels[xIndex,yIndex]
                            deltaDisplacement=(velVec.real*displacementVec.real +velVec.imag*displacementVec.imag)/(displacement**2)

                            force=around((self.springConst) * (1-self.pointSpaceing*offsetLen/displacement)*displacementVec +self.damping*deltaDisplacement*displacementVec,5)
                            
                            self.pointVels[xIndex,yIndex]+=force*deltaT/self.pointMass
                            self.pointVels[xIndex+offsetX, yIndex+offsetY]-=force*deltaT/self.pointMass
                            
                            #draws lines
                            colorMod=abs(1-self.pointSpaceing*offsetLen/displacement)
                            if colorMod>1:
                                colorMod=1
                            point1=self.points[xIndex+offsetX,yIndex+offsetY]
                            point2=self.points[xIndex,yIndex]
                            pg.draw.aaline(display, (255,int(255-255*colorMod),int(255-255*colorMod)),(point1.real,point1.imag), (point2.real,point2.imag))
                #applys externalForces
                self.pointVels[xIndex,yIndex]+=externalForces*deltaT/self.pointMass

                #applies boundry forces
                #real axis
                if self.points[xIndex,yIndex].real<=0:
                    self.pointVels[xIndex,yIndex]=abs(self.pointVels[xIndex,yIndex].real*(1-self.collisionDamping))+(1-self.friction)*self.pointVels[xIndex,yIndex].imag*1j

                if self.points[xIndex,yIndex].real>=self.screenSize[0]:
                    self.pointVels[xIndex,yIndex]=-abs(self.pointVels[xIndex,yIndex].real*(1-self.collisionDamping))+(1-self.friction)*self.pointVels[xIndex,yIndex].imag*1j
                
                #imag axis
                if self.points[xIndex,yIndex].imag<=0:
                    self.pointVels[xIndex,yIndex]=(1-self.friction)*self.pointVels[xIndex,yIndex].real+abs((self.pointVels[xIndex,yIndex].imag*(1-self.collisionDamping)))*1j

                if self.points[xIndex,yIndex].imag>=self.screenSize[1]:
                    self.pointVels[xIndex,yIndex]=(1-self.friction)*self.pointVels[xIndex,yIndex].real-abs((self.pointVels[xIndex,yIndex].imag*(1-self.collisionDamping)))*1j

    def applyMotion(self,deltaT):
        self.points+=self.pointVels*deltaT
        self.points=self.points

    def findNearestPointIndex(self,point):
        minDist=inf
        x,y=-1,-1
        for xIndex in range(0,self.dimensions[0]):
            for yIndex in range(0,self.dimensions[1]):
                dist=abs(self.points[xIndex,yIndex]-point)
                if dist<minDist:
                    minDist=dist
                    x,y=xIndex,yIndex
        return(x,y)

    def drawNearest(self,display,mousePos):
        if self.pointIsTeathered:
            x,y=self.pointTeatheredIndex[0],self.pointTeatheredIndex[1]
        else:
            x,y=self.findNearestPointIndex(mousePos)
        point=(int(self.points[x,y].real),int(self.points[x,y].imag))
        pg.draw.circle(display,(255,0,0),point,self.circleRadius,2)

    def teatherNearest(self,mousePos):
        self.pointIsTeathered=True
        x,y=self.findNearestPointIndex(mousePos)
        self.pointTeatheredIndex[0]=x
        self.pointTeatheredIndex[1]=y
        self.teatherLength=abs(self.points[x,y]-mousePos)

    def releaseTeather(self):
        self.pointIsTeathered=False

    def applyTeather(self,display,deltaT,mousePos):
        
        xIndex=self.pointTeatheredIndex[0]
        yIndex=self.pointTeatheredIndex[1]
        displacementVec=mousePos-self.points[xIndex,yIndex]
        displacement=abs(displacementVec)
        colorMod=0
        if displacement>self.teatherLength:
            velVec=-self.pointVels[xIndex,yIndex]
            deltaDisplacement=(velVec.real*displacementVec.real +velVec.imag*displacementVec.imag)/(displacement**2)

            force=around((self.springConst) * (1-self.teatherLength/displacement)*displacementVec +self.damping*deltaDisplacement*displacementVec,5)

            self.pointVels[xIndex,yIndex]+=force*deltaT/self.pointMass

            #draws lines
            colorMod=abs(1-self.teatherLength/displacement)
            if colorMod>1:
                colorMod=1
        pg.draw.aaline(display, (255,int(255-255*colorMod),int(255-255*colorMod)),(mousePos.real,mousePos.imag), (self.points[xIndex,yIndex].real,self.points[xIndex,yIndex].imag))

    def handler(self,display,deltaT,tickNumber,mousePos):
        self.applyForces(deltaT,self.gravity,display)
        self.applyMotion(deltaT)
        self.drawNearest(display,mousePos)
        if self.pointIsTeathered:
            self.applyTeather(display,deltaT,mousePos)



