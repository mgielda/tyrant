#!/usr/bin/env python3

'''Example script using argh'''

import argh

# declaring:

def build(what='this'):
    return 'Building ' + what

def greet(name, greeting='Hello'):
    "Greets the user with given name. The greeting is customizable."
    return greeting + ', ' + name

# assembling:

p = argh.ArghParser()
p.add_commands([build,greet])
p.set_default_command(build)

# dispatching:

if __name__ == '__main__':
    p.dispatch()
