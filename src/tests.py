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
        sepset ={(1,2):(), (1,3):(2,), (1,4):(), (1,5):(2,),
                 (2,1):(), (2,3):(4,5), (2,4):(), (2,5):(),
                 (3,1):(2,), (3,2):(4,5), (3,4):(), (3,5):(),
                 (4,1):(), (4,2):(), (4,3):(), (4,5):(3,),
                 (5,1):(2,), (5,2):(), (5,3):(), (5,4):(3,), }
        self.skeleton.add_edges_from([[1,2],[3,4],[3,5],[4,2],[5,2]])
        directed = self.pcalg.orientEdges(self.skeleton, sepset)
        assert(list(directed.edges) ==  [(1, 2), (4, 2), (4, 3), (5, 2), (5, 3), (3, 4), (3, 5)])

if __name__ == '__main__':
    unittest.main()
    

