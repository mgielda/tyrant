#!/usr/bin/env python3

from tyrant import run, get_stdout, cd, watch, tyrant

def ls_parent():
    with cd('..'):
        run('ls')

def ls(d):
    run('ls %s' % d)
    watch('ls','.','*.py')

tyrant([ls_parent, ls],default=ls_parent)


