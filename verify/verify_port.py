#!/usr/bin/env python3
"""Out-of-band verifier for a demoniC port: run the upstream reference and the
.dmc on the same fixed inputs, then compare their stdout.

The .dmc and the reference are not required to format output identically — the
demoniC `print` emits one token per line, the reference prints idiomatic Python
lists / C grids. We compare the *meaning*, not the bytes:

  --mode floats   extract every numeric literal in order, compare within tol
  --mode glyphs   extract the drawn ASCII glyphs (@ O o .) in order, compare exact

Exit 0 = match, 1 = mismatch, 2 = a command failed to run.
"""
import argparse, re, subprocess, sys

NUM = re.compile(r'[-+]?(?:\d+\.\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?|\d+(?:[eE][-+]?\d+)?)')
GLYPH = re.compile(r'[@Oo.]')

def run(cmd, label):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except Exception as e:
        print(f"  [{label}] failed to run: {e}", file=sys.stderr); sys.exit(2)
    if p.returncode != 0:
        print(f"  [{label}] exit {p.returncode}\n{p.stderr[:500]}", file=sys.stderr); sys.exit(2)
    return p.stdout

def floats(s):  return [float(x) for x in NUM.findall(s)]
def glyphs(s):  return GLYPH.findall(s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', nargs='+', required=True, help='reference command (e.g. python3 foo.py)')
    ap.add_argument('--dmc', nargs='+', required=True, help='dmc command (e.g. dmc run foo.dmc)')
    ap.add_argument('--mode', choices=['floats', 'glyphs'], required=True)
    ap.add_argument('--rtol', type=float, default=1e-5)
    ap.add_argument('--atol', type=float, default=1e-6)
    a = ap.parse_args()

    ref_out, dmc_out = run(a.ref, 'ref'), run(a.dmc, 'dmc')

    if a.mode == 'glyphs':
        r, d = glyphs(ref_out), glyphs(dmc_out)
        if r == d:
            print(f"  OK — {len(r)} glyphs match"); return 0
        print(f"  MISMATCH — ref {len(r)} glyphs vs dmc {len(d)} glyphs", file=sys.stderr)
        return 1

    r, d = floats(ref_out), floats(dmc_out)
    if len(r) != len(d):
        print(f"  MISMATCH — ref has {len(r)} numbers, dmc has {len(d)}", file=sys.stderr)
        return 1
    bad = []
    for i, (x, y) in enumerate(zip(r, d)):
        if abs(x - y) > max(a.atol, a.rtol * abs(x)):
            bad.append((i, x, y))
    if bad:
        print(f"  MISMATCH — {len(bad)}/{len(r)} numbers differ beyond tol:", file=sys.stderr)
        for i, x, y in bad[:8]:
            print(f"    [{i}] ref={x!r} dmc={y!r}", file=sys.stderr)
        return 1
    print(f"  OK — {len(r)} numbers match within rtol={a.rtol} atol={a.atol}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
