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

try:
    with mido.open_input() as port:
        print('Using {}'.format(port))        
        while True:
            for message in port.iter_pending():
                print('Received {}'.format(message))
                print(message.type) #note_off = button false, note_on = button true, control_change = slider value
                print(message.channel) #1 = secondary sliders, 2 = group sliders
                if message.type == "note_off" or message.type == "note_on":
                    print(message.note)
                    client.sendMessage(json.dumps({message.note: message.type == "note_on"}))

                if message.type == "control_change":
                    print(message.control)
                    print(message.value)
                    client.sendMessage(json.dumps({message.control: round(message.value*100/127)}))


except KeyboardInterrupt:
    pass