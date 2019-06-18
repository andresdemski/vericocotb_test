import re

def get_log_events(log):
    with open(log, 'r') as f:
        lines = f.read().split('\n')
    filter = lambda x: 'ERROR' in x or 'INFO' in x or 'WARN' in x
    log = [l for l in lines if filter(l) and '**' not in l]
    events = []
    for l in log:
        time = re.findall('^.*ns', l)[0].replace(' ','')
        msg = re.findall('ns.*', l)[0].replace('ns ','')
        parts = msg.split('     ')
        severity = parts[0]
        msg = ' '.join(parts[1:])
        events.append({'time':time, 'severity':severity, 'msg':msg})
    return events

def get_from_results(lines, pattern):
    l = [a for a in lines if pattern in a][0]
    return l.split(pattern)[1].split('  ')[0]

def get_results(log):
    with open(log, 'r') as f:
        lines = f.read().split('\n')
    lines = [l for l in lines if '**' in l]
    sim_time = get_from_results(lines, pattern='SIM TIME : ')
    real_time = get_from_results(lines, pattern='REAL TIME : ')
    sim_real_time = get_from_results(lines, pattern='SIM / REAL TIME : ')
    errors = get_from_results(lines, pattern='ERRORS : ')
    return errors, sim_time, real_time, sim_real_time

    
    
    
