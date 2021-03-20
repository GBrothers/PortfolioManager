import sys
from pathlib import Path
import configparser

IS_INIT = False
config = configparser.ConfigParser()

def init_config():
    global IS_INIT
    if not IS_INIT:
        configpath = Path("config.ini")
        try:
            if not configpath.exists():
                raise RuntimeError('config file not found!')
            config.read(configpath)
            IS_INIT = True
        except RuntimeError as r_e:
            print("exception:", r_e)
            sys.exit()

def get_config(section, option, main_with_sub=False):
    init_config()
    if option.startswith('sub-url') and main_with_sub:
        return config.get(section, 'main-url') + config.get(section, option)
    return config.get(section, option)
