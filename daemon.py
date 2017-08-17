#!/usr/bin/env python3

import sys
sys.path.append('./Networking')  # hack
import mido
import TCPClient
import json
import collections

mido.set_backend('mido.backends.pygame')
client = TCPClient.CreateClient("localhost", 9999)
currentState = {}
lastState = {}

midiMappings = {
    "buttons": {
        0: {
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
        1: {
            0: 'b_slider30',
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
        0: {
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
        1: {
            0: 'slider30',
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

try:
    with mido.open_input() as port:
        print('Using {}'.format(port))        
        while True:
            #Buffer updates
            for message in port.iter_pending():
                # print('Received {}'.format(message))
                if message.type == "note_off" or message.type == "note_on":
                    currentState.update({midiMappings["buttons"][message.channel][message.note]: message.type == "note_on"})
                if message.type == "control_change":
                    currentState.update({midiMappings["sliders"][message.channel][message.control]: round(message.value*100/127)})

            #Send updates 
            if currentState != lastState:
                lastState = currentState.copy()
                client.sendMessage(json.dumps(currentState))

except KeyboardInterrupt:
    pass