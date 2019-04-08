import networkx as nx 
from graphs import PAG
from algorithms import GraphLearner
import itertools
from indepTests import chi
import copy
import sys

class FCIAlg(GraphLearner):
    """

    """

    def orientEdges(self, skeleton, sepSet):
        """
        A function to orient the edges of a skeleton using the orientation rules of the FCI algorithm
        Parameters
        ----------
            skeleton: networkx Graph(),
                skeleton estimation
            sepSet: dict
                Dicitonary containg separation sets of all pairs of nodes

        Returns
        -------
            PAG containing estimated causal relationships in data

        """
        pag = PAG()
        pag.add_nodes_from(skeleton)
        pag.add_edges_from(skeleton.edges)
        self.orient_V(pag, sepSet)
        old_pag = nx.DiGraph()
        while old_pag.edges != pag.edges:
            old_pag = copy.deepcopy(pag)
            for i in pag:
                for j in pag:
                    for k in pag:
                        if  k not in [i,j] and j != i:
                            self.rule1(pag,i,j,k)
                            self.rule2(pag,i,j,k)
                            for l in pag:
                                if l not in [i,j,k]:
                                    self.rule3(pag,i,j,k,l)
                                    self.rule4(pag,i,j,k,l, sepSet)
                                    self.rule5(pag,i,j,k,l)
                                    self.rule67(pag,i,j,k)
                                    self.rule8(pag,i,j,k)
                                    self.rule9(pag,i,j,k,l)
                                    self.rule10(pag,i,j,k,l)
        return pag

    def learnSkeleton(self):
        """ A  function to build the skeleton of a causal graph from data
        
        Returns
        -------
            PDAG
                The skeleton of the causal network
            dict
                Dicitonary containg separation sets of all pairs of nodes

        """ 
        
        skeleton, sepSet = super().learnSkeleton()
        pag = PAG()
        pag.add_nodes_from(skeleton)
        pag.add_edges_from(skeleton.edges)
        print('finalising skeleton')
        self.orient_V(pag, sepSet)
        dseps = self.possible_d_seps( pag)
        pag.write_to_file('tmp')
        print(dseps)
        for x in pag:
            for y in pag:
                if y in pag.neighbors(x):
                    indep = False
                    for i in range(1,len(dseps[x])+1):
                        for dsepset in itertools.combinations(dseps[x],i):
                            indep = False
                            dsepset = list(dsepset)
                            if y in dsepset:
                                dsepset.remove(y)
                            if len(dsepset )>= 1:
                                print('testing {} indep {} given {}'.format(x,y,dsepset) )
                                p, *_ = self.indep_test(self.data, x, y, dsepset)
                                indep = p > self.alpha
                                #stop testing if independence is found and remove edge
                                if indep:
                                    print('removing edge {},{}'.format(x,y))
                                    pag.remove_edge(x,y)
                                    sepSet[(x,y)] = dsepset
                                    sepSet[(y,x)] = dsepset
                                    break
                        if indep:
                            break
                    if indep:
                        break
        return pag, sepSet




    def orient_V(self, pag, sepSet):
        """
        A function to orient the colliders in a PAG
            
        Parameters
        ----------
            pag: PAG
                PAG to be oriented
            sepSet: dict
                separation d#sets of all pairs of nodes in PAG
        Returns
        -------
            PAG
                PAG with v-structures oriented
            

        """
        for i in pag:
            for j in pag:
                if j != i:
                    for k in pag:
                        if k not in [i,j]:
                            if pag.has_edge(i,j) and pag.has_edge(k,j) and not pag.has_edge(i,k):
                                if j not in sepSet[(i,k)]:
                                    pag.direct_edge(i,j)
                                    pag.direct_edge(k,j)
                                    print('Orienting collider {}, {}, {}'.format(i,j,k))
    
    def learnGraph(self):
        """
        function to learn a causal netwoork from data

        Returns
        -------
        PAG
            causal network learned from data
        """
        print('Learning Skeleton of graph...')
        skeleton, sepset = self.learnSkeleton()
        print('...Skeleton learnt')
        print('Orienting Edges...')
        pag = self.orientEdges(skeleton, sepset)
        print('...Learning complete')
        return pag

    @staticmethod
    def is_possible_d_sep(X,Y, pag):
        """

        """
        all_paths = nx.all_simple_paths(pag,X,Y)
        for path in all_paths:
            path_sep = True
            for i in range(1, len(path[:-1])):
                collider = (pag.has_directed_edge(path[i-1],path[i]) and pag.has_directed_edge(path[i+1],path[i]))
                triangle = (pag.has_edge(path[i-1],path[i]) and pag.has_edge(path[i+1],path[i]) and pag.has_edge(path[i-1],path[i+1]))
                if not(collider or triangle):
                    path_sep = False
            if path_sep:
                return True
        return False

    @staticmethod
    def possible_d_seps(pag):
        """

        """
        dseps = {}
        for i in pag:
            dseps[i] = []
            for j in pag:
                if i != j:
                    if FCIAlg.is_possible_d_sep(i,j,pag):
                        dseps[i].append(j)
        return dseps
    
    @staticmethod
    def hasDirectedPath(pag, X, Y):
        """

        """
        all_paths = nx.all_simple_paths(pag,X,Y)
        any_directed = False
        for path in all_paths:
            directed = True
            for i in range(1, len(path[1:])+1):
                if not pag.has_directed_edge(path[i-1],path[i]):
                    directed = False
            any_directed = any_directed or directed
        return any_directed

    @staticmethod
    def rule1(pag,i,j,k):
        if pag.has_directed_edge(i,j) and pag.has_o(j,k,j) and not pag.has_edge(i,k):
            pag.fully_direct_edge(j,k)
            print('Orienting edge {},{} with rule 1'.format(j,k))
        
    @staticmethod
    def rule2(pag,i,j,k):
        chain1 = pag.has_fully_directed_edge(i,j) and pag.has_directed_edge(j,k)
        chain2 = pag.has_fully_directed_edge(j,k) and pag.has_directed_edge(i,j)
        if (chain1 or chain2) and pag.has_o(i,k,k):
            pag.direct_edge(i,k)
            print('Orienting edge {},{} with rule 2'.format(i,k))
            
    @staticmethod
    def rule3(pag,i,j,k,l):
        chain1 = (pag.has_directed_edge(i,j)) and pag.has_directed_edge(k,j)
        chain2 = (pag.has_o(i,l,l)) and (pag.has_o(k,l,l))
        if chain1 and chain2 and not pag.has_edge(i,k) and pag.has_o(l,j,j):
            pag.direct_edge(l,j)
            print('Orienting edge {},{} with rule 3'.format(l,j))

    @staticmethod
    def rule4(pag,i,j,k,l, sepSet):
        paths = pag.findDiscPath(l,k,j)
        for path in paths:
            if i in path:
                if path.index(i) == len(path)-3 and  pag.has_o(j,k,j) :
                    if j in sepSet[(l,k)]:
                        pag.fully_direct_edge(j,k)
                        print('Orienting edge {},{} with rule 4'.format(j,k))

                    else:
                        pag.direct_edge(i,j)
                        pag.direct_edge(j,k)
                        pag.direct_edge(j,i)
                        pag.direct_edge(k,j)    
                        print('Orienting edges {},{}, {},{} with rule 4'.format(i,j,j,k))

    
    @staticmethod
    def rule5(pag,i,j,k,l):
        for path in pag.findUncoveredCirclePaths(i,j):
            edge = pag.has_o(i,j,j) and pag.has_o(i,j,j)
            on_path = False
            if l in path and k in path:
                on_path = path.index(k) == 1 and path.index(l) == (len(path) - 2)
            nonadj = not pag.has_edge(i,l) and not pag.has_edge(k,j)
            if edge and on_path and nonadj:
                pag.undirect_edge(i,j)
                print('Orienting edge {},{} with rule 5'.format(i,j))
                for x in range(len(path)-1):
                    pag.undirect_edge(path[x], path[x+1])
                    print('Orienting edge {},{} with rule 5'.format(path[x], path[x+1]))
    
    @staticmethod
    def rule67(pag,i,j,k):
        if pag.has_edge(i,j) and pag.has_edge(j,k):
            edge1 = pag.get_edge_data(i,j)
            edge2 = pag.get_edge_data(j,k)
            if edge1[i] == '-' and edge1[j] == '-' and edge2[j] == 'o':
                pag.setTag([j,k],j,'-')
                print('Orienting edge {},{} with rule 6'.format(k,j))
            if edge1[i] == '-' and edge1[j] == 'o' and edge2[j] == 'o' and not pag.has_edge(i,k):
                pag.setTag([j,k],j,'-')
                print('Orienting edge {},{} with rule 7'.format(k,j))

    
    @staticmethod
    def rule8(pag,i,j,k):
        chain1 = pag.has_fully_directed_edge(i,j) and pag.has_fully_directed_edge(j,k)#
        chain2 = False
        edge = False
        if pag.has_edge(i,j) and pag.has_edge(i,k):
            chain2 = pag.has_directed_edge(j,k) and pag.get_edge_data(i,j)[j] == 'o' and pag.get_edge_data(i,j)[i] == '-'
            edge =  pag.get_edge_data(i,k)[i] == 'o' and pag.has_directed_edge(i,k)
        if chain1 or chain2 and edge:
            pag.fully_direct_edge(i,k)
            print('Orienting edge {},{} with rule 8'.format(k,i))
        
    @staticmethod
    def rule9(pag,i,j,k,l):
        if pag.has_directed_edge(i,k) and pag.has_o(i,k,i):
            for path in nx.all_simple_paths(pag,i,k):
                if pag.isUncovered(path) and pag.isPD(path):
                    if path[1] == j and path[2] == l and not pag.has_edge(j,k):
                        pag.fully_direct_edge(i,k)
                        print('Orienting edge {},{} with rule 9'.format(k,i))
                        break

    @staticmethod
    def rule10(pag,i,j,k,l):
        if pag.has_directed_edge(i,k) and pag.has_o(i,k,i):
            if pag.has_fully_directed_edge(j,k) and pag.has_fully_directed_edge(l,k):
                for path1 in nx.all_simple_paths(pag,i,j):
                    for path2 in nx.all_simple_paths(pag,i,l):
                        if pag.isUncovered(path1) and pag.isPD(path1) and pag.isUncovered(path2) and pag.isPD(path2):
                            if path1[1] != path2[1] and not pag.has_edge(path1[1],path2[1]):
                                pag.fully_direct_edge(i,k) 
                                print('Orienting edge {},{} with rule 10'.format(k,i)) 






if __name__ == '__main__':
    data_path = sys.argv[1]
    data = FCIAlg.prepare_data(data_path, isLabeled=True)
    fci = FCIAlg(data, chi, 0.05)
    pag = fci.learnGraph()
    print(pag.to_matrix())
    for edge in pag.edges:
        print(pag.get_edge_data(*edge))


    
