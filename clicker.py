import pygame as pg
import os
import random
import math

pg.init()#Start Pygame
screen = pg.display.set_mode((500, 400))#Open a 500x400 pixel window. Does not accept transparent objects.
bg = pg.Surface((500, 400), pg.SRCALPHA)#Accepts transparent objects

class GameState:
    def __init__(self):
        self.Clicks = 0
        self.Pressed = 0;
        self.sprites = [];
    def addClick(self,n):
        self.Clicks = self.Clicks + n
    def addSprite(self,sprite):
        self.sprites.append(sprite)
    def simulate(self):
        currentIndex = 0;
        while (currentIndex < len(self.sprites)):
            if self.sprites[currentIndex].simulate()==1:#Simulated sprite has requested its destruction
                self.sprites.pop(currentIndex)
                currentIndex = currentIndex - 1
            currentIndex = currentIndex + 1

class Bus:
    busImages = [pg.image.load('graphics/blue bus %d.png'%i).convert_alpha() for i in range(5)];
    bumpSound=pg.mixer.Sound("BlueBusBump.mp3")
    bumpSound.set_volume(.1)
    def __init__(self,startingYPos,gs):
        self.startingYPos=startingYPos;
        self.YPos=startingYPos;
        self.YVel=0;
        self.BusDamageIndex = 0;
        self.XPos=-self.getImage().get_rect()[2]
        self.XVel=3;
        self.gs = gs;
    def getImage(self):
        return self.busImages[self.BusDamageIndex]
    def simulate(self):#Advance the bus to its next simulated physics state
        if self.BusDamageIndex==4: #The driver is without a bus.
            self.XPos = self.XPos + 1;
            bg.blit(self.getImage(),(self.XPos,self.YPos))
            if (self.XPos>1000):
                return 1 #Remove the bus object from the sprites list
        else:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.getImage().get_rect().collidepoint(mouse_x-self.XPos, mouse_y-self.YPos) and pg.mouse.get_pressed()[0] and self.gs.Clicks > 0 and not self.gs.Pressed:#Clicking on the bus increases its X Velocity
                self.XVel = self.XVel + 4
                self.gs.addClick(-1)
                #TO DO: Make a sound of coins going into the payment machine
            self.XPos = self.XPos + self.XVel
            if self.XPos > 500:
                self.XPos=self.XPos-500-self.getImage().get_rect()[2] # Wrap bus
            self.YVel=self.YVel+.75 #Gravitational Acceleration
            if random.random()<0.01*self.XVel and self.YPos==self.startingYPos:#Bus is driving on its ground level and hits a random bump
                self.YVel=self.YVel-2*math.sqrt(self.XVel)
                self.gs.addClick(1)
                self.bumpSound.play()
                if random.random()<0.1:
                    self.BusDamageIndex = min(self.BusDamageIndex + 1,len(self.busImages)-1);
                    self.XVel = 0;
                    #TO DO: Draw an explosion GIF?
            if random.random()<0.01 and self.YPos==self.startingYPos and self.XVel > 0:#Bus breaks down
                self.XVel = self.XVel - 1
                #TO DO: If we break down to speed zero, play a sound of the driver saying "Not again!"
            self.YPos=self.YPos+self.YVel
            if self.YPos>self.startingYPos:#Bus lands back on its ground level
                self.YPos=self.startingYPos
                self.YVel=0
            TemporaryYPos = self.YPos-math.sin(abs(self.YVel)*math.pi/180)*self.getImage().get_rect()[2]/2;
            bg.blit(pg.transform.rotate(self.getImage(),-self.YVel),(self.XPos,TemporaryYPos))
            
            NumberOfFlames = self.XVel//10
            for FlameI in range(NumberOfFlames):
                SmokeX = self.XPos + self.getImage().get_rect()[2]/2 - 30*NumberOfFlames*random.random()
                SmokeY = TemporaryYPos + self.getImage().get_rect()[3] - 15*random.random()
                SmokeRadius = NumberOfFlames*3*random.random();
                SmokeColor = self.XVel*5;
                SmokeBlue = max(min(255-SmokeColor,255),0);
                pg.draw.circle(bg,(255,255,SmokeBlue,125),(SmokeX,SmokeY),SmokeRadius);
        return 0 #Bus simulation exits normally with a 0

