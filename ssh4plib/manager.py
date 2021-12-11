# encoding: UTF-8
import argparse
import os
import sys

from ssh4plib.host_storage import Host, HostStorage
from ssh4plib.common import host_map_path
from ssh4plib.version import VERSION


class Manager(object):

    @staticmethod
    def list(args: list):
        host_list = HostStorage.all().values()
        Manager.__print_header_line()
        for host in host_list:
            Manager.__print_line(host)

    @staticmethod
    def get(args: list):
        Manager.__print_header_line()
        host_map = HostStorage.all()
        for name in args:
            if name in host_map:
                Manager.__print_line(host_map.get(name))

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
        pass

    @staticmethod
    def version(args: list):
        print('v' + VERSION)

    @staticmethod
    def __print_header_line():
        Manager.__print_line(
            Host(name="NAME", host="HOST", port="PORT", user="USER", password="PASSWORD", proxy="PROXY"))

    @staticmethod
    def __print_line(host: Host):
        size = 20
        print(str(host.name).ljust(size) + str(host.host).ljust(size) + str(host.port).ljust(10) + str(host.user).ljust(
            10) + str(host.password).ljust(30) + str(host.proxy).ljust(size))
