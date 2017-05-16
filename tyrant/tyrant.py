#!/usr/bin/env python3

import argh, contextlib, watchdog
from sarge import run, get_stdout

def watch(command, directories='.', patterns='*', ignore_patterns='', ignore_directories=False, wait_for_process=False, drop_during_process=False, timeout=5, recursive=True):
    """
    Subcommand to execute shell commands in response to file system events.
    :param args:
        Command line argument options.
    """
    from watchdog.watchmedo import parse_patterns, observe_with
    from watchdog.tricks import ShellCommandTrick
    from watchdog.observers import Observer

    patterns, ignore_patterns = parse_patterns(patterns, ignore_patterns)
    handler = ShellCommandTrick(shell_command=command,
                                patterns=patterns,
                                ignore_patterns=ignore_patterns,
                                ignore_directories=ignore_directories,
                                wait_for_process=wait_for_process,
                                drop_during_process=drop_during_process)
    observer = Observer(timeout=timeout)
    observe_with(observer, handler, directories, recursive)

def tyrant(commands, default=None):
    p = argh.ArghParser()
    p.add_commands(commands)
    if default is not None:
        try:
            p.set_default_command(default)
        except argh.AssemblingError:
            print('To use default commands, please upgrade to Python 3.4 or higher')
            p.add_commands([default])
    p.dispatch()

@contextlib.contextmanager
def cd(d):
    import os
    curdir= os.getcwd()
    try:
        os.chdir(d)
        yield
    finally: os.chdir(curdir)
