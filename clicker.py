import pygame as pg
import os
import random
import math

pg.init()#Start Pygame
screen = pg.display.set_mode((500, 400))#Open a 500x400 pixel window. Does not accept transparent objects.
bg = pg.Surface((500, 400), pg.SRCALPHA)#Accepts transparent objects

class GameState:
    gameFont = pg.font.Font(None, 30)
    def __init__(self):
        self.Clicks = 0
        self.Pressed = 0;
        self.sprites = [];
        self.holding = False;
    def addClick(self,n):
        self.Clicks = self.Clicks + n
    def multiplyClick(self,n):
        self.Clicks = round(self.Clicks*n)
    def addSprite(self,sprite):
        self.sprites.append(sprite)
    def simulate(self):
        currentIndex = 0;
        while (currentIndex < len(self.sprites)):
            if self.sprites[currentIndex].simulate()==1:#Simulated sprite has requested its destruction
                self.sprites.pop(currentIndex)
                currentIndex = currentIndex - 1
            currentIndex = currentIndex + 1

class Snitch:
    snitchImages = [pg.image.load('graphics/Snitch %d.png'%i).convert_alpha() for i in range(7)];
    snitchSound=pg.mixer.Sound("snitch2.mp3")
    snitchSound.set_volume(.1)
    def __init__(self,startingYPos,gs):
        self.startingYPos=startingYPos;
        self.YPos=startingYPos;
        self.YVel = 0;
        self.WingIndex = 0;
        self.XPos = 300;
        self.XVel = 3;
        self.gs = gs;
        self.age = 0;
        self.wid = self.snitchImages[0].get_rect()[2]
        self.hgt = self.snitchImages[0].get_rect()[3]
        self.snitchSound.play(-1)
    def simulate(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.age > 60 and pg.mouse.get_pressed()[0] and not self.gs.Pressed:#Clicked somewhere
            hit_distance2 = (mouse_x-(self.XPos-self.wid/2))**2 + (mouse_y-(self.YPos-self.hgt/2))**2;
            if hit_distance2 < 65:#Counts as a hit
                self.age = 30;
                self.gs.multiplyClick(1.1)
                #TODO: Add a sound effect for catching the snitch
                self.XVel = 0;
                self.YVel = 0;
        if self.age < 10:
            self.WingIndex = 0
        elif self.age < 20:
            self.WingIndex = 1
        elif self.age < 30:
            self.WingIndex = 2
        elif self.age < 40:
            self.WingIndex = 3
        else: #Flying :)
            self.YVel=self.YVel*.99+(random.random()-.5)*2
            self.XVel=self.XVel*.99+(random.random()-.5)*2
            self.YPos=(self.YVel+self.YPos)%(400+self.hgt)
            self.XPos=(self.XVel+self.XPos)%(500+self.wid)
            self.WingIndex=self.age%3+4
        self.age = self.age+1
        bg.blit(self.snitchImages[self.WingIndex],(self.XPos-self.wid,self.YPos-self.hgt))

class Lamumu:
    images = [pg.image.load('graphics/lamumu %d.png'%i).convert_alpha() for i in range(7)];
    #snitchSound=pg.mixer.Sound("snitch2.mp3")
    #snitchSound.set_volume(.1)
    def __init__(self,startingYPos,gs):
        self.startingYPos=startingYPos;
        self.YPos=startingYPos;
        self.YVel = 0;
        self.XPos = 300;
        self.XVel = 0;
        self.gs = gs;
        self.age = 0;
        self.wid = self.images[0].get_rect()[2]
        self.hgt = self.images[0].get_rect()[3]
        self.holding = False
        self.mouseOffsets = [0,0]
        randomRoll = random.random();
        if randomRoll < .001:
            self.lamumuType = 6
        elif randomRoll < 0.003:
            self.lamumuType = 5
        elif randomRoll < 0.01:
            self.lamumuType = 4
        elif randomRoll < 0.03:
            self.lamumuType = 3
        elif randomRoll < 0.1:
            self.lamumuType = 2
        elif randomRoll < 0.3:
            self.lamumuType = 1
        elif randomRoll < 1:
            self.lamumuType = 0
        #self.snitchSound.play(-1)
    def simulate(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if not self.gs.holding and self.images[0].get_rect().collidepoint(mouse_x-self.XPos, mouse_y-self.YPos) and pg.mouse.get_pressed()[0] and not self.gs.Pressed:#Clicking on the lamumu picks it up
            self.holding = True
            self.gs.holding = True
            self.mouseOffsets = [self.XPos - mouse_x,self.YPos - mouse_y]

        if self.holding and not pg.mouse.get_pressed()[0]:
            self.holding = False
            self.gs.holding = False
            self.XPos = self.XPos + self.mouseOffsets[0]
            self.YPos = self.YPos + self.mouseOffsets[1]
            self.mouseOffsets = [0,0]

        if self.holding:
            self.YVel = mouse_y - self.YPos
            self.XVel = mouse_x - self.XPos
            self.XPos = mouse_x
            self.YPos = mouse_y
        else:
            self.XPos = self.XPos + self.XVel
            self.YPos = self.YPos + self.YVel
        
        #TODO: animate the thing appearing, etc
        bg.blit(self.images[self.lamumuType],(self.XPos + self.mouseOffsets[0],self.YPos + self.mouseOffsets[1]))
        

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
    def __init__(self,gs,upgradeText,upgradePrice,upgradeChild,YPos):
        self.gs = gs
        self.upgradeText = upgradeText
        self.upgradePrice = upgradePrice
        self.upgradeChild = upgradeChild
        self.XPos = 10
        self.YPos = YPos
        self.rect = pg.Rect(self.XPos,self.YPos,250,30)
    def simulate(self):
        #Handle button clicks
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y) and pg.mouse.get_pressed()[0] and self.gs.Clicks >= self.upgradePrice and not self.gs.Pressed:
             self.gs.addClick(-self.upgradePrice)
             self.gs.addSprite(self.upgradeChild(50+30*round(8*random.random()),self.gs))
             self.upgradePrice = self.upgradePrice*1.1
        #Draw the button onto the screen
        buttonColor = (225,225,225)
        textColor = (30,60,50)
        if self.gs.Clicks < self.upgradePrice:
            buttonColor = (180,180,180)
            textColor = (160,160,150)
        button=pg.draw.rect(bg,buttonColor,self.rect,0,10)
        #TO DO: Draw text describing the upgrade
        description = GameState.gameFont.render(self.upgradeText + ": %d"%self.upgradePrice,False,textColor)
        bg.blit(description,[10+8,self.YPos+5,200,100]);

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
    upgrades = [UpgradeButton(gs,"Buy a bus",4,Bus,280),UpgradeButton(gs,"Harry Pooter",8,Snitch,320),UpgradeButton(gs,"Lamumu",1,Lamumu,360)]
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
