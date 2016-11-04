#!/usr/bin/env python
from subprocess import check_output
from collections import Counter
from argparse import ArgumentParser

SOCKET_STATE = {
    '01':'ESTABLISHED',
    '02':'SYN_SENT',
    '03':'SYN_RECV',
    '04':'FIN_WAIT1',
    '05':'FIN_WAIT2',
    '06':'TIME_WAIT',
    '07':'CLOSE',
    '08':'CLOSE_WAIT',
    '09':'LAST_ACK',
    '0A':'LISTEN',
    '0B':'CLOSING'
}


def decode_ip(val):
    items = [val[6:8], val[4:6], val[2:4], val[0:2]]
    items = [str(int(x, 16)) for x in items]
    return '.'.join(items)


def split_by_spaces(val):
    return list(filter(None, val.split(' ')))


def main():
    parser = ArgumentParser()
    parser.add_argument('--net', action='store_true', default=False)
    opts = parser.parse_args()

    vars = split_by_spaces(open('/proc/loadavg').read())
    host = open('/etc/hostname').read().strip()
    print('(HOST) %s' % host)

    rows = check_output(['ps', 'axo', 'comm']).decode('utf-8').splitlines()
    reg = Counter()
    for proc in rows:
        reg[proc] += 1
    top = ['%s %d' % x for x in reg.most_common(5)]
    print('(PROC) %s | %s' % (
        vars[3].split('/')[1],
        ' | '.join(top)
    ))
    print('(LOAD) %s | %s | %s' % (vars[0], vars[1], vars[2]))

    rows = check_output(['/usr/bin/free', '-h']
                        ).decode('utf-8').splitlines()
    mem_total = split_by_spaces(rows[1])[1]
    mem_used = split_by_spaces(rows[2])[2]
    mem_avail = split_by_spaces(rows[2])[3]
    print('(MEM) total %s | used %s | avail %s' % (mem_total, mem_used, mem_avail))

    # TCP: inuse 2179 orphan 32 tw 31836 alloc 3404 mem 780
    row = open('/proc/net/sockstat').readlines()[1]
    vars = split_by_spaces(row.split('TCP: ')[1])
    reg = dict(vars[x:x+2] for x in range(0, len(vars) - 2, 2))
    print('(TCP) inuse %s | orphan %s | tw %s | alloc %s'
          % (reg.get('inuse'), reg.get('orphan'),
             reg.get('tw'), reg.get('alloc')))

    if opts.net:
        local_ports = Counter()
        ext_ips = Counter()
        states = Counter()
        # http://www.linuxdevcenter.com/pub/a/linux/2000/11/16/LinuxAdmin.html
        for count, row in enumerate(open('/proc/net/tcp')):
            if count:
                items = split_by_spaces(row.rstrip())
                port = int(items[1].split(':')[1], 16)
                local_ports[port] += 1

                ip = decode_ip(items[2].split(':')[0])
                ext_ips[ip] += 1

                states[items[3]] += 1
        lports = ['%d (%d)' % x for x in local_ports.most_common(5)]
        xips = ['%s (%d)' % x for x in ext_ips.most_common(5)]
        states = ['%s %d' % (SOCKET_STATE[x[0]], x[1])
                  for x in states.most_common()]
        print('(L.PORT) %s' % ' | '.join(lports))
        print('(EX.IP) %s' % ' | '.join(xips))
        print('(TCP.STATE) %s' % ' | '.join(states))



if __name__ == '__main__':
    main()
