#!/usr/bin/env python

import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Input XDC file.')
parser.add_argument('-o', help='Output XDC file.')
args = parser.parse_args()

out_lines = []

with open(args.i) as f:
    for l in f:

        if "DIRECTION" in l:
            continue

        if 'make_diff_pair_ports' in l:
            continue

        r_idx_diff = r'_(\d)_([pn])\]'
        m_idx_diff = re.search(r_idx_diff, l)

        r_idx = r'_(\d)\]'
        m_idx = re.search(r_idx, l)

        if m_idx_diff:
            m = m_idx_diff
            new_idx = '_{}[{}]]'.format(m[2], m[1])
            #print(m.groups())
            #print(new_idx)
            #print(l[:-1])
            #print(re.sub(r_idx_diff, new_idx, l))
            out_lines.append(re.sub(r_idx_diff, new_idx, l))
        elif m_idx:
            m = m_idx
            new_idx = '[{}]]'.format(m[1])
            #print(m.groups())
            #print(new_idx)
            #print(l[:-1])
            #print(re.sub(r_idx, new_idx, l))
            out_lines.append(re.sub(r_idx, new_idx, l))
        else:
            #print(l[:-1])
            out_lines.append(l)

with open(args.o, 'w') as f:
    for l in out_lines:
        f.write(l)