class UpgradeButton:
    def __init__(self,gs,upgradePrice,upgradeChild,YPos):
        self.gs = gs
        self.upgradePrice = upgradePrice
        self.upgradeChild = upgradeChild
        self.XPos = 10
        self.YPos = YPos
        self.rect = pg.Rect(self.XPos,self.YPos,128,30)
    def simulate(self):
        #Handle button clicks
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y) and pg.mouse.get_pressed()[0] and self.gs.Clicks >= self.upgradePrice and not self.gs.Pressed:
             self.gs.addClick(-self.upgradePrice)
             self.gs.addSprite(self.upgradeChild(50+30*round(8*random.random()),self.gs))
        #Draw the button onto the screen
        drawColor = (225,225,225)
        if self.gs.Clicks < self.upgradePrice:
            drawColor = (180,180,180)
        button=pg.draw.rect(bg,drawColor,self.rect,0,10)
        #TO DO: Draw text describing the upgrade

def main():#Create the main function

    SpaceBar=pg.image.load('graphics/Button1.png').convert_alpha()
    SpaceBarGoingDown=pg.image.load('graphics/Button2.png').convert_alpha()
    SpaceBarDown=pg.image.load('graphics/Button3.png').convert_alpha()
    SpaceBar=pg.transform.scale_by(SpaceBar,1)
    pg.mixer.init()
    Beep=pg.mixer.Sound("Easytotype.mp3")
    bg.fill((127, 127, 127))#fill the background gray
    clock = pg.time.Clock()#Get a copy of the clock object (slow?)
    pg.font.init()#Set up all fonts for use (probably not needed)
    font1 = pg.font.Font(None, 100)#Get a copy of the default font

    #Initialize Game State
    gs = GameState();
    #Initialize upgrade list
    upgrades = [UpgradeButton(gs,4,Bus,280)]
    #For testing:
    #buses = [Bus(50+30*i,gs) for i in range(8)];

    while True:#Main game loop (continues forever)
        clock.tick(50)#Run at 50 Frames per second
        for event in pg.event.get():#Look for standard events
            if event.type == pg.QUIT:#User clicked the window close button
                pg.quit()#Tell Pygame to quit
                raise SystemExit#Error out the program
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    gs.addClick(1)
                    Beep.play()
        #Erase the screen
        bg.fill((127, 127, 127))#fill the background gray
        # Initialize Button
        Button=pg.draw.rect(
            bg,
            (255,127.5,0),
            (0,100,1000,25)
            )
        mouse_x, mouse_y = pg.mouse.get_pos()

        SpaceBarXPos=bg.get_rect()[2]/2-SpaceBar.get_rect()[2]/2
        if SpaceBar.get_rect().collidepoint(mouse_x-SpaceBarXPos, mouse_y-200) and pg.mouse.get_pressed()[0] or pg.key.get_pressed()[pg.K_SPACE]:
            bg.blit(SpaceBarGoingDown,(SpaceBarXPos,200))
        else:
            bg.blit(SpaceBar,(SpaceBarXPos,200))
        
        if SpaceBar.get_rect().collidepoint(mouse_x-SpaceBarXPos, mouse_y-200) and pg.mouse.get_pressed()[0] and not gs.Pressed:
            gs.addClick(1)
            Beep.play()
        #Update the text
        button_text = font1.render("Clicks:%d"%gs.Clicks, False, (0, 0, 0))#Like printing this text onto a slip of paper...
        bg.blit(button_text,[0,0,200,100]);#...which we glue onto the screen at the rectangle coordinates 0,0, which is the upper left corner, because of computer graphics conventions.
        #Update the bus
        #[bus.simulate() for bus in buses];
        gs.simulate()
        #Upgrades
        [upgrade.simulate() for upgrade in upgrades]

        #Draw bg to screen (to fix the transparency problem)
        screen.blit(bg,(0,0))
        
        gs.Pressed=pg.mouse.get_pressed()[0]
        pg.display.update()#Draw the display


if __name__ == "__main__":#If you run this as the top level program, like "python3 clicker.py" from command line
    main()#Run the main function
