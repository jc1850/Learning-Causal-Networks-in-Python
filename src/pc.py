import networkx as nx 
from graphs import PDAG
from algorithms import GraphLearner
from indepTests import chi


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
                                if PCAlg.findPath(i,j, directed, []) and undirected.has_edge(i,j):
                                    directed.add_edge(i,j)
                                    undirected.remove_edge(i,j)
        #generate PDAG
        pdag = self.pdag_union(directed, undirected)
        return pdag
    
    
    
    
    def learnGraph(self):
        print('Learning Skeleton of graph...')
        skeleton, sepset = self.learnSkeleton()
        print('...Skeleton learnt')
        print('Orienting Edges...')
        pdag = self.orientEdges(skeleton, sepset)
        print('...Learning complete')
        return pdag
    
if __name__ == '__main__':
    data = PCAlg.prepare_data('alarm_10000.dat', isLabeled=True)
    pc = PCAlg(data, chi, 0.05)
    print(len([('KINKEDTUBE', 'PRESS'), ('INTUBATION', 'MINVOL'), ('INTUBATION', 'VENTLUNG'), ('INTUBATION', 'VENTALV'), ('MINVOL', 'EXPCO2'), ('MINVOL', 'VENTLUNG'), ('VENTMACH', 'VENTTUBE'), ('VENTMACH', 'MINVOLSET'), ('VENTTUBE', 'PRESS'), ('DISCONNECT', 'VENTTUBE'), ('VENTLUNG', 'EXPCO2'), ('VENTLUNG', 'INTUBATION'), ('VENTLUNG', 'VENTALV'), ('VENTLUNG', 'MINVOL'), ('SHUNT', 'SAO2'), ('SHUNT', 'PULMEMBOLUS'), ('VENTALV', 'PVSAT'), ('VENTALV', 'INTUBATION'), ('VENTALV', 'VENTLUNG'), ('VENTALV', 'ARTCO2'), ('PVSAT', 'SAO2'), ('FIO2', 'PVSAT'), ('ARTCO2', 'EXPCO2'), ('ARTCO2', 'CATECHOL'), ('ARTCO2', 'VENTALV'), ('CATECHOL', 'HRSAT'), ('CATECHOL', 'HR'), ('TPR', 'CATECHOL'), ('TPR', 'BP'), ('TPR', 'ANAPHYLAXIS'), ('HR', 'HREKG'), ('HR', 'HRSAT'), ('HR', 'CO'), ('HR', 'HRBP'),
('CO', 'BP'), ('ERRCAUTER', 'HRSAT'), ('ERRCAUTER', 'HREKG'), ('HYPOVOLEMIA', 'LVEDVOLUME'), ('HYPOVOLEMIA', 'STROKEVOLUME'), ('LVEDVOLUME', 'CVP'), ('LVEDVOLUME', 'PCWP'), ('STROKEVOLUME', 'CO'), ('LVFAILURE', 'LVEDVOLUME'), ('LVFAILURE', 'STROKEVOLUME'), ('LVFAILURE', 'HISTORY'), ('CVP', 'PCWP'), ('PCWP', 'CVP'), ('ERRLOWOUTPUT', 'HRBP'), ('PULMEMBOLUS', 'PAP'), ('PULMEMBOLUS', 'SHUNT'), ('PAP', 'PULMEMBOLUS'), ('MINVOLSET', 'VENTMACH'), ('ANAPHYLAXIS', 'TPR'), ('HISTORY', 'LVFAILURE')]))

