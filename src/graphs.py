import networkx as nx

class PDAG(nx.DiGraph):
    
    def add_edge(self, u,v, directed = True):
        super().add_edge(u,v)
        if not directed:
            super().add_edge(v,u)
    
