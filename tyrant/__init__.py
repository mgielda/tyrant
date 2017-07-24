#!/usr/bin/env python3

import argh, contextlib, watchdog
import sarge

import os, sys, types
from os import getcwd
from os.path import exists

def run(command, **kwargs):
    if 'shell' not in kwargs:
        kwargs['shell'] = True
    sarge.run(command, **kwargs)

def get_stdout(command, **kwargs):
    if 'shell' not in kwargs:
        kwargs['shell'] = True
    sarge.get_stdout(command, **kwargs)

def source(script):
    import os
    from subprocess import check_output

    output = check_output(script + "; env -0", shell=True, executable="/bin/bash")
    #print(output.split('\0'))
    os.environ.update(line.partition('=')[::2] for line in output.decode('utf-8').split('\0'))


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
    curdir = getcwd()
    try:
        os.chdir(d)
        yield
    finally: os.chdir(curdir)

def main():
    try:
        sys.path.append(getcwd())
        import tasks
    except Exception as e:
        print(type(e).__name__, ":", e)
        print('No tasks.py file found or file corrupt.')
        sys.exit(1)

    builtin = [cd, exists, getcwd, run, get_stdout, source, watch]

    for fun in builtin:
        setattr(tasks, fun.__name__, fun)

    default_task = tasks.default_task if hasattr(tasks, 'default_task') else None
    tyrant([tasks.__dict__.get(a) for a in dir(tasks) if a not in [b.__name__ for b in builtin] and a != 'default_task' and isinstance(tasks.__dict__.get(a), types.FunctionType)], default_task)

if __name__ == '__main__':
    main()
