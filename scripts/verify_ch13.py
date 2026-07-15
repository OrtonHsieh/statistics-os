#!/usr/bin/env python3
"""Recompute the Chapter 13 ANOVA problem answers from the source data."""

from __future__ import annotations

import math


def _betacf(a: float, b: float, x: float) -> float:
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    tiny = 3e-14
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 301):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-14:
            return h
    raise RuntimeError("incomplete beta did not converge")


def ibeta(a: float, b: float, x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log1p(-x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def f_sf(value: float, dfn: int, dfd: int) -> float:
    x = dfd / (dfd + dfn * value)
    return ibeta(dfd / 2.0, dfn / 2.0, x)


def f_critical(alpha: float, dfn: int, dfd: int) -> float:
    lo, hi = 0.0, 1.0
    while f_sf(hi, dfn, dfd) > alpha:
        hi *= 2
    for _ in range(120):
        mid = (lo + hi) / 2
        if f_sf(mid, dfn, dfd) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def t_cdf(t: float, df: int) -> float:
    if t == 0:
        return 0.5
    x = df / (df + t * t)
    tail = 0.5 * ibeta(df / 2.0, 0.5, x)
    return 1.0 - tail if t > 0 else tail


def t_critical(alpha_two_sided: float, df: int) -> float:
    target = 1.0 - alpha_two_sided / 2.0
    lo, hi = 0.0, 20.0
    for _ in range(120):
        mid = (lo + hi) / 2
        if t_cdf(mid, df) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def one_way(groups: list[list[float]] | None = None, summaries=None):
    if summaries is None:
        summaries = [(len(g), sum(g) / len(g), sum((x - sum(g) / len(g)) ** 2 for x in g) / (len(g) - 1)) for g in groups]
    ns = [x[0] for x in summaries]
    means = [x[1] for x in summaries]
    variances = [x[2] for x in summaries]
    n, k = sum(ns), len(ns)
    grand = sum(ni * mi for ni, mi in zip(ns, means)) / n
    ssb = sum(ni * (mi - grand) ** 2 for ni, mi in zip(ns, means))
    sse = sum((ni - 1) * vi for ni, vi in zip(ns, variances))
    dfb, dfe = k - 1, n - k
    msb, mse = ssb / dfb, sse / dfe
    f = msb / mse
    return dict(n=n, k=k, means=means, grand=grand, ssb=ssb, sse=sse, sst=ssb+sse,
                dfb=dfb, dfe=dfe, dft=n-1, msb=msb, mse=mse, f=f,
                p=f_sf(f, dfb, dfe), fc05=f_critical(.05, dfb, dfe), fc01=f_critical(.01, dfb, dfe))


def randomized_block(rows: list[list[float]]):
    a, b = len(rows), len(rows[0])
    flat = [x for row in rows for x in row]
    grand = sum(flat) / len(flat)
    rowmeans = [sum(row) / b for row in rows]
    colmeans = [sum(rows[i][j] for i in range(a)) / a for j in range(b)]
    sst = sum((x-grand)**2 for x in flat)
    ssa = b * sum((x-grand)**2 for x in rowmeans)
    ssblocks = a * sum((x-grand)**2 for x in colmeans)
    sse = sst - ssa - ssblocks
    dfa, dfblocks, dfe = a-1, b-1, (a-1)*(b-1)
    msa, msblocks, mse = ssa/dfa, ssblocks/dfblocks, sse/dfe
    return dict(grand=grand,rowmeans=rowmeans,colmeans=colmeans,sst=sst,ssa=ssa,ssblocks=ssblocks,sse=sse,
                dfa=dfa,dfblocks=dfblocks,dfe=dfe,msa=msa,msblocks=msblocks,mse=mse,
                fa=msa/mse,pa=f_sf(msa/mse,dfa,dfe),fb=msblocks/mse,pb=f_sf(msblocks/mse,dfblocks,dfe),
                fca=f_critical(.05,dfa,dfe))


def factorial_2way(cells: list[list[list[float]]]):
    a, b, r = len(cells), len(cells[0]), len(cells[0][0])
    flat = [x for row in cells for cell in row for x in cell]
    grand = sum(flat)/len(flat)
    am = [sum(x for cell in cells[i] for x in cell)/(b*r) for i in range(a)]
    bm = [sum(x for i in range(a) for x in cells[i][j])/(a*r) for j in range(b)]
    cm = [[sum(cells[i][j])/r for j in range(b)] for i in range(a)]
    ssa = b*r*sum((x-grand)**2 for x in am)
    ssb = a*r*sum((x-grand)**2 for x in bm)
    ssab = r*sum((cm[i][j]-am[i]-bm[j]+grand)**2 for i in range(a) for j in range(b))
    sse = sum((x-cm[i][j])**2 for i in range(a) for j in range(b) for x in cells[i][j])
    dfa,dfb,dfab,dfe=a-1,b-1,(a-1)*(b-1),a*b*(r-1)
    mse=sse/dfe
    return dict(grand=grand,am=am,bm=bm,cm=cm,ssa=ssa,ssb=ssb,ssab=ssab,sse=sse,sst=ssa+ssb+ssab+sse,
                dfa=dfa,dfb=dfb,dfab=dfab,dfe=dfe,mse=mse,fa=(ssa/dfa)/mse,fb=(ssb/dfb)/mse,fab=(ssab/dfab)/mse,
                pa=f_sf((ssa/dfa)/mse,dfa,dfe),pb=f_sf((ssb/dfb)/mse,dfb,dfe),pab=f_sf((ssab/dfab)/mse,dfab,dfe),
                fc=f_critical(.05,1,dfe))


PROBLEMS = {
    1: (None, [(12,24,18),(9,25,7),(12,26,10)]),
    2: (None, [(12,26,10),(10,31,7),(9,22,15),(14,25,9)]),
    3: ([[80,75,76,89,80],[85,86,81,80],[79,85,88]], None),
    4: ([[84,64,93,88,71],[95,60,89,96,90],[85,93,90,92,80]], None),
    6: ([[37,33,36,38],[43,39,35,38,40],[28,32,33]], None),
    8: ([[45,41,37,40,42],[31,34,35,40],[39,35,40]], None),
    9: (None, [(8,62,36),(8,52,25),(8,60,49)]),
    10: ([[31,28,34,32,26,29],[37,32,34,24,32,33],[37,31,32,39,30,35]], None),
    11: ([[83,60,80,85,71],[90,55,84,91,85],[85,90,90,95,80]], None),
    12: ([[89,95,75,92,99,90],[60,95,89,80],[82,70,90,79,66]], None),
    14: ([[88,84,88,82,93],[76,78,60,62],[85,67,58]], None),
    15: (None, [(10,37,3),(10,38,4),(10,33,2)]),
    16: (None, [(15,42,16),(15,49,25),(15,44,9)]),
    17: ([[60,78,72,66],[84,78,93,81],[60,57,69,66]], None),
    18: ([[182,170,179],[170,192,190],[162,166]], None),
    19: ([[14,18,20,12,20,18],[12,10,22,12,16,12],[25,32,18,14,17,14]], None),
    20: ([[150,130,120,180,145],[150,120,135,160,110],[185,220,190,180,175],[175,150,120,130,175]], None),
    23: (None, [(11,40,23.4),(11,35,21.6),(11,39,25.2),(11,37,24.6)]),
    26: ([[92,85,96,95],[91,85,90,86],[85,93,82,84]], None),
    27: ([[33,30,28,29],[33,35,30,38],[28,36,30,34]], None),
    28: ([[40,37,43,41,35,38],[46,41,43,33,41,42],[46,40,41,48,39,44]], None),
    29: ([[83,80,82,83,82],[90,88,87,82,83],[81,83,80,82,79]], None),
    30: ([[75,80,84,85,81],[85,89,86,88],[80,81,84,79,83,85]], None),
    31: ([[180,175,179,176,190],[177,180,167,172],[175,176,177]], None),
    34: ([[9,8,7,8],[10,11,10,13],[6,7,8,11]], None),
    40: ([[260,280,240,260,300],[178,190,220,240],[211,190,250]], None),
    41: (None, [(10,37,3),(10,38,4),(10,33,2)]),
    42: ([[46,47,45,42,45],[34,36,35,39],[33,31,35]], None),
    44: ([[10,13,12,13],[16,14,15],[15,18]], None),
    46: ([[12,13,17,10,18],[15,19,20],[16,18]], None),
    47: (None, [(12,120,16),(10,186,18),(11,240,20)]),
}


if __name__ == "__main__":
    for number, (groups, summaries) in PROBLEMS.items():
        print(number, one_way(groups, summaries))
    print("block21", randomized_block([[210,230,190,180,190],[195,170,200,190,193],[295,275,290,275,265]]))
    print("block24", randomized_block([[25,29,21],[27,38,28],[20,24,16],[28,37,19]]))
    print("block35", randomized_block([[30,31,30,27,32],[36,35,28,31,30]]))
    print("factor25", factorial_2way([[[320,240],[380,300]],[[160,180],[240,210]],[[240,290],[360,380]]]))
    print("factor36", factorial_2way([[[14,16],[18,12]],[[18,20],[16,14]]]))
    print("t critical examples", t_critical(.05, 27), t_critical(.05, 21), t_critical(.01, 8))
