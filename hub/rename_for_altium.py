import re

out_lines = []

with open('release/au27p_ffvb676_v3.xdc') as f:
    for l in f:
        r_diff_idx = r'_([pn])\[(\d)\]'
        m_diff_idx = re.search(r_diff_idx, l)

        r_idx = r'\[(\d)\]'
        m_idx = re.search(r_idx, l)

        make_diff = 'make_diff_pair_ports' in l

        if m_diff_idx:
            m = m_diff_idx
            new_suffix = "_{}_{}".format(m[2], m[1])
            #print(m.groups())
            #print(new_suffix)
            #print(l[:-1])
            #print(re.sub(r_diff_idx, new_suffix, l))
            #print("")
            if make_diff:
                #print(l[:-1])
                p_subed = re.sub(r_diff_idx, new_suffix, l, count=1)
                new_suffix = "_{}_{}".format(m[2], 'n')
                pn_subed = re.sub(r_diff_idx, new_suffix, p_subed, count=1)
                #print(pn_subed)
                out_lines.append(pn_subed)
            else:
                out_lines.append(re.sub(r_diff_idx, new_suffix, l))

        elif m_idx:
            m = m_idx
            new_suffix = "_{}".format(m[1])
            #print(m.groups())
            #print(new_suffix)
            #print(l[:-1])
            #print(re.sub(r_idx, new_suffix, l))
            #print("")
            if make_diff:
                #print(l[:-1])
                p_subed = re.sub(r_idx, new_suffix, l, count=1)
                new_suffix = "_{}".format('n')
                pn_subed = re.sub(r_idx, new_suffix, p_subed, count=1)
                #print(pn_subed)
                out_lines.append(pn_subed)
            else:
                out_lines.append(re.sub(r_idx, new_suffix, l))
        else:
            #print(l[:-1])
            out_lines.append(l)

with open('release/au27p_ffvb676_v4.xdc', 'w') as f:
    for l in out_lines:
        f.write(l)
