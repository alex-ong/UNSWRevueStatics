from Model import Channel

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

