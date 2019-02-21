import networkx as nx  
import unittest
import matplotlib.pyplot as plt
from pc import PCAlg
from indepTests import chi
"""
class ChiSquareTests(unittest.TestCase):
    def setUp(self):
        self.data = PCAlg.prepare_data('alarm_10000.dat', ' ', True)

    
    def test1(self):
        p = chi(self.data, 'EXPCO2', 'EXPCO2', [])
        assert(p == 0)
        
    def test2(self):
        p = chi(self.data, 'EXPCO2', 'EXPCO2', ['PAP'])
        assert(p == 0)
    
    def test3(self):
        p = chi(self.data, 'EXPCO2', 'EXPCO2', ['PAP','PULMEMBOLUS'])
        assert(p == 0)
        
    def test4(self):
        self.data =  PCAlg.prepare_data('testdata.dat', ' ', True)
        p = chi(self.data, 'A', 'B', [])
        assert(p==1) 

    def test5(self):
        self.data =  PCAlg.prepare_data('testdata.dat', ' ', True)
        p = chi(self.data, 'A', 'C', [])
        assert(round(p,3)==0.505)   

    def test6(self):
        self.data =  PCAlg.prepare_data('testdata.dat', ' ', True)
        p = chi(self.data, 'A', 'D', [])
        assert(round(p,3)==0.505) 
    
    def test7(self):
        self.data =  PCAlg.prepare_data('testdata.dat', ' ', True)
        p = chi(self.data, 'A', 'B', ['C'])
        print(p)
        assert(round(p,3)==0.018) 

"""

class SkeletonTests(unittest.TestCase):
    
    def setUp(self):
        self.data = PCAlg.prepare_data('alarm_10000.dat', ' ', True)
        self.pcalg = PCAlg(self.data, chi)
        self.skeleton = nx.Graph()
        
    def test1(self):
        self.skeleton.add_nodes_from([1,2,3,4,5])
        sepset 
        self.skeleton.add_edges_from([[1,2],[3,4],[3,5],[4,2],[5,2]])
        directed = self.pcalg.orientEdges(self.skeleton)
        print(directed.edges)

if __name__ == '__main__':
    unittest.main()
    
""""
x= 1  y= 2  S=  : pval = 9.953947e-256 
x= 1  y= 3  S=  : pval = 9.082948e-06 
x= 1  y= 4  S=  : pval = 0.03933131 
x= 1  y= 5  S=  : pval = 1.414214e-95 
x= 2  y= 1  S=  : pval = 9.953947e-256 
x= 2  y= 3  S=  : pval = 2.783621e-17 
x= 2  y= 4  S=  : pval = 6.584309e-09 
x= 2  y= 5  S=  : pval = 0 
x= 3  y= 1  S=  : pval = 9.082948e-06 
x= 3  y= 2  S=  : pval = 2.783621e-17 
x= 3  y= 4  S=  : pval = 2.445323e-41 
x= 3  y= 5  S=  : pval = 6.410634e-65 
x= 4  y= 2  S=  : pval = 6.584309e-09 
x= 4  y= 3  S=  : pval = 2.445323e-41 
x= 4  y= 5  S=  : pval = 0.003960591 
x= 5  y= 1  S=  : pval = 1.414214e-95 
x= 5  y= 2  S=  : pval = 0 
x= 5  y= 3  S=  : pval = 6.410634e-65 
x= 5  y= 4  S=  : pval = 0.003960591 
Order=1; remaining edges:18
x= 1  y= 2  S= 3 : pval = 6.9655e-250 
x= 1  y= 2  S= 5 : pval = 8.253147e-161 
x= 1  y= 3  S= 2 : pval = 0.8635111 
x= 1  y= 5  S= 2 : pval = 0.7130915 
x= 2  y= 1  S= 3 : pval = 6.9655e-250 
x= 2  y= 1  S= 4 : pval = 2.396259e-253 
x= 2  y= 1  S= 5 : pval = 8.253147e-161 
x= 2  y= 3  S= 1 : pval = 4.883148e-12 
x= 2  y= 3  S= 4 : pval = 2.580833e-26 
x= 2  y= 3  S= 5 : pval = 9.47727e-10 
x= 2  y= 4  S= 1 : pval = 2.765395e-07 
x= 2  y= 4  S= 3 : pval = 4.248502e-18 
x= 2  y= 4  S= 5 : pval = 3.935485e-126 
x= 2  y= 5  S= 1 : pval = 4.940656e-324 
x= 2  y= 5  S= 3 : pval = 0 
x= 2  y= 5  S= 4 : pval = 0 
x= 3  y= 2  S= 1 : pval = 4.883148e-12 
x= 3  y= 2  S= 4 : pval = 2.580833e-26 
x= 3  y= 2  S= 5 : pval = 9.47727e-10 
x= 3  y= 4  S= 1 : pval = 2.559598e-42 
x= 3  y= 4  S= 2 : pval = 3.581916e-50 
x= 3  y= 4  S= 5 : pval = 1.883917e-38 
x= 3  y= 5  S= 1 : pval = 2.791544e-62 
x= 3  y= 5  S= 2 : pval = 4.347867e-57 
x= 3  y= 5  S= 4 : pval = 6.227292e-62 
x= 4  y= 2  S= 3 : pval = 4.248502e-18 
x= 4  y= 2  S= 5 : pval = 3.935485e-126 
x= 4  y= 3  S= 2 : pval = 3.581916e-50 
x= 4  y= 3  S= 5 : pval = 1.883917e-38 
x= 4  y= 5  S= 2 : pval = 1.259319e-120 
x= 4  y= 5  S= 3 : pval = 0.7150221 
x= 5  y= 2  S= 1 : pval = 4.940656e-324 
x= 5  y= 2  S= 3 : pval = 0 
x= 5  y= 2  S= 4 : pval = 0 
x= 5  y= 3  S= 1 : pval = 2.791544e-62 
x= 5  y= 3  S= 2 : pval = 4.347867e-57 
x= 5  y= 3  S= 4 : pval = 6.227292e-62 
Order=2; remaining edges:12
x= 2  y= 1  S= 3 4 : pval = 2.709864e-244 
x= 2  y= 1  S= 3 5 : pval = 7.101437e-156 
x= 2  y= 1  S= 4 5 : pval = 1.660283e-137 
x= 2  y= 3  S= 1 4 : pval = 2.332881e-18 
x= 2  y= 3  S= 1 5 : pval = 3.652957e-06 
x= 2  y= 3  S= 4 5 : pval = 0.3391282 
x= 2  y= 4  S= 1 3 : pval = 1.00277e-13 
x= 2  y= 4  S= 1 5 : pval = 5.952032e-103 
x= 2  y= 4  S= 3 5 : pval = 1.170103e-115 
x= 2  y= 5  S= 1 3 : pval = 1.281738e-316 
x= 2  y= 5  S= 1 4 : pval = 0 
x= 2  y= 5  S= 3 4 : pval = 0 
x= 3  y= 4  S= 2 5 : pval = 1.432156e-28 
x= 3  y= 5  S= 2 4 : pval = 2.137569e-35 

"""