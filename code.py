import random
import time

import usb_midi

import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend

print(usb_midi.ports)
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0)

print("Midi test")
# Convert channel numbers at the presentation layer to the ones musicians use
print("Default output channel:", midi.out_channel + 1)
print("Listening on input channel:", midi.in_channel + 1)


import board
import digitalio
from adafruit_debouncer import Button as AdafruitButton

class Button(AdafruitButton):
    def __init__(self, pin, pressedMidi=None, releasedMidi=None):
        self.pin = pin
        b = digitalio.DigitalInOut(pin)
        b.direction = digitalio.Direction.INPUT
        b.pull = digitalio.Pull.UP
        AdafruitButton.__init__(self, b)

        self.pressedMidi = pressedMidi
        self.releasedMidi = releasedMidi


bA = Button(board.D0, NoteOn("C1", 127), NoteOff("C1", 0))
bB = Button(board.D1, NoteOn("C#1", 127), NoteOff("C#1", 0))
bC = Button(board.D2, NoteOn("D1", 127), NoteOff("D1", 0))
bD = Button(board.D3, NoteOn("D#1", 127), NoteOff("D#1", 0))

buttons = [bA, bB, bC, bD]

while True:
    for btn in buttons:
        btn.update()

        if btn.pressed:
            print("Button on pin %d pressed", btn.pin)
            if btn.pressedMidi:
                midi.send(btn.pressedMidi)
        if btn.released:
            print("Button on pin %d released", btn.pin)
            if btn.releasedMidi:
                midi.send(btn.releasedMidi)
