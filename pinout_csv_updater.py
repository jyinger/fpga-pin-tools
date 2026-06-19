#!/usr/bin/env python

import argparse
import csv
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('-vivado', help='Vivado pin CSV to update.')
parser.add_argument('-altium', help='Altium pin CSV, source of update info.')
parser.add_argument('-o', help='Output Vivado CSV file.')
args = parser.parse_args()

def site_is_io(site):
    return site.startswith("IO_")


pin_net_map = {}


with open(args.altium) as f_in:
    csv_in = csv.reader(f_in)

    # Throw away the header
    list(itertools.islice(csv_in, 3))

    for r in csv_in:
        pin_num = r[0]
        net = r[1]
        site = r[2]
        if site_is_io(site) and len(net) > 0:
            pin_net_map[pin_num] = net


#for k, v in pin_net_map.items():
#    print((k, v))


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
fc_diffpair = 'DiffPair Signal'
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


csv_in_rows = []
with open(args.vivado) as f_in:
    csv_in = csv.reader(f_in)

    # Find the header
    header_found = False
    while not header_found:
        header = csv_in.__next__()
        if len(header) > 0 and header[0] == 'IO Bank':
            header_found = True

    header_asoc = {}
    for i in range(len(header)):
        header_asoc[header[i]] = i

    # Capture pinout rows
    for r in csv_in:
        csv_in_rows.append(r)


def io_details(row):
    return row[header_asoc[fc_net]:]


net_std_map = {}
for r in csv_in_rows:
    net = r[header_asoc[fc_net]]
    if net != '':
        net_std_map[net] = io_details(r)
    else:
        if site_is_io(r[header_asoc[fc_site]]):
            print(r)
            print(io_details(r))
            print('')

#for k, v in net_std_map.items():
#    print((k, v))


def other_pair_member(net):
    if '_n' in net:
        return net.replace('_n', '_p')
    else:
        return net.replace('_p', '_n')


# TODO UESE ME: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

with open(args.o, 'w') as f_out:
    csv_out = csv.writer(f_out)

    # New header:
    csv_out.writerow(['# Updated by pinout_csv_updater.py'])
    csv_out.writerow(['#    Input Vivado Pinout: {}'.format(args.vivado)])
    csv_out.writerow(['#    Altium Pinout with Updates: {}'.format(args.altium)])
    csv_out.writerow(['#    Output Vivado Pinout: {}'.format(args.o)])
    csv_out.writerow(header)

    for r in csv_in_rows:

        pin = r[header_asoc[fc_pin]]


        net = r[header_asoc[fc_net]]
        if pin in pin_net_map:
            new_net = pin_net_map[pin]
            if net != new_net:
                print("Change: Swap or Add")
        else:
            new_net = ''
            if net != new_net:
                print("Change: Remove")

        if net != new_net:
            print(r)
            r[header_asoc[fc_net]] = new_net
            r[header_asoc[fc_diffpair]] = other_pair_member(new_net)
            print(r)
            print('')

        csv_out.writerow(r)
