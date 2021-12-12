# encoding: UTF-8
import argparse
import os
import sys
import getpass

from ssh4plib.host_storage import Host, HostStorage
from ssh4plib.common import host_map_path
from ssh4plib.version import VERSION


class Manager(object):

    @staticmethod
    def list(args: list):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--password", action="store_true")
        opts = parser.parse_args(args)

        host_list = HostStorage.all().values()
        Manager.__print_header_line()
        for host in host_list:
            Manager.__print_line(host, password=opts.password)

    @staticmethod
    def get(args: list):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--password", action="store_true")
        opts, host_name_list = parser.parse_known_args(args)

        Manager.__print_header_line()
        host_map = HostStorage.all()
        for name in host_name_list:
            if name in host_map:
                Manager.__print_line(host_map.get(name), password=opts.password)

    @staticmethod
    def edit(args: list):
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "-app", "--application", action="store", default="vim", required=False)
        opts = parser.parse_args(args)
        shell = "/bin/bash  -c '%s %s'" % (opts.application, host_map_path)
        os.system(shell)

    @staticmethod
    def remove(args: list):
        parser = argparse.ArgumentParser()
        parser.add_argument("-y", "--yes", action="store_true", required=False)
        opts, host_name_list = parser.parse_known_args(args)
        tip_flag = not opts.yes
        if len(host_name_list) == 0:
            print("No host specified to delete!")
            sys.exit()
        host_map = HostStorage.all()
        removed_list = list()
        for name in host_name_list:
            if name not in host_map:
                print("No host name is " + name + "!")
                continue
            if tip_flag:
                print("Are you sure you want to delete %s host?(yes/no):" % name, end="")
                flag = input().lower()
                if flag not in ["y", "yes"]:
                    print("%s host will not be deleted" % name)
                    continue
            del host_map[name]
            removed_list.append(name)
        HostStorage.saveBatch(list(host_map.values()))
        if len(removed_list) > 0:
            print("remove hosts [%s] successfully!" % ", ".join(removed_list))
        else:
            print("No hosts deleted!")

    @staticmethod
    def save(args: list):
        if len(args) == 0:
            Manager.__save_by_input()
        else:
            Manager.__save_by_args(args)

    @staticmethod
    def version(args: list):
        print('v' + VERSION)

    @staticmethod
    def __print_header_line():
        Manager.__print_line(
            Host(name="NAME", host="HOST", port="PORT", user="USER", password="PASSWORD", proxy="PROXY"), password=True)

    @staticmethod
    def __save_by_args(args: list):
        parse = argparse.ArgumentParser(add_help=False)
        parse.add_argument("-n", "--name", action="store", required=True)
        parse.add_argument("-h", "--host", action="store", required=True)
        parse.add_argument("-P", "--port", action="store", default=22, required=False)
        parse.add_argument("-u", "--user", action="store", required=True)
        parse.add_argument("-p", "--password", action="store", required=False, default=None)
        parse.add_argument("--proxy", action="store", default=None, required=False)
        opts = parse.parse_args(args)
        host = Host(name=opts.name, host=opts.host, port=opts.port, user=opts.user, password=opts.password, proxy=opts.proxy)
        if host.password is None:
            host.password = Manager.__input_param("Host Password", password=True)

        HostStorage.save(host)
        print("save host[%s] successfully" % opts.name)

    @staticmethod
    def __save_by_input():
        host_dict = dict()
        host_dict["name"] = Manager.__input_param("name")
        host_dict["host"] = Manager.__input_param("host")
        host_dict["port"] = int(Manager.__input_param("port", require=False, default=22))
        host_dict["user"] = Manager.__input_param("user")
        host_dict["password"] = Manager.__input_param("password", password=True)
        host_dict["proxy"] = Manager.__input_param("proxy", require=False)
        HostStorage.save(Host(**host_dict))
        print("save host[%s] successfully" % host_dict["name"])

    @staticmethod
    def __input_param(name, **kwargs):
        if kwargs.get("password", False):
            value = getpass.getpass("%s:" % name).strip()
        else:
            value = input("%s:" % name).strip()
        if kwargs.get("require", True) and (value is None or value == ""):
            print("%s is required!" % name)
            value = Manager.__input_param(name, kwargs=kwargs)

        return value if value is not None and value != "" else kwargs.get("default", None)

    @staticmethod
    def __print_line(host: Host, **kwargs):
        size = 20
        line = str(host.name).ljust(size) + \
               str(host.host).ljust(size) + \
               str(host.port).ljust(10) + \
               str(host.user).ljust(10) + \
               str(host.password if kwargs.get("password", False) else "*" * len(host.password)).ljust(30) + \
               str(host.proxy).ljust(size)
        print(line)
