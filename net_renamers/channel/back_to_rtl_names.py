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
        r_adc_dat = r'adc_(\d)_dat_(\d{1,2})_([pn])'
        m_adc_dat = re.search(r_adc_dat, l)

        r_adc_co = r'adc_(\d)_([df])co_(\d)_([pn])'
        m_adc_co = re.search(r_adc_co, l)

        r_adc_csb = r'adc_(\d)_csb_(\d)'
        m_adc_csb = re.search(r_adc_csb, l)

        r_idx = r'_(\d)[\]\}]'
        m_idx = re.search(r_idx, l)

        make_diff = 'make_diff_pair_ports' in l

        if (m_adc_dat):
            m = m_adc_dat
            new_net = 'adc_dat_{}[{}][{}]'.format(m[3], m[1], m[2])
            #print(m.groups())
            #print(new_net)
            #print(l[:-1])
            #print(re.sub(r_adc_dat, new_net, l))
            if make_diff:
                #print(l[:-1])
                p_subed = re.sub(r_adc_dat, new_net, l, count=1)
                new_net = 'adc_dat_{}[{}][{}]'.format('n', m[1], m[2])
                pn_subed = re.sub(r_adc_dat, new_net, p_subed, count=1)
                #print(pn_subed)
                out_lines.append(pn_subed)
            else:
                out_lines.append(re.sub(r_adc_dat, new_net, l))
        elif (m_adc_co):
            m = m_adc_co
            new_net = 'adc_{}co_{}[{}][{}]'.format(m[2], m[4], m[1], m[3])
            #print(m.groups())
            #print(new_net)
            #print(l[:-1])
            #print(re.sub(r_adc_co, new_net, l))
            if make_diff:
                #print(l[:-1])
                p_subed = re.sub(r_adc_co, new_net, l, count=1)
                new_net = 'adc_{}co_{}[{}][{}]'.format(m[2], 'n', m[1], m[3])
                pn_subed = re.sub(r_adc_co, new_net, p_subed, count=1)
                #print(pn_subed)
                out_lines.append(pn_subed)
            else:
                out_lines.append(re.sub(r_adc_co, new_net, l))
        elif (m_adc_csb):
            m = m_adc_csb
            new_net = 'adc_csb[{}][{}]'.format(m[1], m[2])
            #print(m.groups())
            #print(new_net)
            #print(l[:-1])
            #print(re.sub(r_adc_csb, new_net, l))
            out_lines.append(re.sub(r_adc_csb, new_net, l))
        elif (m_idx):
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
