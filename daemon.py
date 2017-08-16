#!/usr/bin/env python3

import sys
from _collections import OrderedDict
sys.path.append('./Networking')  # hack
import mido
import TCPClient
import json
import collections

mido.set_backend('mido.backends.pygame')
client = TCPClient.CreateClient("localhost", 9999)

midiMappings = {
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
    }
}

try:
    with mido.open_input() as port:
        print('Using {}'.format(port))        
        while True:
            for message in port.iter_pending():
                print('Received {}'.format(message))
                if message.type == "note_off" or message.type == "note_on":
                    client.sendMessage(json.dumps({midiMappings["buttons"][message.channel][message.note]: message.type == "note_on"}))
                if message.type == "control_change":
                    client.sendMessage(json.dumps({midiMappings["sliders"][message.channel][message.control]: round(message.value*100/127)}))


except KeyboardInterrupt:
    pass