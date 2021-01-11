import configparser
import os


class AstroConfig:

    def __init__(self):
        _configdir = os.path.expanduser("~") + '/.config/astrostream/'
        if not os.path.exists(_configdir):
            os.makedirs(_configdir)
        _configfile = _configdir + 'main.cfg'
        _config = configparser.SafeConfigParser({
            'youtube_key': 'your_key',
            'twitch_key': 'your_key',
            'libpath': '/usr/lib/x86_64-linux-gnu/libASICamera2.so',
        })

        _config.read(_configfile)

        if not os.path.isfile(_configfile):
            print("Config file does not exist")
            with open(_configfile, 'wt') as configfile:
                _config.write(configfile)

        self.settings = _config.defaults()
