import pandas as pd
import networkx as nx
import itertools
import scipy.stats


def chi(data, X,Y,Z):
    """ A  function to determine whether variable X is indepenent of Y given conditioning set Z
    Parameters
    ----------
        X : str, 
            One variable being tested for independence, 
        Y : str
            The other variable being tested for independence
        Z: str[]
            The conditioning set
        alpha: float
            The minimum p-value returned by the indepence test
            for the data to be considered independent

    Returns
    -------
        boolean
            True : X independent of Y given Z
            False: X not independent of Y given Z
    """ 
    if len(Z) == 0:
        cont = pd.crosstab(data[X], data[Y])
        xvalues = [val for val in cont.index]
        yvalues = [val for val in cont.columns]
        ysums = {val: sum(cont[val]) for val in yvalues}
        xsums = {val: sum(cont.loc[val]) for val in xvalues}

        total = sum(xsums.values())
        observed = []
        expected = []
        for x in xvalues:
            for y in yvalues:
                observed.append(cont[y][x])
                expected.append(xsums[x]/total * ysums[y])
        freedom = len(xvalues) * len(yvalues) - ((len(xvalues) - 1) * (len(yvalues) - 1)) -1
        chisq, p = scipy.stats.chisquare(observed, f_exp=expected, ddof=freedom)
        return p, chisq
    else:
        zdata = [data[z] for z in Z]
        zdata = list(zip(*(column for column in zdata)))
        zdatastr = []
        for point in zdata:
            pointstr = ""
            for var in point:
                pointstr += str(var) + ","
            zdatastr.append(pointstr)
        zdata = pd.DataFrame(data=zdatastr,columns=['z'])
        cont = pd.crosstab(data[X],[zdata['z'], data[Y],])
        xvalues = [val for val in cont.index]
        yvalues = cont.columns.levels[1]
        zvalues = cont.columns.levels[0]
        labels = cont.columns.labels
        zyvalues = {z: [] for z in zvalues}
        for i in range(len(labels[0])):
            zyvalues[zvalues[labels[0][i]]].append(yvalues[labels[1][i]])
        ygz = {}
        xgz = {}
        #find x|z and y|z
        ztotal = {}
        for z in zvalues:
            #calculate y|z for all y and z
            #also capture z totals
            ygz[z] = {}
            xgz[z] = {x: 0 for x in xvalues}
            ztotal[z] = 0
            for y in zyvalues[z]:
                zytotal = sum(cont[z][y])
                ygz[z][y] = zytotal
                ztotal[z] += zytotal
                for x in xvalues:
                    xgz[z][x] += cont[z][y][x]
            for y in zyvalues[z]:
                ygz[z][y] =  ygz[z][y] / ztotal[z]
            for x in xvalues:
                xgz[z][x] = xgz[z][x]/ztotal[z]
        observed = []
        expected = []
        for z in zvalues:
            for y in zyvalues[z]:
                for x in xvalues:
                    observed.append(cont[z][y][x])
                    expected.append(ygz[z][y] * xgz[z][x] * ztotal[z])
        freedom = len(xvalues) * len(yvalues) * len(zvalues) - ((len(xvalues) - 1) * (len(yvalues) - 1) * (len(xvalues) - 1)) -1
        chisq, p =  scipy.stats.chisquare(observed, f_exp=expected, ddof=freedom)
        p = 1
        return p, chisq