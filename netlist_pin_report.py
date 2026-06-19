#!/usr/bin/env python

import argparse
import csv
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('-vivado', help='Vivado pin CSV.')
parser.add_argument('-from_edf', help='Pin CSV from bunnie-netlist-checker from EDF.')
parser.add_argument('-o', help='Output CSV file.')
args = parser.parse_args()

#import pdb#; pdb.set_trace()
#import sys
#def excepthook(type, value, traceback):
#    pdb.set_trace()
#sys.excepthook = excepthook

report = {}

# Report Dict Keys
k_brd_net = "brd_net"
k_fpga_net = "fpga_net"
k_fpga_site = "fpga_site"

# FPGA CSV Column Names
#'IO Bank'
fc_pin = 'Pin Number'
#'Site'
fc_site = 'Site Type'
#'Min Trace Delay (ps)'
#'Max Trace Delay (ps)'
#'Prohibit'
#'Interface'
fc_net = 'Signal Name'
#'Direction'
#'DiffPair Type'
#'DiffPair Signal'
#'IO Standard'
#'Drive (mA)'
#'Slew Rate'
#'OUTPUT_IMPEDANCE'
#'PRE_EMPHASIS'
#'LVDS_PRE_EMPHASIS'
#'OFFSET_CONTROL'
#'EQUALIZATION'
#'Pull Type'
#'DQS_BIAS'
#'IN_TERM'
#'DIFF_TERM'
#'OFFCHIP_TERM'
#'Board Signal'
#'Board Voltage'

with open(args.vivado) as f:
    cr = csv.reader(f)

    # Find the header
    header_found = False
    while not header_found:
        header = cr.__next__()
        if len(header) > 0 and header[0] == 'IO Bank':
            header_found = True

    header_asoc = {}
    for i in range(len(header)):
        header_asoc[header[i]] = i

    for r in cr:
        #print(r)
        pin = r[header_asoc[fc_pin]]
        report[pin] = {}
        report[pin][k_fpga_net] = r[header_asoc[fc_net]]
        report[pin][k_fpga_site] = r[header_asoc[fc_site]]


with open(args.from_edf) as f:
    cr = csv.reader(f)
    for r in cr:
        net, pin = r
        report[pin][k_brd_net] = net


#print(report)

#for kv in report.items():
#    print("{} has {}".format(*kv))

# Report pins with no board net
#for k, v in report.items():
#    if (k_brd_net not in v):
#        print("{} has {}".format(k, v))

# FIX UP PINS WITH NO SCH NET!!!
for k, v in report.items():
    if (k_brd_net not in v):
        v[k_brd_net] = "NC"
        report[k] = v

with open(args.o, 'w') as f:
    cw = csv.writer(f)

    c_hdr = [k_brd_net, k_fpga_net, k_fpga_site]
    cw.writerow(['pin'] + c_hdr)

    for k, v in report.items():
        cw.writerow([k] + [v[c] for c in c_hdr])
