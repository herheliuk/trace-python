#!/usr/bin/env python3

from sys import exit as sys_exit
from os import (
    fork as os_fork,
    kill as os_kill,
    getpid as os_getpid,
    waitpid as os_waitpid
)
from signal import (
    SIGSTOP as signal_SIGSTOP,
    SIGCONT as signal_SIGCONT,
    SIGKILL as signal_SIGKILL
)

cool_array = []

def fork_add():
    child_pid = os_fork()
    if child_pid == 0:
        os_kill(os_getpid(), signal_SIGSTOP)
        print("CHILD RUNNING", flush=True)
    else:
        cool_array.append(child_pid)

def _discard_after(pid):
    kill_after = cool_array.index(pid)
    for pid_to_kill in cool_array[kill_after + 1:]:
        os_kill(pid_to_kill, signal_SIGKILL)
        os_waitpid(pid_to_kill, 0)

def resume_pid(pid):
    _discard_after(pid)
    os_kill(pid, signal_SIGCONT)
    os_waitpid(pid, 0)
    print("CHILD EXITED", flush=True)
    sys_exit()
