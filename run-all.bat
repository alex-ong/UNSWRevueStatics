@echo off
start python daemons/midi-daemon.py 0
start python daemons/midi-daemon.py 1
start python daemons/dmx-daemon.py COM8
start python main.py
exit