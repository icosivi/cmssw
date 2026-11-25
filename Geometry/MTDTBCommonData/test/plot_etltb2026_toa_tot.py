#!/usr/bin/env python3
"""ToA / ToT distributions of the ETL digis, from the JSON written by ana_etltb2026_toa_tot.py.
Usage: python3 plot_etltb2026_toa_tot.py digis_toa_tot.json [toa_tot.png] [title]  (needs numpy + matplotlib)
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D = json.load(open(sys.argv[1]))
OUTPNG = sys.argv[2] if len(sys.argv) > 2 else 'toa_tot.png'
TITLE = sys.argv[3] if len(sys.argv) > 3 else 'ETL TB2026 digis'
G = [d for d in D['digis'] if d['plane'] > 0]
CAT = ['#2a78d6', '#eb6834', '#1baf7a']
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(2, 2, figsize=(13, 9))
a, b, c, d = ax.ravel()
for p in (1, 2, 3):
    s = [g for g in G if g['plane'] == p]
    toa = np.array([g['toa_ns'] for g in s]); tot = np.array([g['tot_ns'] for g in s])
    a.hist(toa, bins=np.arange(1.6, 4.4, 0.026), histtype='step', lw=2, color=CAT[p - 1],
           label=f'plane {p}: median {np.median(toa):.3f} ns (N = {len(s)})')
    b.hist(tot, bins=np.arange(0, 7.6, 0.104), histtype='step', lw=2, color=CAT[p - 1],
           label=f'plane {p}: median {np.median(tot):.2f} ns')
    w = [g for g in s if g['tsim'] is not None]
    dt = np.array([g['toa_ns'] - g['tsim'] for g in w]); tw = np.array([g['tot_ns'] for g in w])
    c.scatter(tw, 1000 * dt, s=4, color=CAT[p - 1], alpha=0.5, lw=0, label=f'plane {p}')
    e = [g for g in s if g['esim_keV'] is not None]
    d.scatter([g['esim_keV'] for g in e], [g['tot_ns'] for g in e], s=4, color=CAT[p - 1], alpha=0.5, lw=0,
              label=f'plane {p}')
# profile of the time walk (all planes)
w = [g for g in G if g['tsim'] is not None]
tw = np.array([g['tot_ns'] for g in w]); dt = 1000 * np.array([g['toa_ns'] - g['tsim'] for g in w])
edges = np.arange(0, 7.6, 0.5); xc, ym = [], []
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (tw >= lo) & (tw < hi)
    if m.sum() >= 20:
        xc.append(0.5 * (lo + hi)); ym.append(np.median(dt[m]))
c.plot(xc, ym, 'k-o', ms=4, lw=1.5, label='median (all planes)')
a.set_xlabel('ToA (ns)  [11 bit × 13 ps]'); a.set_ylabel('digis / 26 ps'); a.legend(frameon=False, fontsize=8.5)
a.set_title('(a) ToA: shifted per plane by the 200 mm flight (0.667 ns)', fontsize=10)
b.set_xlabel('ToT (ns)  [11 bit × 13 ps]'); b.set_ylabel('digis / 104 ps'); b.legend(frameon=False, fontsize=8.5)
b.set_title('(b) ToT: same for the 3 planes (Landau charge × pulse shape)', fontsize=10)
c.set_xlabel('ToT (ns)'); c.set_ylabel('ToA − SimHit ToF (ps)'); c.legend(frameon=False, fontsize=8.5, markerscale=3)
c.set_title('(c) time walk: small signals cross the threshold later', fontsize=10)
c.set_ylim(150, 900)
d.set_xlabel('energy deposited in the sensor, SimHit sum (keV)'); d.set_ylabel('ToT (ns)'); d.set_xscale('log')
d.legend(frameon=False, fontsize=8.5, markerscale=3, loc='lower right')
d.set_title('(d) ToT vs deposited energy: ~logarithmic (vertical bands = 1 keV rounding)', fontsize=10)
fig.suptitle(f'{TITLE} — {D["nev"]} events, {len(G)} digis', fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(OUTPNG, dpi=170)
print('written', OUTPNG)
