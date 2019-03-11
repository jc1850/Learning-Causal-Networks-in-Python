import networkx as nx

class PDAG(nx.DiGraph):
    
    def add_edge(self, u,v, directed = True):
        super().add_edge(u,v)
        if not directed:
            super().add_edge(v,u)
    
    def remove_edge(self, u,v):
        super().remove_edge(u,v)
        if super().has_edge(v,u):
            super().remove_edge(v,u)

    def has_directed_edge(self,u,v):
        return super().has_edge(u,v) and not super().has_edge(v,u)

    
class PAG(nx.Graph):
    def add_edge(self, u,v, utag = 'o', vtag = 'o'):
        super().add_edges_from([(u,v, {u:utag, v:vtag})])
    

    def has_edge(self, u,v):
        if super().has_edge(u,v):
            tags = super().get_edge_data(u,v)
            if tags[v] != '-':
                return True
    
    def has_undirected_edge(self, u,v):
        if super().has_edge(u,v):
            return True

    def add_edges_from(self, bunch):
        for edge in bunch:
            super().add_edges_from([(*(edge), {edge[0]:'o', edge[1]:'o'})])

    def setTag(self, edge, node, tag):
        self.edges[edge][node] = tag
