#!/usr/bin/python

import webui

import argparse

# this example is actually taken from https://github.com/shimpe/argparseui/blob/master/argparseui/ui.py
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--make-argument-true", help="optional boolean argument", action="store_true")
parser.add_argument("-o","--make-other-argument-true", help="optional boolean argument 2", action="store_true", default=True)
parser.add_argument("-n","--number", help="an optional number", type=int)
parser.add_argument("-r","--restricted-number", help="one of a few possible numbers", type=int, choices=[1,2,3], default=2)
parser.add_argument("-c", "--counting-argument", help="counting #occurrences", action="count")
parser.add_argument("--default-value-argument", "-d", help="default value argument with a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long description", type=float, default="3.14")
parser.add_argument("-a", "--append-args", help="append arguments to list", type=str, action="append", default=["dish", "dash"])
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument('--foo', type=int, nargs='+')
parser.add_argument('--bar', type=int, nargs=2, metavar=('bar', 'baz'))

w = webui.Webui(parser)

w.dispatch()
