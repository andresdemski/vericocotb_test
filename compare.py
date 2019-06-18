from test_diff.vcd import *
from test_diff.log import *
import sys
import re

def main():
    test = sys.argv[1]
    try:
        veri_vcd = vcd_to_dic('./results/{}/verilator/dump.vcd'.format(test),
                              filter='COCOTB')
        icarus_vcd = vcd_to_dic('./results/{}/icarus/dump.vcd'.format(test))
        summary, diff = compare_vcd(veri_vcd, icarus_vcd)

        txt = ''
        for d in diff:
            txt += d['net'] + " verilator: {}  icarus: {}\n".format(*d['tv'])

        with open('./results/{}/readable_vcd.txt'.format(test), 'w') as f:
            f.write(summary)
        
        with open('./results/{}/vcd_diff.txt'.format(test), 'w') as f:
            f.write(txt)
    except:
        pass

    try:
        veri_log = get_log_events('./results/{}/verilator/console.log'.format(test))
        icarus_log = get_log_events('./results/{}/icarus/console.log'.format(test))

        fixed = lambda x: x if len(x) < 20 else x[0:19] + '...'
        
        events_str = '{:23} {:23}\n'.format('verilator', 'icarus')
        for v, i in zip(veri_log, icarus_log):
            events_str += '{:23} {:23}\n'.format(fixed(v['time'] + ' ' + v['msg']),
                                                 fixed(i['time'] + ' ' + i['msg']))
        with open('./results/{}/log_events.txt'.format(test), 'w') as f:
            f.write(events_str)

        veri_error, veri_sim, veri_real, veri_sim_real = get_results('./results/{}/verilator/console.log'.format(test))
        icarus_error, icarus_sim, icarus_real, icarus_sim_real = get_results('./results/{}/icarus/console.log'.format(test))

        log_results =  '{:>20} | {:30} | {:30}\n'.format('', 'verilator', 'icarus')
        log_results += '{:>20} | {:30} | {:30}\n'.format('ERRORS', veri_error, icarus_error)
        log_results += '{:>20} | {:30} | {:30}\n'.format('SIM TIME', veri_sim, icarus_sim)
        log_results += '{:>20} | {:30} | {:30}\n'.format('REAL TIME', veri_real, icarus_real)
        log_results += '{:>20} | {:30} | {:30}\n'.format('SIM / REAL TIME', veri_sim_real, icarus_sim_real)

        with open('./results/{}/log_results.txt'.format(test), 'w') as f:
            f.write(log_results)
        

        
    except:
        pass

    

if __name__ == '__main__':
    main()
