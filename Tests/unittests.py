import networkx as nx  
import unittest
import matplotlib.pyplot as plt
import sys
sys.path.append('src')
from pc import PCAlg
from indepTests import chi
from graphs import PDAG, PAG
from fci import FCIAlg

class ChiSquareTests(unittest.TestCase):
    # Chi squared independence test functions
    def setUp(self):
        self.data = PCAlg.prepare_data('data/alarm_10000.dat', ' ', True)

    
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
        self.data = PCAlg.prepare_data('data/asia_1000.data', ' ', True)
        p, h = chi(self.data, 'asia', 'tub', [])
        assert(round(h,3)== 34.496)

    def test8(self):
        self.data = PCAlg.prepare_data('data/asia_1000.data', ' ', True)
        p, h = chi(self.data, 'asia', 'tub', ['smoke'])
        assert(round(h,3)== 37.322)

    def test9(self):
        self.data = PCAlg.prepare_data('data/asia_1000.data', ' ', True)
        p, h = chi(self.data, 'asia', 'tub', ['smoke', 'lung'])
        assert(round(h,3)== 36.997)

    
    def test10(self):
        self.data = PCAlg.prepare_data('data/asia_1000.data', ' ', True)
        p, h = chi(self.data, 'either', 'tub', ['bronc', 'xray'])
        assert(round(h,3)== 991)
    
    def test11(self):
        self.data = PCAlg.prepare_data('data/asia_10000.data', ' ', True)
        p, h = chi(self.data, 'either', 'tub', ['bronc', 'xray'])
        assert(round(h,3)== 9884.0 )
    
    def test12(self):
        self.data = PCAlg.prepare_data('data/alarm_1000.data', ' ', False)
        p, h = chi(self.data, '1', '2', ['3', '4'])
        assert(round(h,3)==3.115)
    
    def test13(self):
        self.data = PCAlg.prepare_data('data/insurance_1000.data', ' ', False)
        p, h = chi(self.data, '0', '1', ['2', '3'])
        assert(round(h,3)==35.531)

