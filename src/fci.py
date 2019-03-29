import networkx as nx 
from graphs import PAG
from algorithms import GraphLearner
import itertools
from indepTests import chi
import copy

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
        pag.add_edges_from(skeleton.edges)
        self.orient_V_pag(pag, sepSet)
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
                                self.rule3(pag,i,j,k,l)
                                self.rule4(pag,i,j,k,l, sepSet)
                                self.rule5(pag,i,j,k,l)
                                self.rule67(pag,i,j,k,l)
                                self.rule8(pag,i,j,k,l)
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
        directed = nx.DiGraph()
        directed.add_nodes_from(skeleton.nodes)
        undirected = skeleton.copy()
        self.orient_V(undirected, directed, sepSet)
        pdag = self.pdag_union(directed, undirected)
        dseps = self.possible_d_seps(skeleton, pdag)
        for x in skeleton:
            for y in skeleton.neighbors(x):
                for i in range(len(dseps[x])):
                    for dsepset in itertools.combinations(dseps[x],i):
                        dsepset = list(dsepset)
                        if y in dsepset:
                            dsepset.remove(y)
                        p, *_ = self.indep_test(self.data, x, y, dsepset)
                        indep = p > self.alpha
                        #stop testing if independence is found and remove edge
                        if indep:
                            print('removing edge {},{}'.format(x,y))
                            skeleton.remove_edge(x,y)
                            sepSet[(x,y)] = dsepset
                            sepSet[(y,x)] = dsepset
                            break
                    if indep:
                        break
                    for dsepset in itertools.combinations(dseps[y],i):
                        dsepset = list(dsepset)
                        if x in dsepset:
                            dsepset.remove(x)
                        p, *_ = self.indep_test(self.data, x, y, dsepset)
                        indep = p > self.alpha
                        #stop testing if independence is found and remove edge
                        if indep:
                            print('removing edge {},{}'.format(x,y))
                            skeleton.remove_edge(x,y)
                            sepSet[(x,y)] = dsepset
                            sepSet[(y,x)] = dsepset
                            break
                    if indep:
                        break
        return skeleton, sepSet




    def orient_V_pag(self, pag, sepSet):
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
    def is_possible_d_sep(X,Y, skeleton, pdag):
        """

        """
        all_paths = nx.all_simple_paths(skeleton,X,Y)
        d_sep = False
        for path in all_paths:
            path_sep = True
            for i in range(1, len(path[1:])):
                collider = (pdag.has_directed_edge(path[i-1],path[i]) and pdag.has_directed_edge(path[i+1],path[i]))
                triangle = (skeleton.has_edge(path[i-1],path[i]) and skeleton.has_edge(path[i+1],path[i]) and skeleton.has_edge(path[i-1],path[i+1]))
                if not(collider) and not(triangle):
                    path_sep = False
            d_sep = d_sep or path_sep
        return d_sep

    @staticmethod
    def possible_d_seps(skeleton, pdag):
        """

        """
        dseps = {}
        for i in skeleton:
            dseps[i] = []
            for j in skeleton:
                if FCIAlg.is_possible_d_sep(i,j,skeleton,pdag):
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
        
    @staticmethod
    def rule2(pag,i,j,k):
        chain1 = pag.has_fully_directed_edge(i,j) and pag.has_directed_edge(j,k)
        chain2 = pag.has_fully_directed_edge(j,k) and pag.has_directed_edge(i,j)
        if (chain1 or chain2) and pag.has_o(i,k,k):
            pag.direct_edge(i,k)
            
    @staticmethod
    def rule3(pag,i,j,k,l):
        chain1 = (pag.has_directed_edge(i,j)) and pag.has_directed_edge(k,j)
        chain2 = (pag.has_o(i,l,l)) and (pag.has_o(k,l,l))
        if chain1 and chain2 and not pag.has_edge(i,k) and pag.has_o(l,j,j):
            pag.direct_edge(l,j)

    @staticmethod
    def rule4(pag,i,j,k,l, sepSet):
        if pag.hasDiscPath(l,k,j):
            paths = pag.findDiscPath(l,k,j)
            for path in paths:
                if i in path:
                    if path.index(i) == len(path)-3 and  pag.has_o(j,k,j) :
                        if j in sepSet(l,k):
                            pag.fully_direct_edge(i,k)
                        else:
                            pag.direct_edge(i,j)
                            pag.direct_edge(j,k)
                            pag.direct_edge(j,i)
                            pag.direct_edge(k,j)    
    
    @staticmethod
    def rule5(pag,i,j,k,l):
        for path in nx.all_simple_paths(pag, i,j):
            uncovered_circle = True
            for x in range(1,len(path)-1):
                pred = path[x-1]
                suc = path[x+1]
                node = path[x]
                if pag.has_edge(pred,suc):
                    uncovered_circle = False
                edge1_data = pag.get_edge_data(pred,node)
                edge2_data = pag.get_edge_data(suc,node)
                if not (edge1_data[node] == 'o' and edge1_data[pred] == 'o'):
                    uncovered_circle = False
                if not (edge2_data[node] == 'o' and edge2_data[suc] == 'o'):
                    uncovered_circle = False
            if uncovered_circle:
                edge = pag.has_o(i,j,j) and pag.has_o(i,j,j)
                on_path = False
                if l in path and k in path:
                    print(path.index(k))
                    on_path = path.index(k) == 1 and path.index(l) == (len(path) - 2)
                nonadj = not pag.has_edge(i,l) and not pag.has_edge(k,j)
                if edge and on_path and nonadj:
                    pag.undirect_edge(i,j)
                    for x in range(len(path)-1):
                        pag.undirect_edge(path[x], path[x+1])
    
    @staticmethod
    def rule67(pag,i,j,k,l):
        if pag.has_edge(i,j) and pag.has_edge(j,k):
            edge1 = pag.get_edge_data(i,j)
            edge2 = pag.get_edge_data(j,k)
            if edge1[i] == '-' and edge1[j] == '-' and edge2[j] == 'o':
                pag.setTag([j,k],j,'-')
            if edge1[i] == '-' and edge1[j] == 'o' and edge2[j] == 'o' and not pag.has_edge(i,k):
                pag.setTag([j,k],j,'-')

    
    @staticmethod
    def rule8(pag,i,j,k,l):
        chain1 = pag.has_fully_directed_edge(i,j) and pag.has_directed_edge(j,k)#
        chain2 = False
        edge = False
        if pag.has_edge(i,j) and pag.has_edge(i,k):
            chain2 = pag.has_directed_edge(j,k) and pag.get_edge_data(i,j)[j] == 'o' and pag.get_edge_data(i,j)[i] == '-'
            edge =  pag.get_edge_data(i,k)[i] == 'o' and pag.has_directed_edge(i,k)
        if chain1 or chain2 and edge:
            pag.fully_direct_edge(i,k)
        
    @staticmethod
    def rule9(pag,i,j,k,l):
        if pag.has_directed_edge(i,k) and pag.has_o(i,k,i):
            for path in nx.all_simple_paths(pag,i,k):
                if pag.isUncovered(path) and pag.isPD(path):
                    if path[1] == j and not pag.has_edge(j,k):
                        pag.fully_direct_edge(i,k)
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






if __name__ == '__main__':
    data = FCIAlg.prepare_data('asia_1000.data', isLabeled=True)
    fci = FCIAlg(data, chi, 0.05)
    pag = fci.learnGraph()
    print(pag.edges)
    for i in pag.edges:
        print(pag.get_edge_data(*i))


    
