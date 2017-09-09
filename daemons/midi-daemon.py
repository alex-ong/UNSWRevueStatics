#!/usr/bin/env python3

import sys
sys.path.append('./Networking')  # hack to run from main folder
sys.path.append('../Networking')  # hack to run from this folder
import ButtonDebouncer
import SliderDebouncer
import TCPClient
import json
import collections
import time
import rtmidi
from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import (CONTROLLER_CHANGE, NOTE_ON, NOTE_OFF)

client = TCPClient.CreateClient("localhost", 9999)

# the following are the current/previous states. we use this to know when to send data.
currentState = {}
lastState = {}

B_SLIDERS = ['b_slider' + str(i) for i in range(1, 28)] + ['b_slider-1']
B_BUTTONS = ['DBO', 'Back', 'Release', 'Next']
B_LIST = B_SLIDERS + B_BUTTONS
SLIDER_LIST = ['slider' + str(i) for i in range(1, 28)] + ['slider-1']


class DebouncedDictionary(object):
    def __init__(self):
        buttonDebouncers = {buttonName: ButtonDebouncer.ButtonDebouncer(buttonName, 
                                                                        lambda name, value: currentState.update({name, value})) 
                                                                        for buttonName in B_LIST}
        sliderDebouncers = {sliderName: SliderDebouncer.SliderDebouncer(sliderName, 
                                                                        lambda name, value: currentState.update({name, value}))
                                                                        for sliderName in SLIDER_LIST}
        # merge the two dictionaries of debouncers
        buttonDebouncers.update(sliderDebouncers)
        self.debouncers = buttonDebouncers
    
    def updateTime(self, timeStamp):
        # todo change to value in self.debouncers.values()
        for (key, value) in self.debouncers.items():
            value.update(timeStamp)
            
    def updateValue(self, key, value):
        if key in self.debouncers:
            self.debouncers[key].receiveInput(value, time.time())
        
DEBOUNCE_DICT = DebouncedDictionary()
 
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
            key = MIDI_MAP["buttons"][channel][message[1]]
            value = (status == NOTE_ON)
            DEBOUNCE_DICT.updateValue(key, value)  # debounceDict will decide final value to send
        elif status == CONTROLLER_CHANGE:
            key = MIDI_MAP["sliders"][channel][message[1]]
            value = round(message[2] * 100 / 127)
            DEBOUNCE_DICT.update(key, value)
        
if __name__ == '__main__':      
    try:
        midiin, port_name = open_midiinput(0)
        midiin1, port_name1 = open_midiinput(1)
    except (EOFError, KeyboardInterrupt):
        print("Failed to connect to midi inputs! Press enter to exit...")
        _ = input()
        sys.exit()
    except OSError as e:
        print ('Received OSError:' + str(e))
        print ("Press enter to exit...")
        _ = input()
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
            # 100 fps refresh rate 
            time.sleep(0.01)

    except KeyboardInterrupt:
        print('Received KeyboardInterrupt')
    finally:
        print("Exiting.")
        midiin.close_port()
        midiin1.close_port()
        del midiin
        del midiin1
