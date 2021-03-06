import networkx as nx 
from graphs import PDAG
from algorithms import GraphLearner
from indepTests import chi
import sys

class PCAlg(GraphLearner):
    """
    A graph learner which implements the PC algorithm
    """
    
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
                                if PCAlg.findPath(i,j, directed, []) and undirected.has_edge(i,j):
                                    directed.add_edge(i,j)
                                    undirected.remove_edge(i,j)
        #generate PDAG
        pdag = self.pdag_union(directed, undirected)
        return pdag
        
    def learnGraph(self):
        """
        function to learn a causal network from data

        Returns
        -------
        PDAG
            causal network learned from data
        """
        print('Learning Skeleton of graph...')
        skeleton, sepset = self.learnSkeleton()
        print('...Skeleton learnt')
        print('Orienting Edges...')
        pdag = self.orientEdges(skeleton, sepset)
        print('...Learning complete')
        return pdag
    
    def pdag_union(self, directed, undirected):
        """
        A method to orient all "V-structures" in a graph

        Parameters
        ----------
        undirected: nx.Graph
            graph containing the undirected edges
        directed: nx.DiGraph
            graph containing the directed edges

        Returns
        -------
            PDAG
                a graph containing all edges from the two graphs
        """
        pdag = PDAG()
        for edge in directed.edges:
            pdag.add_edge(*edge)
        for edge in undirected.edges:
            pdag.add_edge(*edge, False)
        return pdag

    
if __name__ == '__main__':
    data_path = sys.argv[1]
    if len(sys.argv) == 4:
        if sys.argv[3] == 'space':
            sys.argv[3] = ' '
        delimeator = sys.argv[3]
        labeled = sys.argv[2] == 'True'
    elif len(sys.argv) == 3:
        delimeator = ' '
        labeled = sys.argv[2] == 'True'
    else:
        delimeator = ' '
        labeled = True
    data = PCAlg.prepare_data(data_path, isLabeled=labeled, delim = delimeator)
    pc = PCAlg(data, chi, 0.05)
    pdag = pc.learnGraph()
    pdag.write_to_file('adjmat')


    