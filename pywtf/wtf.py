#!/usr/bin/env python
from subprocess import check_output
import re
from collections import Counter

RE_SPACE = re.compile(r'\s+')


def main():
    vars = RE_SPACE.split(open('/proc/loadavg').read())
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
    mem_total = RE_SPACE.split(rows[1])[1]
    mem_used = RE_SPACE.split(rows[2])[2]
    mem_avail = RE_SPACE.split(rows[2])[3]
    print('(MEM) total %s | used %s | avail %s' % (mem_total, mem_used, mem_avail))

    # TCP: inuse 2179 orphan 32 tw 31836 alloc 3404 mem 780
    row = open('/proc/net/sockstat').readlines()[1]
    vars = RE_SPACE.split(row.split('TCP: ')[1])
    reg = dict(vars[x:x+2] for x in range(0, len(vars) - 2, 2))
    print('(TCP) inuse %s | orphan %s | tw %s | alloc %s'
          % (reg.get('inuse'), reg.get('orphan'),
             reg.get('tw'), reg.get('alloc')))


if __name__ == '__main__':
    main()
