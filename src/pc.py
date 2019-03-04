import networkx as nx 
from graphs import PDAG
from algorithms import GraphLearner


class PCAlg(GraphLearner):
    
    
    def orientEdges(self, skeleton, sepset):
        """ A method to orient the edges of a skeleton

        Parameters
        ----------
        skeleton : networkx.Graph
        An undirected graph showing causal links to be oriented by
        the pc algorithm. Can be genertaed using the learnSkeleton 
        method.

        Returns
        -------
        PDAG
        A partially directed acyclic graph represnting a set of directed acyclic graphs.
        this graph shows independence relationships between variables.
        """
        directed = nx.DiGraph()
        directed.add_nodes_from(skeleton.nodes)
        undirected = skeleton.copy()
        self.orient_V( undirected, directed, sepset)
        old_directed = nx.DiGraph()
        while old_directed.edges != directed.edges:
            old_directed = directed.copy()
            for i in skeleton:
                for j in skeleton:
                    if i != j:
                        for k in skeleton:
                            if i != k and j != k:
                                if directed.has_edge(i,j) and not skeleton.has_edge(k,i) and undirected.has_edge(j,k):
                                    directed.add_edge(j,k)
                                    undirected.remove_edge(j,k)
                                if directed.has_edge(i,k) and directed.has_edge(k,j) and undirected.has_edge(i,j):
                                    directed.add_edge(i,j)
                                    undirected.remove_edge(i,j)
                                for l in skeleton:
                                    if l not in [i,j,k]:
                                        first_chain = undirected.has_edge(i,k) and directed.has_edge(k,j)
                                        second_chain = undirected.has_edge(i,l) and directed.has_edge(l,j)
                                        if first_chain and second_chain and not skeleton.has_edge(k,l) and undirected.has_edge(i,j):
                                            print(i,j,k,l)
                                            directed.add_edge(i,j)
                                            undirected.remove_edge(i,j)

                                        first_chain = skeleton.has_edge(i,k) and directed.has_edge(k,l)
                                        second_chain = directed.has_edge(k,l) and directed.has_edge(l,j)
                                        if first_chain and second_chain and not skeleton.has_edge(k,l) and undirected.has_edge(i,j):                
                                            directed.add_edge(i,j)
                                            undirected.remove_edge(i,j)
        #generate PDAG
        pdag = self.pdag_union(directed, undirected)
        return pdag
    
    
    def orient_V(self, undirected, directed, sepset):
        """
        A method to orient all "V-structures" in a graph

        Parameters
        ----------
        undirected:
        """
        skeleton = undirected.copy()
        for i in undirected:
            for j in undirected:
                if i != j:
                    for k in undirected:
                        if i != k and j != k:
                            if skeleton.has_edge(i,k) and skeleton.has_edge(k,j) and not skeleton.has_edge(i,j) and k not in sepset[(i,j)]:
                                directed.add_edge(j,k)
                                if undirected.has_edge(j,k):
                                    undirected.remove_edge(j,k)
                                directed.add_edge(i,k)
                                if undirected.has_edge(i,k):
                                    undirected.remove_edge(i,k)
    
    
    def pdag_union(self, directed, undirected):
        """
        A method to orient all "V-structures" in a graph

        Parameters
        ----------
        undirected:
        """
        pdag = PDAG()
        for edge in directed.edges:
            pdag.add_edge(*edge)
        for edge in undirected.edges:
            pdag.add_edge(*edge, False)
        return pdag
    
    
    def learnGraph(self):
        print('Learning Skeleton of graph...')
        skeleton, sepset = self.learnSkeleton()
        print('...Skeleton learnt')
        print('Orienting Edges...')
        pdag = self.orientEdges(skeleton, sepset)
        print('...Learning complete')
        return pdag
    
    