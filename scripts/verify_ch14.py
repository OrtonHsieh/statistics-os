#!/usr/bin/env python3
"""Recompute Chapter 14 simple-regression problem answers."""

from __future__ import annotations

import math

from verify_ch13 import f_critical, f_sf, t_cdf, t_critical


def regress(x, y):
    n = len(x)
    xb, yb = sum(x) / n, sum(y) / n
    sxx = sum((v - xb) ** 2 for v in x)
    syy = sum((v - yb) ** 2 for v in y)
    sxy = sum((a - xb) * (b - yb) for a, b in zip(x, y))
    b1, b0 = sxy / sxx, yb - (sxy / sxx) * xb
    fitted = [b0 + b1 * v for v in x]
    residuals = [obs - fit for obs, fit in zip(y, fitted)]
    sse = sum(e * e for e in residuals)
    ssr = syy - sse
    df = n - 2
    mse = sse / df
    se = math.sqrt(mse)
    seb1 = math.sqrt(mse / sxx)
    t = b1 / seb1
    f = t * t
    p = 2 * (1 - t_cdf(abs(t), df))
    r2 = ssr / syy
    r = math.copysign(math.sqrt(r2), b1)
    return dict(n=n, xb=xb, yb=yb, sxx=sxx, syy=syy, sxy=sxy, b0=b0, b1=b1,
                fitted=fitted, residuals=residuals, sse=sse, ssr=ssr, sst=syy,
                df=df, mse=mse, se=se, seb1=seb1, t=t, f=f, p=p, r2=r2, r=r,
                f05=f_critical(.05, 1, df), t05=t_critical(.05, df))


def interval(result, x0, alpha):
    yhat = result['b0'] + result['b1'] * x0
    n, sxx, xb, se, df = result['n'], result['sxx'], result['xb'], result['se'], result['df']
    tc = t_critical(alpha, df)
    mean_se = se * math.sqrt(1 / n + (x0 - xb) ** 2 / sxx)
    pred_se = se * math.sqrt(1 + 1 / n + (x0 - xb) ** 2 / sxx)
    return dict(yhat=yhat, tc=tc, mean=(yhat-tc*mean_se, yhat+tc*mean_se),
                prediction=(yhat-tc*pred_se, yhat+tc*pred_se), mean_se=mean_se, pred_se=pred_se)


DATA = {
    1: ([500,700,750,590,540,650,480],[7,7.5,9,6.5,7.5,7,4.5]),
    3: ([34,36,32,35,30,38,40],[3,4,6,5,9,2,1]),
    12: ([2,6,9,9],[4,7,8,9]),
    13: ([2,3,4,5,6],[4,4,3,2,1]),
    16: ([32,33,35,34,36,37,39,42],[15,16,18,17,16,19,19,24]),
    17: ([10,20,30,40,50],[7,5,4,2,1]),
    20: ([9.2,7.6,10.4,5.3],[22,20,10,45]),
    21: ([50,60,70,80,90,100],[350,200,210,100,60,40]),
    22: ([45,30,22,25,5],[1,3,4,3,6]),
    23: ([2,3,6,7,8,7,9],[12,9,8,7,6,5,2]),
    24: ([0,50,250,150,125],[200,270,420,300,325]),
    25: ([20,19,22,25,14],[.45,10.75,5.4,7.8,5.6]),
    26: ([0,3,2,1,4],[28,40,36,28,48]),
    27: ([18,22,21,28],[210,180,220,280]),
    28: ([2,2,3,4,3,1,4,3,4,4],[20,23,25,26,28,29,27,30,33,35]),
    29: ([18,20,23,34,24,27,27],[20,24,24,25,26,27,34]),
    30: ([1.8,2.3,2.6,2.4,2.8,3.0,3.4,3.2,3.6,3.8],[26,31,28,30,34,38,41,44,40,43]),
}


if __name__ == '__main__':
    for number, (x, y) in DATA.items():
        result = regress(x, y)
        print(number, result)
        if number == 1:
            print('  x800 alpha10', interval(result, 800, .10))
        if number == 16:
            print('  x40 alpha05', interval(result, 40, .05))
        if number == 20:
            print('  x10 alpha01', interval(result, 10, .01))
        if number == 25:
            print('  x20 alpha05', interval(result, 20, .05))
