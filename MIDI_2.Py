import pygame
import pygame.midi
from time import sleep

def midiExample():
    # Things to consider when using pygame.midi:
    #
    # 1) Initialize the midi module with a to pygame.midi.init().
    # 2) Create a midi.Output instance for the desired output device port.
    # 3) Select instruments with set_instrument() method calls.
    # 4) Play notes with note_on() and note_off() method calls.
    # 5) Call pygame.midi.Quit() when finished. Though the midi module tries
    #    to ensure that midi is properly shut down, it is best to do it
    #    explicitly. A try/finally statement is the safest way to do this.
    #
    GRAND_PIANO = 0
    CHURCH_ORGAN = 19
    instrument = CHURCH_ORGAN
    #instrument = GRAND_PIANO
    
    pygame.init()
    pygame.midi.init()

    port = 0
    print ("using output_id :%s:" % port)
    midi_out = pygame.midi.Output(port, 0)
    try:
        midi_out.set_instrument(instrument)

        midi_out.note_on(72,127) # 74 is middle C, 127 is "how loud" - max is 127
        sleep(.5)
        midi_out.note_off(72,127)
        sleep(.5)

        midi_out.note_on(76,127) # E
        sleep(.5)
        midi_out.note_off(76,127)
        sleep(.5)

        midi_out.note_on(79,127) # G
        sleep(.5)
        midi_out.note_off(79,127)
        sleep(.5)

        midi_out.note_on(72,127)
        midi_out.note_on(76,127)
        midi_out.note_on(79,127)
        sleep(.5)
        midi_out.note_off(72,127)
        midi_out.note_off(76,127)
        midi_out.note_off(79,127)

    finally:
        del midi_out
        pygame.midi.quit()

midiExample()
