#!/usr/bin/env python3

import sys
sys.path.append('./Networking')  # hack
import TCPClient
import json
import collections
import time
import rtmidi
from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import (CONTROLLER_CHANGE, NOTE_ON, NOTE_OFF)

client = TCPClient.CreateClient("localhost", 9999)
currentState = {}
lastState = {}

MIDI_MAP = {
    "buttons": {
        1: {
            0: 'b_slider1',
            1: 'b_slider2',
            2: 'b_slider3',
            3: 'b_slider4',
            4: 'b_slider5',
            5: 'b_slider6',
            6: 'b_slider7',
            7: 'b_slider8',
            8: 'b_slider9',
            9: 'b_slider10',
            10: 'b_slider11',
            11: 'b_slider12',
            12: 'b_slider13',
            13: 'b_slider14',
            14: 'b_slider15',
            15: 'b_slider16',
            16: 'b_slider17',
            17: 'b_slider18'
        },
        2: {
            0: 'b_slider-1',
            1: 'b_slider19',
            2: 'b_slider20',
            3: 'b_slider21',
            4: 'b_slider22',
            5: 'b_slider23',
            6: 'b_slider24',
            7: 'b_slider25',
            8: 'b_slider26',
            9: 'b_slider27',
            10: 'DBO',
            11: 'Back',
            12: 'Release',
            13: 'Next'
        },
    },
    "sliders": {
        1: {
            0: 'slider1',
            1: 'slider2',
            2: 'slider3',
            3: 'slider4',
            4: 'slider5',
            5: 'slider6',
            6: 'slider7',
            7: 'slider8',
            8: 'slider9',
            9: 'slider10',
            10: 'slider11',
            11: 'slider12',
            12: 'slider13',
            13: 'slider14',
            14: 'slider15',
            15: 'slider16',
            16: 'slider17',
            17: 'slider18'
        },
        2: {
            0: 'slider-1',
            1: 'slider19',
            2: 'slider20',
            3: 'slider21',
            4: 'slider22',
            5: 'slider23',
            6: 'slider24',
            7: 'slider25',
            8: 'slider26',
            9: 'slider27'
        },
    }
}

class MidiInputHandler(object):
    def __call__(self, event, data=None):
        message, deltatime = event
        channel = (message[0] & 0xF) + 1
        status = message[0] & 0xF0
        if status == NOTE_OFF or status == NOTE_ON:
            currentState.update({MIDI_MAP["buttons"][channel][message[1]]: status == NOTE_ON})
        if status == CONTROLLER_CHANGE:
            currentState.update({MIDI_MAP["sliders"][channel][message[1]]: round(message[2]*100/127)})

try:
    midiin, port_name = open_midiinput(0)
    midiin1, port_name1 = open_midiinput(1)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler())
midiin1.set_callback(MidiInputHandler())

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        if currentState != lastState:
            lastState = currentState.copy()
            client.sendMessage(json.dumps(currentState))
        time.sleep(0.01)
except KeyboardInterrupt:
    print('Interrupt')
finally:
    print("Exit.")
    midiin.close_port()
    midiin1.close_port()
    del midiin
    del midiin1