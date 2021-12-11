# encoding: utf-8
import os

from ssh4plib.host_storage import HostStorage

config_dir = '.ssh4p'
config_home = os.path.join(os.path.expanduser('~'), config_dir)
host_map_file = 'host_map.json'
host_map_path = os.path.join(config_home, host_map_file)


def check_config():
    global config_home, host_map_path
    if not os.path.exists(config_home):
        os.mkdir(config_home)
    if not os.path.exists(host_map_path):
        HostStorage.saveBatch([])
