import numpy as np 
import statsmodels.tsa.api as smt
from arch import arch_model

#WARNING::: INPUTS SHOULD BE SCALED LOG RETURNS
def _get_best_model(TS, upper_=6):
    best_aic = np.inf 
    best_order = None
    best_mdl = None

    pq_rng = range(1,upper_) 
    d_rng = range(3) 
    for i in pq_rng:
        for d in d_rng:
            for j in pq_rng:
                try:
                    tmp_mdl = smt.ARIMA(TS, order=(i,d,j)).fit(method='mle', trend='nc')
                    tmp_aic = tmp_mdl.aic
                    if tmp_aic < best_aic:
                        best_aic = tmp_aic
                        best_order = (i, d, j)
                        best_mdl = tmp_mdl
                except: continue
    return best_aic, best_order, best_mdl


def get_arch(TS, upper_=6):
	par = _get_best_model(TS, upper_=upper_)
	best_order = par[1]
	am = arch_model(TS, p=best_order[0], o=best_order[1], q=best_order[2], dist='StudentsT')
	res = am.fit(update_freq=5, disp='off')
	return res