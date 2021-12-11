# encoding: UTF-8
import json
import ssh4plib


class Host:

    def __init__(self, **opts):
        self.name = opts.get('name', None)
        self.host = opts.get('host', None)
        self.port = opts.get('port', None)
        self.user = opts.get('user', None)
        self.password = opts.get('password', None)
        self.proxy = opts.get('proxy', None)

    # def __init__(self, dict_data: dict):
    #     self.name = dict_data.get('name', None)
    #     self.host = dict_data.get('host', None)
    #     self.port = dict_data.get('port', None)
    #     self.user = dict_data.get('user', None)
    #     self.password = dict_data.get('password', None)
    #     self.proxy = dict_data.get('proxy', None)

    @staticmethod
    def parse_dict(dict_data: dict):
        pass

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return str(self.to_dict())


class HostStorage(object):

    @staticmethod
    def all() -> dict:
        with open(ssh4plib.common.host_map_path) as file:
            host_map_json = json.load(file)

        host_map = dict()
        for key in host_map_json:
            host = Host(**host_map_json[key])
            host.name = key
            host_map[key] = host
        return host_map

    @staticmethod
    def get(name: str) -> Host:
        return HostStorage.all().get(name, None)

    @staticmethod
    def saveBatch(host_list: list):
        host_map_dict = dict(list(map(lambda v: (v.name, HostStorage.__host_to_dict(v)), host_list)))
        host_map_json = json.dumps(host_map_dict, indent=2)
        with open(ssh4plib.common.host_map_path, 'w') as file:
            file.write(host_map_json)

    @staticmethod
    def __host_to_dict(host: Host):
        host_dict = host.to_dict()
        del host_dict["name"]
        return host_dict
