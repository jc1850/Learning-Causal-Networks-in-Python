import networkx as nx 
from graphs import PAG
from algorithms import GraphLearner
import itertools

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
        pag.add_edges_from(skeleton)
        self.orient_V_pag(pag, sepSet)
        old_pag = nx.DiGraph()
        while old_pag.edges != pag.edges:
            old_pag = pag.copy()
            



    def orient_V_pag(self, pag, sepSet):
        for i in pag:
            for j in pag:
                if j != i:
                    for k in pag:
                        if k not in [i,j]:
                            if pag.has_undirected_edge(i,j) and pag.has_undirected_edge(k,j) and not pag.has_undirected_edge(i,k):
                                if j not in sepSet[(i,k)]:
                                    if pag.get_edge_data(i,j)[j] == 'o' and  pag.get_edge_data(k,j)[j] == 'o':
                                        pag.setTag((i,j),j,'>')
                                        pag.setTag((k,j),j,'>')

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








