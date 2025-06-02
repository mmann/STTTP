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
    def addClick(self,n):
        self.Clicks = self.Clicks + n

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
    #TO DO: User can click on the bus to speed it up

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

    #Initialize Pressed
    gs = GameState();
    #For testing:
    buses = [Bus(50+30*i,gs) for i in range(8)];

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
        [bus.simulate() for bus in buses];
        #Upgrades
        BusButton=pg.draw.rect(bg,(225,225,225),(10,280,128,30),0,10)

        #Draw bg to screen (to fix the transparency problem)
        screen.blit(bg,(0,0))
        
        gs.Pressed=pg.mouse.get_pressed()[0]
        pg.display.update()#Draw the display


if __name__ == "__main__":#If you run this as the top level program, like "python3 clicker.py" from command line
    main()#Run the main function
