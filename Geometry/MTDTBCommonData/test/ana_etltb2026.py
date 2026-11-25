#!/usr/bin/env python3
"""FWLite analysis of the ETL TB2026 step2 output: beam centred on the module (4 LGADs per plane), any particle.
Usage (after cmsenv):  python3 ana_etltb2026.py ETLTB2026_step2_tb.root [--json events.json] [more files]
Per plane (1/2/3 along the beam): SimHits, digis, RecHits, clusters, earliest-RecHit time and its difference
from the earliest SimHit ToF, occupancy of the 4 sensors, events without hits (beam through the gaps).
With --json, the per-event records (beam vertex x, y and per-plane hit flags) are written for the plots.
"""
import json
import sys
from collections import Counter, defaultdict
from math import sqrt
import ROOT
from DataFormats.FWLite import Events, Handle

ROOT.gROOT.SetBatch(True)

ETLDIGI = ('edm::SortedCollection<FTLDataFrameT<io_v1::ETLDetId,io_v1::ETLSample,mtdhelpers::ETLRowColDecode>,'
           'edm::StrictWeakOrdering<FTLDataFrameT<io_v1::ETLDetId,io_v1::ETLSample,mtdhelpers::ETLRowColDecode> > >')
RECHIT = 'edm::SortedCollection<io_v1::FTLRecHit,edm::StrictWeakOrdering<io_v1::FTLRecHit> >'
CLUS = 'edmNew::DetSetVector<io_v1::FTLCluster>'
SIMLC = 'std::vector<io_v1::MtdSimLayerCluster>'
SIMHIT = 'std::vector<io_v1::PSimHit>'
SIMVTX = 'std::vector<io_v1::SimVertex>'

_ETLDetId = getattr(ROOT, 'ETLDetId', None) or ROOT.io_v1.ETLDetId


def plane(rawid):
    d = _ETLDetId(rawid)
    if d.zside() != 1:
        return -1
    return {(1, 0): 1, (1, 1): 2, (2, 0): 3}.get((d.nDisc(), d.discSide()), 0)


def stats(v):
    if not v:
        return float('nan'), float('nan')
    m = sum(v) / len(v)
    return m, sqrt(sum((x - m) ** 2 for x in v) / len(v))


def rms_core(v, k=3.):
    """mean/rms after iterative k-sigma clipping (tails from secondaries)"""
    v = list(v)
    for _ in range(10):
        m, s = stats(v)
        w = [x for x in v if abs(x - m) < k * s] if s > 0 else v
        if len(w) == len(v):
            break
        v = w
    return stats(v) + (len(v),)


