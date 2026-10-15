#!/usr/bin/env python3
"""Apply the recovered code-E key to the transcribed telegrams and verify it.

Usage:  python3 check.py [transcription.txt] [key.tsv]
Standard library only (Python 3.8+).

What it does:
  1. ORDER CHECK. Code E is a one-part code: group numbers rise with the
     alphabetical order of the plaintext. Every reading for a group >= 30
     (outside the ʒ list) must sort between its neighbours. Any violation
     is printed; a correct key prints "0 violations".
  2. RENDER. Prints each telegram with code groups replaced by their
     readings in CAPITALS, clear text in lower case, unread groups as [N].
  3. COVERAGE. Counts coded text tokens (header groups excluded) and how
     many the key reads.
"""
import re, sys, unicodedata

tfile = sys.argv[1] if len(sys.argv) > 1 else 'transcription.txt'
kfile = sys.argv[2] if len(sys.argv) > 2 else 'key.tsv'

def fold(w):
    """Alphabetical sort key: strip accents, lower-case."""
    return ''.join(c for c in unicodedata.normalize('NFD', w)
                   if unicodedata.category(c) != 'Mn').lower()

key, tier = {}, {}
for line in open(kfile, encoding='utf-8'):
    if not line.strip() or line.startswith('#'):
        continue
    g, w, t = line.rstrip('\n').split('\t')
    key[g], tier[g] = w, t

# 1. order check over the main (non-ʒ) word list, groups >= 30
main = sorted((int(g), w) for g, w in key.items() if not g.endswith('z') and int(g) >= 30)
viol = [(a, wa, b, wb) for (a, wa), (b, wb) in zip(main, main[1:]) if fold(wa) > fold(wb)]
print(f'ORDER CHECK: {len(main)} groups in the main list, {len(viol)} violations')
for v in viol:
    print('  VIOLATION: %d=%s sorts after %d=%s' % v)

# 2-3. render + coverage
tels, cur = [], None
for line in open(tfile, encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('# ') or line == '#':
        continue   # comment lines start with "# "; code lines start with "#<digit>"
    if line.startswith('@'):
        h = re.search(r'hdr=(\S+)', line).group(1)
        cur = {'meta': line[1:], 'nhdr': 0 if h == '-' else len(h.split('-')), 'toks': []}
        tels.append(cur)
    else:
        cur['toks'] += line.split()

tot = rd = 0
unread = []
print()
for t in tels:
    out, seen = [], 0
    for tok in t['toks']:
        m = re.fullmatch(r'#(\d+)(z?)\??', tok)
        if not m:
            out.append(tok)
            continue
        g = m.group(1) + m.group(2)
        seen += 1
        if seen <= t['nhdr']:
            out.append(f'<hdr {g}>')
            continue
        tot += 1
        if g in key:
            rd += 1
            out.append(key[g].upper() + ('ʒ' if m.group(2) else ''))
        else:
            unread.append((t['meta'].split()[0], g))
            out.append(f'[{g}]')
    print('@' + t['meta'])
    print(' '.join(out))
    print()

print(f'COVERAGE: {rd} of {tot} coded text tokens read ({100*rd/tot:.1f}%); '
      f'{tot-rd} unread ({len(set(g for _, g in unread))} distinct groups)')
from collections import Counter
c = Counter(tier.values())
print('KEY: %d groups — %d confirmed, %d probable, %d tentative'
      % (len(key), c['confirmed'], c['probable'], c['tentative']))
