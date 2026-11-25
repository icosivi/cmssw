#!/usr/bin/env python3
"""Dump ToA, ToT, ADC of the ETL digis (ETLSample: 11-bit ToA/ToT, LSB = toaLSB_ns = 0.013 ns; 8-bit ADC)
plus the SimHit ToF and RecHit time/energy of the same sensor, for the ETL TB2026 step2 output.
Usage (after cmsenv): python3 ana_etltb2026_toa_tot.py ETLTB2026_step2_tb.root digis_toa_tot.json
"""
import json
import sys
import ROOT
from DataFormats.FWLite import Events, Handle

ROOT.gROOT.SetBatch(True)
LSB = 0.013
ETLDIGI = ('edm::SortedCollection<FTLDataFrameT<io_v1::ETLDetId,io_v1::ETLSample,mtdhelpers::ETLRowColDecode>,'
           'edm::StrictWeakOrdering<FTLDataFrameT<io_v1::ETLDetId,io_v1::ETLSample,mtdhelpers::ETLRowColDecode> > >')
RECHIT = 'edm::SortedCollection<io_v1::FTLRecHit,edm::StrictWeakOrdering<io_v1::FTLRecHit> >'
SIMHIT = 'std::vector<io_v1::PSimHit>'
_ETLDetId = getattr(ROOT, 'ETLDetId', None) or ROOT.io_v1.ETLDetId


def plane(rawid):
    d = _ETLDetId(rawid)
    if d.zside() != 1:
        return -1
    return {(1, 0): 1, (1, 1): 2, (2, 0): 3}.get((d.nDisc(), d.discSide()), 0)


hd, hr, hs = Handle(ETLDIGI), Handle(RECHIT), Handle(SIMHIT)
out = []
nev = 0
for iev, ev in enumerate(Events(sys.argv[1])):
    nev += 1
    ev.getByLabel('mix', 'FTLEndcap', hd)
    ev.getByLabel('mtdRecHits', 'FTLEndcap', hr)
    ev.getByLabel('g4SimHits', 'FastTimerHitsEndcap', hs)
    tsim, esim = {}, {}
    for s in hs.product():
        did = s.detUnitId()
        tsim[did] = min(tsim.get(did, 1e9), s.tof())
        esim[did] = esim.get(did, 0.) + 1e6 * s.energyLoss()   # keV (energyLoss in GeV), summed per sensor
    rh = {}
    for r in hr.product():
        rh.setdefault(r.id().rawId(), []).append((r.row(), r.column(), r.time(), r.energy()))
    for f in hd.product():
        raw = f.id().rawId()
        pl = plane(raw)
        for i in range(f.size()):
            smp = f.sample(i)
            if smp.toa() == 0 and smp.tot() == 0 and smp.data() == 0:
                continue
            m = [x for x in rh.get(raw, []) if x[0] == smp.row() and x[1] == smp.column()]
            out.append(dict(ev=iev, plane=pl, det=raw, i=i, row=smp.row(), col=smp.column(), thr=int(smp.threshold()),
                            adc=smp.data(), toa=smp.toa(), tot=smp.tot(),
                            toa_ns=round(smp.toa() * LSB, 4), tot_ns=round(smp.tot() * LSB, 4),
                            tsim=round(tsim[raw], 4) if raw in tsim else None,
                            esim_keV=round(esim[raw], 3) if raw in esim else None,
                            t_rh=round(m[0][2], 4) if m else None, e_rh=round(m[0][3], 5) if m else None))
json.dump(dict(nev=nev, lsb_ns=LSB, digis=out), open(sys.argv[2], 'w'))
print(f'{nev} events, {len(out)} digi samples')
for p in (1, 2, 3):
    d = [o for o in out if o['plane'] == p]
    if d:
        a = sorted(o['toa_ns'] for o in d)
        t = sorted(o['tot_ns'] for o in d)
        print(f"plane {p}: N={len(d)}  ToA median {a[len(a)//2]:.3f} ns [{a[0]:.3f}, {a[-1]:.3f}]  "
              f"ToT median {t[len(t)//2]:.3f} ns [{t[0]:.3f}, {t[-1]:.3f}]  sample index {sorted(set(o['i'] for o in d))}")
