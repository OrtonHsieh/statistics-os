#!/usr/bin/env python3
"""Recompute Chapter 17 forecasting and seasonal-decomposition problems."""

from __future__ import annotations

import math


def trend(y):
    t = list(range(1, len(y) + 1))
    tb, yb = sum(t)/len(t), sum(y)/len(y)
    b = sum((a-tb)*(v-yb) for a,v in zip(t,y))/sum((a-tb)**2 for a in t)
    a = yb-b*tb
    return a,b


def weighted_forecasts(y, weights_recent_to_oldest):
    k=len(weights_recent_to_oldest); den=sum(weights_recent_to_oldest); out={}
    for next_index in range(k, len(y)+1):
        vals=list(reversed(y[next_index-k:next_index]))
        out[next_index+1]=sum(w*v for w,v in zip(weights_recent_to_oldest,vals))/den
    return out


def exp_smooth(y, alpha):
    # Keys are one-based periods; F1=A1 and F(t)=a*A(t-1)+(1-a)*F(t-1).
    f={1:y[0]}
    for t in range(2,len(y)+2):
        f[t]=alpha*y[t-2]+(1-alpha)*f[t-1]
    errors=[y[t-1]-f[t] for t in range(2,len(y)+1)]
    return f,sum(e*e for e in errors)/len(errors),sum(abs(e) for e in errors)/len(errors)


def moving_forecast(y,k):
    f={}
    for t in range(k+1,len(y)+2): f[t]=sum(y[t-k-1:t-1])/k
    errs=[y[t-1]-f[t] for t in range(k+1,len(y)+1)]
    return f,sum(e*e for e in errs)/len(errs),sum(abs(e) for e in errs)/len(errs)


def centered_ma(y,k):
    assert k%2==1
    h=k//2; c={}
    for i in range(h,len(y)-h): c[i+1]=sum(y[i-h:i+h+1])/k
    errs=[y[t-1]-v for t,v in c.items()]
    return c,sum(e*e for e in errs)/len(errs)


def simple_quarter_indexes(y):
    qmeans=[sum(y[q::4])/(len(y[q::4])) for q in range(4)]
    grand=sum(y)/len(y)
    return [v/grand for v in qmeans]


def seasonal_decompose(y):
    # Even-period centered moving average, ratio-to-moving-average indexes.
    ma4=[sum(y[i:i+4])/4 for i in range(len(y)-3)]
    cma={i+3:(ma4[i]+ma4[i+1])/2 for i in range(len(ma4)-1)} # one-based t
    ratios={t:y[t-1]/v for t,v in cma.items()}
    raw=[]
    for q in range(1,5):
        vals=[v for t,v in ratios.items() if (t-1)%4+1==q]
        raw.append(sum(vals)/len(vals))
    scale=4/sum(raw)
    indexes=[v*scale for v in raw]
    deseason=[v/indexes[i%4] for i,v in enumerate(y)]
    return ma4,cma,ratios,indexes,deseason


if __name__=='__main__':
    for n,y,future in [(1,[18,20,22,24,26,28],17),(14,[12,16,17,19,18,21,22],10),
                       (15,[6.3,7.7,8,8.2,8.8,8],10),(18,[2,3,5,4,6,8,9,9],9),
                       (19,[195,200,250,270,320,380,440,460,500,500],11),
                       (25,[120,132,148,152,160,175,182,190,195,205],11),
                       (27,[15,16.2,17.1,18.1,18.8,19.2,20.5],8)]:
        a,b=trend(y);print('trend',n,a,b,'future',[(t,a+b*t) for t in range(future, future+(5 if n==27 else (2 if n==25 else 1)))])
    for n,y,w in [(2,[40,45,57,60,75,87],[5,3,2]),(3,[40,45,57,60,75,87],[6,4,2]),(4,[80,83,87,90,95,98],[5,4,3])]:
        print('weighted',n,weighted_forecasts(y,w))
    for n,y,alphas in [(6,[18,25,30,40],[.3]),(7,[18,25,30,40],[.3,.1]),(22,[105,90,95,110,105,100],[.2,.3]),
                       (23,[22,24,28,24,22,24,20,26,24,28,26],[.4]),(24,[82,80,84,83,80,79,82],[.2,.3])]:
        for alpha in alphas: print('smooth',n,alpha,exp_smooth(y,alpha))
    for n,y,k in [(8,[35,30,26,34,28,38],1),(9,[45,48,42,44,50,60],1),(10,[12,14,10,16,29,22],1),
                  (16,[15,16,19,18,19,20,19,22,15,21],4),(21,[18,22,17,18,28,20,12],3),
                  (23,[22,24,28,24,22,24,20,26,24,28,26],3)]: print('moving',n,moving_forecast(y,k))
    print('centered17',centered_ma([8,3,4,5,12,10],3))
    for n,y,tr in [(11,[170,111,270,250,180,96,280,220,190,120,290,223],(174,4)),
                   (12,[106,256,273,190,135,280,280,180,149,292,290,209],(185.86,5.25)),
                   (13,[14,20,36,10,28,16,40,14,30,18,38,12],(20.82,.336))]:
        idx=simple_quarter_indexes(y); t13=tr[0]+tr[1]*13
        print('simple seasonal',n,idx,'trend13',t13,'seasonal forecast',t13*idx[0])
    for n,y in [(20,[2.5,1.5,2.4,1.6,2,1.4,1.7,1.9,2.5,2,2.4,2.1]),
                (26,[300,240,240,290,350,300,280,320,410,400,390,410,490,450,440,510,540,530,520,540]),
                (28,[150,120,160,150,150,130,180,160,170,140,200,180,200,150,230,200]),
                (31,[160,180,190,170,200,210,260,230,210,240,290,260])]:
        ma,cma,rat,idx,des=seasonal_decompose(y);print('decomp',n,'ma',ma,'cma',cma,'rat',rat,'idx',idx,'des',des)
        if n==26:
            a,b=trend(des);print('decomp26 trend',a,b,'year6',[ (a+b*t)*idx[(t-1)%4] for t in range(21,25)])
    idx=[.589,1.351,1.335,.726];y=[10,20,25,5,10,30,35,25,20,40,35,15,20,50,45,35]
    des=[v/idx[i%4] for i,v in enumerate(y)];a,b=trend(des)
    print('p29',des,a,b,[(a+b*t)*idx[(t-1)%4] for t in range(17,21)])
    print('p30',[(126.23-1.6*t)*[1.2,.9,.8,1.1][(t-1)%4] for t in range(21,25)])
