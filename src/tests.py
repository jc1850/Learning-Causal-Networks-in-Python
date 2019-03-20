import networkx as nx  
import unittest
import matplotlib.pyplot as plt
from pc import PCAlg
from indepTests import chi
from graphs import PDAG, PAG
from fci import FCIAlg

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
        
    def test6(self):
        p, h = chi(self.data, 'EXPCO2', 'PULMEMBOLUS', ['KINKEDTUBE','PAP',])
        assert(round(h,3)== 3.862)
    
    def test7(self):
        self.data = PCAlg.prepare_data('asia_1000.data', ' ', True)
        p, h = chi(self.data, 'asia', 'tub', [])
        assert(round(h,3)== 34.496)

    def test8(self):
        self.data = PCAlg.prepare_data('asia_1000.data', ' ', True)
        p, h = chi(self.data, 'asia', 'tub', ['smoke'])
        assert(round(h,3)== 37.322)

    def test9(self):
        self.data = PCAlg.prepare_data('asia_1000.data', ' ', True)
        p, h = chi(self.data, 'asia', 'tub', ['smoke', 'lung'])
        assert(round(h,3)== 36.997)

    def test10(self):
        self.data = PCAlg.prepare_data('asia_1000.data', ' ', True)
        p, h = chi(self.data, 'either', 'tub', ['bronc', 'xray'])
        assert(round(h,3)== 991)

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
    

class PathTests(unittest.TestCase):
    def setUp(self):
        self.directed = nx.DiGraph()
        self.directed.add_nodes_from([1,2,3,4,5])

    def test1(self):
        self.directed.add_edges_from([[1,2],[2,3]])
        assert(PCAlg.findPath(1,3,self.directed, []))

    def test2(self):
        self.directed.add_edges_from([[1,2],[2,3]])
        assert(not PCAlg.findPath(1,5,self.directed, []))
    
    def test3(self):
        self.directed.add_edges_from([[1,2],[2,3]])
        self.directed.add_edges_from([[3,4]])
        assert(PCAlg.findPath(3,4,self.directed, []))

    def test4(self):
        self.directed.add_edges_from([[1,2],[2,3]])
        self.directed.add_edges_from([[3,4]])
        assert(PCAlg.findPath(1,4,self.directed, []))

    def test5(self):
        self.directed.add_edges_from([[1,2],[1,3]])
        self.directed.add_edges_from([[3,4],[3,5]])
        assert(PCAlg.findPath(1,5,self.directed, []))

    def test6(self):
        self.directed.add_edges_from([[1,3]])
        self.directed.add_edges_from([[1,2],[3,4],[3,5]])
        assert(not PCAlg.findPath(2,5,self.directed, []))
   
class D_SepTests(unittest.TestCase):
    def setUp(self):
        self.skeleton = nx.Graph()
        self.skeleton.add_nodes_from([1,2,3,4,5,6])
        self.pdag = PDAG()
        self.pdag.add_nodes_from(self.skeleton)
        
    def test1(self):
        self.pdag.add_edge(1,2)
        self.pdag.add_edge(3,2)
        self.skeleton.add_edges_from(self.pdag.edges)
        dseps = FCIAlg.possible_d_seps(self.skeleton, self.pdag)
        assert(dseps == {1:[2,3],2:[1,3],3:[1,2], 4:[], 5:[], 6:[]})
    
    def test2(self):
        self.pdag.add_edge(1,2)
        self.pdag.add_edge(2,3)
        self.skeleton.add_edges_from(self.pdag.edges)
        dseps = FCIAlg.possible_d_seps(self.skeleton, self.pdag)
        assert(dseps == {1:[2],2:[1,3],3:[2], 4:[], 5:[], 6:[]})
    
    def test3(self):
        self.pdag.add_edge(1,2)
        self.pdag.add_edge(3,2)
        self.pdag.add_edge(2,4,False)
        self.pdag.add_edge(3,4,False)
        self.skeleton.add_edges_from(self.pdag.edges)
        dseps = FCIAlg.possible_d_seps(self.skeleton, self.pdag)
        assert(dseps == {1:[2,3,4],2:[1,3,4],3:[1,2,4,], 4:[1,2,3], 5:[], 6:[]})

class PagPathTests(unittest.TestCase):

    def setUp(self):
        self.pag = PAG()
        self.pag.add_nodes_from([1,2,3,4,5])
    
    def test1(self):
        self.pag.add_edges_from([[1,2],[2,3]])
        self.pag.setTag([1,2],2,'>')
        self.pag.setTag([2,3],3,'>')
        assert(FCIAlg.hasDirectedPath(self.pag, 1,3))
    
    def test2(self):
        self.pag.add_edges_from([[1,2],[2,3]])
        self.pag.setTag([1,2],2,'>')
        assert(not FCIAlg.hasDirectedPath(self.pag, 1,3))
    
class DiscPathTest(unittest.TestCase):

    def setUp(self):
        self.pag = PAG()
        self.pag.add_nodes_from([1,2,3,4])

    def test1(self):
        self.pag.add_edges_from([[1,2],[2,3],[3,4],[2,4]])
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(3,2)
        self.pag.fully_direct_edge(2,4)
        self.pag.fully_direct_edge(3,4)
        assert(self.pag.hasDiscPath(1,4,3))

    def test2(self):
        self.pag.add_edges_from([[1,2],[2,3],[3,4],[2,4]])
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(3,2)
        self.pag.fully_direct_edge(2,4)
        assert(not self.pag.hasDiscPath(1,4,3))

    def test3(self):
        self.pag.add_edges_from([[1,2],[2,3],[3,4],[2,4]])
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(2,3)
        self.pag.fully_direct_edge(2,4)
        self.pag.fully_direct_edge(3,4)
        assert(not self.pag.hasDiscPath(1,4,3))

    def test4(self):
        self.pag.add_edges_from([[1,2],[2,3],[3,4],[2,4]])
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(3,2)
        self.pag.fully_direct_edge(3,4)
        assert(not self.pag.hasDiscPath(1,4,3))
    
    def test4(self):
        self.pag.add_edges_from([[1,2],[2,3],[3,4],[2,4]])
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(3,2)
        self.pag.fully_direct_edge(3,4)
        self.pag.fully_direct_edge(1,4)
        assert(not self.pag.hasDiscPath(1,4,3))

if __name__ == '__main__':
    unittest.main()
    

