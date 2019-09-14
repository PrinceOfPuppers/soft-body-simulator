import pygame as pg
from body import Body
from config import Config
class GameManager: 
    def __init__(self,config):

        self.hasQuit=False
        self.tickNumber=0

        self.clock=pg.time.Clock()

        self.config=config
        self.fps=config.fps
        self.spf=1/config.fps
        self.body=Body(config)
        self.screenSize=config.screenSize
        self.display=pg.display.set_mode((config.screenSize[0], config.screenSize[1]))


    def applyControls(self):
        mousePos=pg.mouse.get_pos()[0]+pg.mouse.get_pos()[1]*1j
        for event in pg.event.get():
            # checks if user has quit
            if event.type == pg.QUIT:
                self.hasQuit=True

            elif event.type==pg.MOUSEBUTTONDOWN:
                self.body.teatherNearest(mousePos)
            
            elif event.type==pg.MOUSEBUTTONUP:
                self.body.releaseTeather()

        return(mousePos)
                
    def gameLoop(self):
        pg.init()
        pg.display.set_caption("Jelly Boi")
        while not self.hasQuit:
            mousePos=self.applyControls()
            print(self.clock)
            self.tickNumber+=1
            self.clock.tick_busy_loop(self.fps)
            self.body.handler(self.display,self.spf,self.tickNumber,mousePos)
            pg.display.update()
            pg.Surface.fill(self.display,(0,0,0))
            

if __name__=="__main__":
    cfg=Config()
    gameMgr=GameManager(cfg)
    gameMgr.gameLoop()