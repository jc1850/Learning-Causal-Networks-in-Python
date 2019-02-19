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
        freedom = len(xvalues) * len(yvalues) - ((len(xvalues) - 1) * (len(yvalues) - 1))
        chisq, p = scipy.stats.chisquare(observed, f_exp=expected, ddof=2)
        return p
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
        cont = pd.crosstab(data[X],[data[Y], zdata['z']])
        xvalues = [val for val in cont.index]
        labels = cont.columns.labels
        yvalues = cont.columns.levels[0]
        zvalues = cont.columns.levels[1]
        zyvalues = {y: [] for y in yvalues}
        for i in range(len(labels[0])):
            zyvalues[yvalues[labels[0][i]]].append(zvalues[labels[1][i]])
        xsums = {val: sum(cont.loc[val]) for val in xvalues}
        ysums = ({y: sum(sum([cont[y][z] for z in zyvalues[y]]))  for y in yvalues})
        zsums = {z:  0 for z in zvalues}
        for y in yvalues:
            for z in zyvalues[y]:
                zsums[z] += sum(cont[y][z])
        total = sum(xsums.values())
        observed = []
        expected = []
        for x in xvalues:
            for y in yvalues:
                for z in zyvalues[y]:
                    observed.append(cont[y][z][x])
                    expected.append(xsums[x]*ysums[y]*zsums[z]/ (total**2))

        freedom = len(xvalues) * len(yvalues) * len(zvalues) - ((len(xvalues) - 1) * (len(yvalues) - 1) * (len(xvalues) - 1)) -1
        chisq, p = scipy.stats.chisquare(observed, f_exp=expected, ddof = freedom)
        return p
            
        
        
            