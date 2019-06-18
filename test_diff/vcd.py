from Verilog_VCD.Verilog_VCD import parse_vcd
import re

def vcd_to_dic(vcd_file, filter_bypass=False):
    vcd = parse_vcd(vcd_file)
    signals = {}
    for k in vcd.keys():
        net = vcd[k]['nets'][0]
        signal = net['hier'] + '.' + net['name']
        if filter_bypass:
            signal = re.sub('^BYPASSTOP_.*?\.', '', signal)
        signals[signal] = {}
        signals[signal]['size'] = net['size']
        signals[signal]['tv'] = to_fixed_size(vcd[k]['tv'], int(net['size'], 10))
    return signals

def to_fixed_size(tv, size):
    ret = []
    for t in tv:
        time = t[0]
        value = t[1]
        if ('z' in value or 'x' in value) and len(value) == 1:
            value = value * size
        else:
            value = '0' * (size - len(value)) + value
        ret.append((time, value))
    return ret
        

def dic_to_yml(dic):
    yml = ""
    for k in sorted(dic.keys()):
        yml +=  k + ':\n'
        yml += '    size:{}\n'.format(dic[k]['size'])
        yml += '    tv:\n'
        for t in dic[k]['tv']:
            yml += '        {}:{}\n'.format(*t)
    return yml

def compare_vcd(vcd1, vcd2):
    keys = list(vcd1.keys())
    keys += [l for l in list(vcd2.keys()) if l not in keys]
    summary = ''
    diff = []

    for k in keys:
        summary += '-'*86 + '\n'
        summary += '| {:^83} |'.format(k) + '\n'
        summary += '-'*86 + '\n'
        if k in vcd1 and k in vcd2:
            for tv1, tv2 in zip(vcd1[k]['tv'], vcd2[k]['tv']):
                value1 = '{}:{}'.format(*tv1)
                value2 = '{}:{}'.format(*tv2)
                summary += '| {:40} | {:40} |'. format(value1, value2) + '\n'
                if value1 != value2:
                    diff.append({'net': k,
                                 'size':(vcd1[k]['size'], vcd2[k]['size']),
                                 'tv':(value1, value2)})
        elif k in vcd1:
            for tv1 in vcd1[k]['tv']:
                value1 = '{}:{}'.format(*tv1)
                summary += '| {:40} | {:40} |'. format(value1, '') + '\n'
                diff.append({'net': k, 'tv':(value1, None)})
        elif k in vcd2:
            for tv2 in vcd2[k]['tv']:
                value2 = '{}:{}'.format(*tv2)
                summary += '| {:40} | {:40} |'. format('', value2) + '\n'
                diff.append({'net': k, 'tv':(None, value2)})
        summary += '-'*86 + '\n'
        summary += '\n' + '\n'
    return summary, diff
    

