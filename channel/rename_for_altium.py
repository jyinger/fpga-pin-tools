import re

out_lines = []

with open('channel_xc7a100t_fgg484/release/a7fgg484_v3.xdc') as f:
    for l in f:
        r_adc_dat = r'adc_dat_([pn])\[(\d)\]\[(\d{1,2})\]'
        m_adc_dat = re.search(r_adc_dat, l)

        r_adc_co = r'adc_([df])co_([pn])\[(\d)\]\[(\d)\]'
        m_adc_co = re.search(r_adc_co, l)

        r_idx = r'\[(\d)\]'
        m_idx = re.search(r_idx, l)

        make_diff = 'make_diff_pair_ports' in l

        if m_adc_dat:
            m = m_adc_dat
            new_net = 'adc_{}_dat_{}_{}'.format(m[2], m[3], m[1])
            #print(m.groups())
            #print(new_net)
            #print(l[:-1])
            #print(re.sub(r_adc_dat, new_net, l))
            if make_diff:
                #print(l[:-1])
                p_subed = re.sub(r_adc_dat, new_net, l, count=1)
                new_net = 'adc_{}_dat_{}_{}'.format(m[2], m[3], 'n')
                pn_subed = re.sub(r_adc_dat, new_net, p_subed, count=1)
                #print(pn_subed)
                out_lines.append(pn_subed)
            else:
                out_lines.append(re.sub(r_adc_dat, new_net, l))
        elif m_adc_co:
            m = m_adc_co
            new_net = 'adc_{}_{}co_{}_{}'.format(m[3], m[1], m[4], m[2])
            #print(m.groups())
            #print(new_net)
            #print(l[:-1])
            #print(re.sub(r_adc_co, new_net, l))
            if make_diff:
                #print(l[:-1])
                p_subed = re.sub(r_adc_co, new_net, l, count=1)
                new_net = 'adc_{}_{}co_{}_{}'.format(m[3], m[1], m[4], 'n')
                pn_subed = re.sub(r_adc_co, new_net, p_subed, count=1)
                #print(pn_subed)
                out_lines.append(pn_subed)
            else:
                out_lines.append(re.sub(r_adc_co, new_net, l))
        elif m_idx:
            m = m_idx
            new_idx = '_{}'.format(m[1])
            #print(m.groups())
            #print(new_idx)
            #print(l[:-1])
            #print(re.sub(r_idx, new_idx, l))
            out_lines.append(re.sub(r_idx, new_idx, l))
        else:
            #print(l[:-1])
            out_lines.append(l)

#for l in out_lines:
#    print(l[:-1])

with open('channel_xc7a100t_fgg484/release/a7fgg484_v4.xdc', 'w') as f:
    for l in out_lines:
        f.write(l)
