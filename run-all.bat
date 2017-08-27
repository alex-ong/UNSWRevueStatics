@echo off
start python daemons/midi-daemon.py
start python daemons/dmx-daemon.py COM4
start python main.py
exit