def analyse(fname, jout=None):
    h = {k: Handle(t) for k, t in dict(sim=SIMHIT, digi=ETLDIGI, rh=RECHIT, cl=CLUS, lc=SIMLC, vtx=SIMVTX).items()}
    lab = dict(sim=('g4SimHits', 'FastTimerHitsEndcap'), digi=('mix', 'FTLEndcap'),
               rh=('mtdRecHits', 'FTLEndcap'), cl=('mtdClusters', 'FTLEndcap'),
               lc=('mix', 'MergedMtdTruthLC'), vtx=('g4SimHits', ''))
    nev = 0
    n = {k: Counter() for k in ('sim', 'digi', 'rh', 'cl')}     # per plane totals
    ev_with = {k: Counter() for k in ('sim', 'rh')}             # events with >= 1 hit per plane
    sens_occ = defaultdict(Counter)                             # plane -> rawId -> events with RecHit
    rh_t0, rh_res, rh_e, cl_size = defaultdict(list), defaultdict(list), [], []
    sim_tof0 = defaultdict(list)
    nrh_dist = defaultdict(Counter)
    rh_minus_z = n_lc = 0
    records = []
    for ev in Events(fname):
        nev += 1
        got = {k: ev.getByLabel(lab[k][0], lab[k][1], h[k]) for k in h}
        vx = vy = float('nan')
        if got['vtx'] and h['vtx'].product().size():
            p = h['vtx'].product()[0].position()
            vx, vy = 10 * p.x(), 10 * p.y()   # mm
        tsim = {}
        if got['sim']:
            for s in h['sim'].product():
                pl = plane(s.detUnitId())
                if pl <= 0:
                    continue
                n['sim'][pl] += 1
                tsim[pl] = min(tsim.get(pl, 1e9), s.tof())
        for pl, t in tsim.items():
            ev_with['sim'][pl] += 1
            sim_tof0[pl].append(t)
        if got['digi']:
            for d in h['digi'].product():
                pl = plane(d.id().rawId())
                if pl > 0:
                    n['digi'][pl] += 1
        trh, sens_ev, nrh_ev = {}, defaultdict(set), Counter()
        if got['rh']:
            for r in h['rh'].product():
                pl = plane(r.id().rawId())
                if pl < 0:
                    rh_minus_z += 1
                    continue
                n['rh'][pl] += 1
                nrh_ev[pl] += 1
                rh_e.append(r.energy())
                sens_ev[pl].add(r.id().rawId())
                if r.time() < trh.get(pl, (1e9,))[0]:
                    trh[pl] = (r.time(), r.id().rawId())
        for pl in (1, 2, 3):
            nrh_dist[pl][min(nrh_ev[pl], 5)] += 1
        for pl, (t, raw) in trh.items():
            ev_with['rh'][pl] += 1
            rh_t0[pl].append(t)
            if pl in tsim:
                rh_res[pl].append(t - tsim[pl])
            for sid in sens_ev[pl]:
                sens_occ[pl][sid] += 1
        if got['cl']:
            try:
                for ds in h['cl'].product():
                    pl = plane(ds.detId())
                    for c in ds:
                        if pl > 0:
                            n['cl'][pl] += 1
                            cl_size.append(c.size())
            except Exception:
                n['cl'][0] += h['cl'].product().dataSize()
        if got['lc']:
            n_lc += h['lc'].product().size()
        records.append(dict(x=round(vx, 3), y=round(vy, 3),
                            rh=[nrh_ev[pl] for pl in (1, 2, 3)],
                            sens=[trh[pl][1] if pl in trh else 0 for pl in (1, 2, 3)],
                            t=[round(trh[pl][0], 4) if pl in trh else None for pl in (1, 2, 3)],
                            tsim=[round(tsim[pl], 4) if pl in tsim else None for pl in (1, 2, 3)]))

    P = (1, 2, 3)
    out = dict(file=fname, nev=nev)
    print(f'\n===== {fname}  ({nev} events)')
    print('SimHits per event (planes 1/2/3):          ', ' / '.join(f"{n['sim'][p] / nev:.2f}" for p in P))
    print('Events with >=1 SimHit (planes 1/2/3, %):  ', ' / '.join(f"{100 * ev_with['sim'][p] / nev:.1f}" for p in P))
    print('Earliest SimHit ToF mean (ns, 1/2/3):      ', ' / '.join(f'{stats(sim_tof0[p])[0]:.4f}' for p in P))
    print('Digis per event (planes 1/2/3):            ', ' / '.join(f"{n['digi'][p] / nev:.2f}" for p in P))
    print('RecHits per event (planes 1/2/3):          ', ' / '.join(f"{n['rh'][p] / nev:.2f}" for p in P))
    print('Clusters per event (planes 1/2/3):         ', ' / '.join(f"{n['cl'][p] / nev:.2f}" for p in P),
          f"(unassigned {n['cl'][0] / nev:.2f})" if n['cl'][0] else '')
    print('Events with >=1 RecHit (planes 1/2/3, %):  ', ' / '.join(f"{100 * ev_with['rh'][p] / nev:.1f}" for p in P))
    for p in P:
        print(f'  plane {p}: RecHit multiplicity 0/1/2/3/4/>=5 (%):',
              ' / '.join(f'{100 * nrh_dist[p][k] / nev:.1f}' for k in range(6)))
    print('Earliest RecHit time mean (ns, 1/2/3):     ', ' / '.join(f'{stats(rh_t0[p])[0]:.3f}' for p in P))
    core = {p: rms_core(rh_res[p]) for p in P}
    print('RecHit - SimHit ToF core rms (ps, 1/2/3):  ', ' / '.join(f'{1000 * core[p][1]:.0f}' for p in P),
          '  (mean ps:', ' / '.join(f'{1000 * core[p][0]:.0f}' for p in P), ')')
    print(f'Mean RecHit energy: {stats(rh_e)[0]:.4f} MeV;  mean cluster size: {stats(cl_size)[0]:.2f};  '
          f'MtdSimLayerClusters per event: {n_lc / nev:.2f};  RecHits at -z: {rh_minus_z}')
    for p in P:
        print(f'  plane {p}: events with RecHit per sensor (rawId: N):',
              ', '.join(f'{k}: {v}' for k, v in sorted(sens_occ[p].items())))
    all3 = sum(1 for r in records if all(r['rh']))
    none = sum(1 for r in records if not any(r['rh']))
    print(f'Events with RecHits in all 3 planes: {100 * all3 / nev:.1f} %;  in no plane: {100 * none / nev:.1f} %')
    out.update(
        sim_per_ev=[n['sim'][p] / nev for p in P], digi_per_ev=[n['digi'][p] / nev for p in P],
        rh_per_ev=[n['rh'][p] / nev for p in P], cl_per_ev=[n['cl'][p] / nev for p in P],
        eff_sim=[ev_with['sim'][p] / nev for p in P], eff_rh=[ev_with['rh'][p] / nev for p in P],
        tof_sim=[stats(sim_tof0[p])[0] for p in P], t_rh=[stats(rh_t0[p])[0] for p in P],
        res_core_ps=[1000 * core[p][1] for p in P], res_mean_ps=[1000 * core[p][0] for p in P],
        res_core_n=[core[p][2] for p in P], res_n=[len(rh_res[p]) for p in P],
        mult=[[nrh_dist[p][k] / nev for k in range(6)] for p in P],
        e_mean=stats(rh_e)[0], cl_size=stats(cl_size)[0], lc_per_ev=n_lc / nev, rh_minus_z=rh_minus_z,
        sens_occ={p: dict(sens_occ[p]) for p in P}, all3=all3 / nev, none=none / nev,
        res=[rh_res[p] for p in P])
    if jout:
        json.dump(dict(summary=out, events=records), open(jout, 'w'))
    return out


if __name__ == '__main__':
    args = sys.argv[1:]
    jout = None
    if '--json' in args:
        i = args.index('--json')
        jout = args[i + 1]
        del args[i:i + 2]
    for k, f in enumerate(args):
        analyse(f, jout if k == 0 else None)
