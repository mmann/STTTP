import pygame as pg
import os


def main():#Create the main function
    pg.init()#Start Pygame
    bg = pg.display.set_mode((500, 400))#Open a 500x400 pixel window
    bg.fill((127, 127, 127))#fill the background gray
    clock = pg.time.Clock()#Get a copy of the clock object (slow?)
    pg.font.init()#Set up all fonts for use (probably not needed)
    font1 = pg.font.Font(None, 100)#Get a copy of the default font
    frame = 0;
    while True:#Main game loop (continues forever)
        clock.tick(50)#Wait 50 milliseconds to give the CPU some rest
        for event in pg.event.get():#Look for standard events
            if event.type == pg.QUIT:#User clicked the window close button
                pg.quit()#Tell Pygame to quit
                raise SystemExit#Error out the program
        #Erase the screen
        bg.fill((127, 127, 127))#fill the background gray
        
        #Update the text
        button_text = font1.render("Frame:%d"%frame, False, (0, 0, 0))#Like printing this text onto a slip of paper...
        bg.blit(button_text,[0,0,200,100]);#...which we glue onto the screen at the rectangle coordinates 0,0, which is the upper left corner, because of computer graphics conventions.
    
        pg.display.update()#Draw the display
        
        frame = frame + 1;#Increment the frame number

if __name__ == "__main__":#If you run this as the top level program, like "python3 clicker.py" from command line
    main()#Run the main function
    