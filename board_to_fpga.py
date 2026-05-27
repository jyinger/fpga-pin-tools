#!/usr/bin/env python

import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-dbg', help='Enable debug mode.', action=argparse.BooleanOptionalAction)
parser.add_argument('-board', help='Which board are we targeting?', choices=['channel', 'hub'], required=True)
parser.add_argument('-altium', help='Altium pin report CSV.', required=True)
parser.add_argument('-out-xdc', help='Output XDC file.', required=True)
args = parser.parse_args()


