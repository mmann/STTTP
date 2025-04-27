import pygame as pg
import os
import random
import math


def main():#Create the main function

    pg.init()#Start Pygame
    bg = pg.display.set_mode((500, 400))#Open a 500x400 pixel window

    SpaceBar=pg.image.load('graphics/Button1.png').convert_alpha()
    SpaceBarGoingDown=pg.image.load('graphics/Button2.png').convert_alpha()
    SpaceBarDown=pg.image.load('graphics/Button3.png').convert_alpha()
    BlueBusUpgrade = pg.image.load('graphics/blue bus.png').convert_alpha()
    SpaceBar=pg.transform.scale_by(SpaceBar,1)
    pg.mixer.init()
    Beep=pg.mixer.Sound("Easytotype.mp3")
    bg.fill((127, 127, 127))#fill the background gray
    clock = pg.time.Clock()#Get a copy of the clock object (slow?)
    pg.font.init()#Set up all fonts for use (probably not needed)
    font1 = pg.font.Font(None, 100)#Get a copy of the default font
    Clicks = 0;
    BlueBusXPos=-BlueBusUpgrade.get_rect()[2]
    #Initialize Pressed
    Pressed=0;
    BlueBusYPos=200;
    BlueBusYVel=0;

    while True:#Main game loop (continues forever)
        clock.tick(50)#Run at 50 Frames per second
        for event in pg.event.get():#Look for standard events
            if event.type == pg.QUIT:#User clicked the window close button
                pg.quit()#Tell Pygame to quit
                raise SystemExit#Error out the program
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    Clicks=Clicks+1
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
        if BlueBusXPos<550:
            BlueBusXPos=BlueBusXPos+1
        else:
            BlueBusXPos=-BlueBusUpgrade.get_rect()[2] # Wrap bus
        if SpaceBar.get_rect().collidepoint(mouse_x-0, mouse_y-200) and pg.mouse.get_pressed()[0] or pg.key.get_pressed()[pg.K_SPACE]:
            bg.blit(SpaceBarGoingDown,(SpaceBarXPos,200))
        else:
            bg.blit(SpaceBar,(SpaceBarXPos,200))
        BlueBusYVel=BlueBusYVel+.75 #Gravitational Acceleration
        if random.random()<0.01 and BlueBusYPos==200:
            BlueBusYVel=BlueBusYVel-5
        BlueBusYPos=BlueBusYPos+BlueBusYVel
        if BlueBusYPos>200:
            BlueBusYPos=200
            BlueBusYVel=0
        bg.blit(pg.transform.rotate(BlueBusUpgrade,-BlueBusYVel),(BlueBusXPos,BlueBusYPos-math.sin(abs(BlueBusYVel)*math.pi/180)*BlueBusUpgrade.get_rect()[2]/2))
      
        if SpaceBar.get_rect().collidepoint(mouse_x-0, mouse_y-200) and pg.mouse.get_pressed()[0] and not Pressed:
            Clicks=Clicks+1
            Beep.play()
        Pressed=pg.mouse.get_pressed()[0]
        #Update the text
        button_text = font1.render("Clicks:%d"%Clicks, False, (0, 0, 0))#Like printing this text onto a slip of paper...
        bg.blit(button_text,[0,0,200,100]);#...which we glue onto the screen at the rectangle coordinates 0,0, which is the upper left corner, because of computer graphics conventions.
    
        pg.display.update()#Draw the display


if __name__ == "__main__":#If you run this as the top level program, like "python3 clicker.py" from command line
    main()#Run the main function