class SkeletonTests(unittest.TestCase):
    # Tests for the skeleton estimation
    def setUp(self):
        self.data = PCAlg.prepare_data('data/asia_1000.data', ' ', True)
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
    #Tests for possible d sep set calculation
    def setUp(self):
        self.pag = PAG()
        self.pag.add_nodes_from([1,2,3,4,5,6])
        
    def test1(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(3,2)
        dseps = FCIAlg.possible_d_seps(self.pag)
        assert(dseps == {1:[2],2:[1,3],3:[2], 4:[], 5:[], 6:[]})
    
    def test2(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(3,2)
        dseps = FCIAlg.possible_d_seps(self.pag)
        assert(dseps == {1:[2,3],2:[1,3],3:[1,2], 4:[], 5:[], 6:[]})
    
    def test3(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(3,2)
        self.pag.add_edge(2,4)
        self.pag.add_edge(3,4)
        dseps = FCIAlg.possible_d_seps(self.pag)
        assert(dseps == {1:[2,3,4],2:[1,3,4],3:[1,2,4,], 4:[1,2,3], 5:[], 6:[]})

    def test4(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(3,2)
        self.pag.add_edge(3,1)
        dseps = FCIAlg.possible_d_seps(self.pag)
        assert(dseps == {1:[2,3],2:[1,3],3:[1,2], 4:[], 5:[], 6:[]})
    
class DiscPathTest(unittest.TestCase):
    # tests for finding discriminating paths on a graph
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
        self.pag.add_edges_from([[1,2],[2,3],[2,4]])
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
    
    def test5(self):
        self.pag.add_edges_from([[1,2],[2,3],[3,4],[2,4]])
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(3,2)
        self.pag.fully_direct_edge(3,4)
        self.pag.fully_direct_edge(1,4)
        assert(not self.pag.hasDiscPath(1,4,3))


class VOrientTests(unittest.TestCase):
    # tests for v structure orientation
    def setUp(self):
        self.data = PCAlg.prepare_data('data/asia_1000.data', ' ', True)
        self.pcalg = PCAlg(self.data, chi)
        self.fcialg = FCIAlg(self.data, chi)
        self.directed = nx.DiGraph()
        self.undirected = nx.Graph()
        self.directed.add_nodes_from([1,2,3,4])
        self.undirected.add_nodes_from(self.directed)
        self.pag = PAG()
        self.pag.add_nodes_from(self.undirected)
        self.sepset = {(x,y): [] for x in [1,2,3,4,5] for y in [1,2,3,4,5] if x!=y}

    def test1(self):
        self.undirected.add_edges_from([(1,2), (2,3)])
        self.pcalg.orient_V(self.undirected, self.directed, self.sepset)
        part1 = not self.undirected.has_edge(1,2) and not self.undirected.has_edge(3,2) 
        part2 =  self.directed.has_edge(1,2) and  self.directed.has_edge(3,2) 
        assert(part1 and part2)

    def test2(self):
        self.undirected.add_edges_from([(1,2), (2,3)])
        self.sepset[(1,3)].append(2)
        self.sepset[(3,1)].append(2)
        self.pcalg.orient_V(self.undirected, self.directed, self.sepset)
        part1 = not self.undirected.has_edge(1,2) and not self.undirected.has_edge(3,2) 
        part2 =  self.directed.has_edge(1,2) and  self.directed.has_edge(3,2) 
        assert(not (part1 and part2))
    
    def test3(self):
        self.pag.add_edges_from([(1,2), (2,3)])
        self.fcialg.orient_V(self.pag, self.sepset)
        assert(self.pag.has_directed_edge(1,2) and self.pag.has_directed_edge(3,2))
    
    def test4(self):
        self.pag.add_edges_from([(1,2), (2,3)])        
        self.sepset[(1,3)].append(2)
        self.sepset[(3,1)].append(2)
        self.fcialg.orient_V(self.pag, self.sepset)
        assert(not self.pag.has_directed_edge(1,2) and not self.pag.has_directed_edge(3,2))

class RulesTests(unittest.TestCase):
    # tests for fci algorithm orientation rules
    def setUp(self):
        self.pag = PAG()
        self.pag.add_nodes_from([1,2,3,4,5])
    
    # Rule 1 Tests
    def test11(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.direct_edge(1,2)
        FCIAlg.rule1(self.pag,1,2,3)
        assert(self.pag.has_fully_directed_edge(2,3))
    
    def test12(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        FCIAlg.rule1(self.pag,1,2,3)
        assert(not self.pag.has_fully_directed_edge(2,3))
    
    # Rule 2 Tests
    def test21(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(1,3)
        self.pag.direct_edge(1,2)
        self.pag.fully_direct_edge(2,3)
        FCIAlg.rule2(self.pag,1,2,3)
        assert(self.pag.has_directed_edge(1,3))

    def test22(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(1,3)
        self.pag.direct_edge(2,3)
        self.pag.fully_direct_edge(1,2)
        FCIAlg.rule2(self.pag,1,2,3)
        assert(self.pag.has_directed_edge(1,3))
    
    def test23(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(1,3)
        self.pag.fully_direct_edge(3,2)
        self.pag.fully_direct_edge(1,2)
        FCIAlg.rule2(self.pag,1,2,3)
        assert(not self.pag.has_directed_edge(1,3))

    # Rule 3 Tests
    def test31(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(1,4)
        self.pag.add_edge(4,3)
        self.pag.add_edge(4,2)
        self.pag.direct_edge(1,2)
        self.pag.direct_edge(3,2)
        FCIAlg.rule3(self.pag,1,2,3,4)
        assert(self.pag.has_directed_edge(4,2))
    
    def test32(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(1,4)
        self.pag.add_edge(4,3)
        self.pag.add_edge(4,2)
        self.pag.direct_edge(1,2)
        self.pag.direct_edge(3,2)
        self.pag.direct_edge(1,4)
        FCIAlg.rule3(self.pag,1,2,3,4)
        assert(not self.pag.has_directed_edge(4,2))

    # Rule 4 Tests
    def test41(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(3,4)
        self.pag.add_edge(4,5)
        self.pag.add_edge(2,5)
        self.pag.add_edge(3,5)
        self.pag.direct_edge(1,2)
        self.pag.direct_edge(2,3)
        self.pag.direct_edge(2,5)
        self.pag.direct_edge(3,2)
        self.pag.direct_edge(3,4)
        self.pag.direct_edge(3,5)
        self.pag.direct_edge(4,3)
        self.pag.direct_edge(3,2)
        sepset = {(1,5) : [4], (5,1): [4]}
        FCIAlg.rule4(self.pag, 3,4,5,1, sepset)
        assert(self.pag.has_directed_edge(4,5))
    
    def test42(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(3,4)
        self.pag.add_edge(4,5)
        self.pag.add_edge(2,5)
        self.pag.add_edge(3,5)
        self.pag.direct_edge(1,2)
        self.pag.direct_edge(2,3)
        self.pag.direct_edge(2,5)
        self.pag.direct_edge(3,2)
        self.pag.direct_edge(3,4)
        self.pag.direct_edge(3,5)
        self.pag.direct_edge(4,3)
        self.pag.direct_edge(3,2)
        sepset = {(1,5) : [2], (5,1): [2]}
        FCIAlg.rule4(self.pag, 3,4,5,1, sepset)
        assert(self.pag.has_directed_edge(4,5) and self.pag.has_directed_edge(5,4) and self.pag.has_directed_edge(4,3) and self.pag.has_directed_edge(3,4))

    # Rule 5 Tests
    def test51(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(1,3)
        self.pag.add_edge(3,4)
        self.pag.add_edge(2,4)
        FCIAlg.rule5(self.pag, 1,2,3,4)
        assert(self.pag.has_fully_undirected_edge(1,2) and self.pag.has_fully_undirected_edge(1,3) and self.pag.has_fully_undirected_edge(3,4) and self.pag.has_fully_undirected_edge(4,2))
    
    def test52(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(1,3)
        self.pag.add_edge(2,4)
        FCIAlg.rule5(self.pag, 1,2,3,4)
        assert(not( self.pag.has_fully_undirected_edge(1,2) and self.pag.has_fully_undirected_edge(1,3) and self.pag.has_fully_undirected_edge(3,4) and self.pag.has_fully_undirected_edge(4,2)))

    def test53(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(1,3)
        self.pag.add_edge(3,4)
        FCIAlg.rule5(self.pag, 1,2,3,4)
        assert(not(self.pag.has_fully_undirected_edge(1,2) and self.pag.has_fully_undirected_edge(1,3) and self.pag.has_fully_undirected_edge(3,4) and self.pag.has_fully_undirected_edge(4,2)))

    def test54(self):
        self.pag.add_edge(1,5)
        self.pag.add_edge(1,2)
        self.pag.add_edge(1,3)
        self.pag.add_edge(3,4)
        self.pag.add_edge(2,4)
        FCIAlg.rule5(self.pag, 1,2,3,4)
        assert(self.pag.has_fully_undirected_edge(1,2) and self.pag.has_fully_undirected_edge(1,3) and self.pag.has_fully_undirected_edge(3,4) and self.pag.has_fully_undirected_edge(4,2))



    # Rule 6 Tests
    def test61(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.undirect_edge(1,2)
        FCIAlg.rule67(self.pag,1,2,3)
        assert(self.pag.get_edge_data(2,3)[2] == '-')
    
    def test62(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        FCIAlg.rule67(self.pag,1,2,3)
        assert(not (self.pag.get_edge_data(2,3)[2] == '-'))

    def test63(self):
        self.pag.add_edge(2,3)
        self.pag.undirect_edge(1,2)
        FCIAlg.rule67(self.pag,1,2,3)
        assert(not (self.pag.get_edge_data(2,3)[2] == '-'))
    
    # Rule 7 Tests
    def test71(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.setTag([1,2],1,'-')
        FCIAlg.rule67(self.pag,1,2,3)
        assert(self.pag.get_edge_data(2,3)[2] == '-')

    def test72(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        FCIAlg.rule67(self.pag,1,2,3)
        assert(not (self.pag.get_edge_data(2,3)[2] == '-'))

    # Rule 8 Tests
    def test81(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(1,3)
        self.pag.direct_edge(1,3)
        self.pag.fully_direct_edge(1,2)
        self.pag.fully_direct_edge(2,3)
        FCIAlg.rule8(self.pag,1,2,3)
        assert(self.pag.has_fully_directed_edge(1,3))

    def test82(self):
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(1,3)
        self.pag.direct_edge(1,3)
        self.pag.setTag([1,2],1,'-')
        self.pag.fully_direct_edge(2,3)
        FCIAlg.rule8(self.pag,1,2,3)
        assert(self.pag.has_fully_directed_edge(1,3))

    # Rule 9 Tests
    def test91(self):
        self.pag.add_edge(1,3)
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,4)
        self.pag.add_edge(4,3)
        self.pag.direct_edge(1,3)
        self.pag.direct_edge(1,2)
        FCIAlg.rule9(self.pag,1,2,3,4)
        assert(self.pag.has_fully_directed_edge(1,3))

    def test92(self):
        self.pag.add_edge(1,3)
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,4)
        self.pag.add_edge(4,3)
        self.pag.direct_edge(1,3)
        self.pag.undirect_edge(1,2)
        FCIAlg.rule9(self.pag,1,2,3,4)
        assert(not self.pag.has_fully_directed_edge(1,3))

    def test93(self):
        self.pag.add_edge(1,3)
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,4)
        self.pag.add_edge(4,3)
        self.pag.direct_edge(1,3)
        self.pag.direct_edge(2,1)
        FCIAlg.rule9(self.pag,1,2,3,4)
        assert(not self.pag.has_fully_directed_edge(1,3))

    # Rule 10 Tests
    def test101(self):
        self.pag.add_edge(1,3)
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(4,3)
        self.pag.add_edge(1,5)
        self.pag.add_edge(5,4)
        self.pag.direct_edge(1,3)
        self.pag.fully_direct_edge(2,3)
        self.pag.direct_edge(1,5)
        self.pag.fully_direct_edge(4,3)
        FCIAlg.rule10(self.pag,1,2,3,4)
        assert(self.pag.has_fully_directed_edge(1,3))

    def test102(self):
        self.pag.add_edge(1,3)
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(4,3)
        self.pag.add_edge(1,5)
        self.pag.add_edge(5,4)
        self.pag.fully_direct_edge(2,3)
        self.pag.direct_edge(1,5)
        self.pag.fully_direct_edge(4,3)
        FCIAlg.rule10(self.pag,1,2,3,4)
        assert(not (self.pag.has_fully_directed_edge(1,3)))

    def test103(self):
        self.pag.add_edge(1,3)
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(4,3)
        self.pag.add_edge(1,5)
        self.pag.direct_edge(1,3)
        self.pag.direct_edge(1,5)
        self.pag.fully_direct_edge(4,3)
        FCIAlg.rule10(self.pag,1,2,3,4)
        assert(not (self.pag.has_fully_directed_edge(1,3)))

    def test104(self):
        self.pag.add_edge(1,3)
        self.pag.add_edge(1,2)
        self.pag.add_edge(2,3)
        self.pag.add_edge(4,3)
        self.pag.add_edge(1,5)
        self.pag.direct_edge(1,3)
        self.pag.fully_direct_edge(2,3)
        self.pag.direct_edge(1,5)
        self.pag.fully_direct_edge(4,3)
        FCIAlg.rule10(self.pag,1,2,3,4)
        assert(not (self.pag.has_fully_directed_edge(1,3)))


if __name__ == '__main__':
    unittest.main()