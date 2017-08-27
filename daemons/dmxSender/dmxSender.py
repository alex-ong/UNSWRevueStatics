# change the line below to switch DMX libraries
DMX_LIB = "DMX_PY"
#DMX_LIB = "pySimpleDMX"
import sys

try:
    import serial
except:
    print ("Please pip-install pyserial")
    print ("Press enter to exit...")
    _ = input()    
    sys.exit()
    
if DMX_LIB == "DMX_PY": 
    from .DmxPy.DmxPy import DmxPy as DmxSender
elif DMX_LIB == "pySimpleDMX":
    from .pySimpleDMX.pysimpledmx import DMXConnection as DmxSender
    
# both classes have the same Pattern
# Constructor:
# s = DmxSender(port)
# Usage:
# s.setChannel(channelNumber, byteValue)
# s.render() pushes the value to the com port
