import networkx as nx  
import unittest
import matplotlib.pyplot as plt
from pc import PCAlg
from indepTests import chi

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

data = PCAlg.prepare_data('alarm_10000.dat', ' ', True)
alg = PCAlg(data, chi)
graph = alg.learnGraph()
nx.draw_networkx(graph)

plt.show()