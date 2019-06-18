from test_diff.vcd import *
import sys

def main():
    veri_vcd = vcd_to_dic('./results/{}/verilator/dump.vcd'.format(sys.argv[1]),
                          filter_bypass=True)
    icarus_vcd = vcd_to_dic('./results/{}/icarus/dump.vcd'.format(sys.argv[1]))
    summary, diff = compare_vcd(veri_vcd, icarus_vcd)

    txt = ''
    for d in diff:
        txt += d['net'] + " verilator: {}  icarus: {}\n".format(*d['tv'])

    with open('./results/{}/readable_vcd.txt'.format(sys.argv[1]), 'w') as f:
        f.write(summary)
    
    with open('./results/{}/vcd_diff.txt'.format(sys.argv[1]), 'w') as f:
        f.write(txt)

if __name__ == '__main__':
    main()
