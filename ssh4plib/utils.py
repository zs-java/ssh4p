import pexpect
import os
import signal
from ssh4plib.host_storage import Host


def spawn(command) -> pexpect.spawn:
    process = pexpect.spawn(command)
    auto_terminal_size(process)
    signal.signal(signal.SIGWINCH, lambda sig, data: auto_terminal_size(process))
    return process


def auto_terminal_size(process: pexpect.spawn):
    size = os.get_terminal_size()
    process.setwinsize(size.lines, size.columns)


def ssh_login(process: pexpect.spawn, host: Host):
    pattern_list = ["yes*", "password:*"]
    index = process.expect(pattern_list, timeout=-1, searchwindowsize=None)
    if index == 0:
        process.sendline("yes")
        process.expect(pattern_list[1])
    process.sendline(host.password)
