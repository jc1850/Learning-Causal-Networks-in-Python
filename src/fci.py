import networkx as nx 
from graphs import PAG
from algorithms import GraphLearner
import itertools
from indepTests import chi
import copy

class FCIAlg(GraphLearner):

    def orientEdges(self, skeleton, sepSet):
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
        pag = PAG()
        pag.add_edges_from(skeleton.edges)
        self.orient_V_pag(pag, sepSet)
        old_pag = nx.DiGraph()
        while old_pag.edges != pag.edges:
            old_pag = copy.deepcopy(pag)
            for i in pag:
                for j in pag:
                    if self.hasDirectedPath(pag, i,j) and pag.has_edge(i,j):
                        print('1: directing edge {} , {}'.format(i,j))
                        pag.direct_edge(i,j)
                    else:
                        for k in pag:
                            for l in pag:
                                if pag.has_directed_edge(i,j) and pag.has_edge(j,k):
                                    print('2: directing edge {} , {}'.format(j,k))
                                    pag.fully_direct_edge(j,k)
                                elif pag.has_directed_edge(i,j) and pag.has_directed_edge(k,j) and pag.has_edge(j,l):
                                    print('3: directing edge {} , {}'.format(l,j))
                                    pag.direct_edge(l,j)
                                elif pag.has_directed_edge(j,i) and pag.has_fully_directed_edge(i,k) and pag.has_edge(k,j):
                                    if pag.get_edge_data(k,j)[k] == 'o':
                                        print('4: directing edge {} , {}'.format(j,k))
                                        pag.direct_edge(j,k)
                                discpaths = pag.findDiscPath(i,j,k)
                                for path in discpaths:
                                    ladj = (path.index(l) - path.index(j))^2 == 1
                                    triangle =  pag.has_edge(i,k) and pag.has_edge(i,l) and pag.has_edge(l,k)
                                    if triangle and ladj:
                                        if k in sepSet(i,j):
                                            pag.non_colliders.append({k:(l,j)})
                                        else:
                                            print('5: directing edge {} , {}'.format(l,k))
                                            print('5: directing edge {} , {}'.format(j,k))
                                            pag.direct_edge(l,k)
                                            pag.direct_edge(j,k)
        return pag

    def orient_V_pag(self, pag, sepSet):
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
        print('Learning Skeleton of graph...')
        skeleton, sepset = self.learnSkeleton()
        print('...Skeleton learnt')
        print('Orienting Edges...')
        pag = self.orientEdges(skeleton, sepset)
        print('...Learning complete')
        return pag

    @staticmethod
    def is_possible_d_sep(X,Y, skeleton, pdag):
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
        dseps = {}
        for i in skeleton:
            dseps[i] = []
            for j in skeleton:
                if FCIAlg.is_possible_d_sep(i,j,skeleton,pdag):
                    dseps[i].append(j)
        return dseps
    @staticmethod
    def hasDirectedPath(pag, X, Y):
        all_paths = nx.all_simple_paths(pag,X,Y)
        any_directed = False
        for path in all_paths:
            directed = True
            for i in range(1, len(path[1:])+1):
                if not pag.has_directed_edge(path[i-1],path[i]):
                    directed = False
            any_directed = any_directed or directed
        return any_directed






if __name__ == '__main__':
    data = FCIAlg.prepare_data('asia_1000.data', isLabeled=True)
    fci = FCIAlg(data, chi, 0.05)
    pag = fci.learnGraph()
    print(pag.edges)
    for i in pag.edges:
        print(pag.get_edge_data(*i))
    
