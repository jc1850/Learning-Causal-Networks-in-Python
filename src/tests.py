import networkx as nx  
import unittest
import matplotlib.pyplot as plt
from pc import PCAlg
from indepTests import chi

class ChiSquareTests(unittest.TestCase):
    def setUp(self):
        self.data = PCAlg.prepare_data('alarm_10000.dat', ' ', True)

    
    def test1(self):
        p, *_= chi(self.data, 'EXPCO2', 'EXPCO2', [])
        assert(p == 0)
        


    def test2(self):
        p, h = chi(self.data, 'PAP', 'PULMEMBOLUS', [])
        assert(round(h,1)==1041.7)
    
    def test3(self):
        p, h = chi(self.data, 'EXPCO2', 'PULMEMBOLUS', [])
        assert(round(h,3)==0.349)
        
    def test4(self):
        p, h = chi(self.data, 'EXPCO2', 'PULMEMBOLUS', ['PAP'])
        assert(round(h,3)== 3.841)
    
    def test5(self):
        p, h = chi(self.data, 'EXPCO2', 'PULMEMBOLUS', ['PAP','KINKEDTUBE'])
        assert(round(h,3)== 3.862)
        
    def test5(self):
        p, h = chi(self.data, 'EXPCO2', 'PULMEMBOLUS', ['KINKEDTUBE','PAP',])
        assert(round(h,3)== 3.862)

class SkeletonTests(unittest.TestCase):
    
    def setUp(self):
        self.data = PCAlg.prepare_data('asia_1000.data', ' ', True)
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
        
    def test2(self):
        pdag = self.pcalg.learnGraph()
        print(pdag.edges)
        nx.draw_networkx(pdag)
        plt.show()

if __name__ == '__main__':
    unittest.main()
    

