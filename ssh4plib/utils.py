import pexpect
from ssh4plib.host_storage import Host


def ssh_login(process: pexpect.spawn, host: Host):
    pattern_list = ["yes*", "password:*"]
    index = process.expect(pattern_list, timeout=-1, searchwindowsize=None)
    if index == 0:
        process.sendline("yes")
        process.expect(pattern_list[1])
    process.sendline(host.password)
