from Model import Channel
import math
import sys
COLOR_DIRECT = 'yellow'
COLOR_PLAYBACK = 'cyan'
COLOR_GROUP = '#00ff00'
COLOR_RECORD = 'red'
COLOR_NONE = 'black'

GROUP = 'Group'
CHANNEL = 'Channel'

typeColourMapping = { Channel.ValueType.DIRECT : COLOR_DIRECT,
                     Channel.ValueType.PLAYBACK : COLOR_PLAYBACK,
                     Channel.ValueType.GROUP : COLOR_GROUP,
                     Channel.ValueType.RECORD : COLOR_RECORD,
                     Channel.ValueType.NONE: COLOR_NONE,
                     CHANNEL : COLOR_DIRECT,
                     GROUP : COLOR_GROUP,
                     None: COLOR_NONE}

# needs to be 16:9. Features are disabled as you reduce resolutions below 1366x768
# SCREEN_RESOLUTION = '3840x2160' # 4k
# SCREEN_RESOLUTION = '2560x1440' # "2k"
SCREEN_RESOLUTION = '1920x1080'  # base resolution
# SCREEN_RESOLUTION = '1366x768' # minimum res with full features
# SCREEN_RESOLUTION = '1280x720' # Disables sub-channel value display
# SCREEN_RESOLUTION = '1024x576' # minimum resolution

# note if this is set to true, it will overwrite screen resolution
SCREEN_RESOLUTION_AUTO = True
# auto screen resolution only supported in
if sys.platform == 'win32':
    if SCREEN_RESOLUTION_AUTO:
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        SCREEN_RESOLUTION = str(w) + 'x'+ str(h)



BASE_RESOLUTION = 1920  # don't change this.

# CHANGING THEME:
# To change font, all you have to do is modify font_size and FONT so that 
# gui lines up nicely pixel_size doesn't need to ever be changed
# If your font doesn't scale linearly with screen resolution, you might have to 
# modify font_size to deal with it


def screen_x():
    return int(SCREEN_RESOLUTION.split('x')[0])


def font_size(defaultSize):
    return round(screen_x() / BASE_RESOLUTION * defaultSize)


def pixel_size(defaultSize):
    return round(screen_x() / BASE_RESOLUTION * defaultSize)


FONT = 'Consolas'  # make sure you install this font! 

