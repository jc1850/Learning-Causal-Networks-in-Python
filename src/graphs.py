import networkx as nx

class PDAG(nx.DiGraph):
    """

    """
    def add_edge(self, u,v, directed = True):
        """

        """
        super().add_edge(u,v)
        if not directed:
            super().add_edge(v,u)
    
    def remove_edge(self, u,v):
        """

        """
        super().remove_edge(u,v)
        if super().has_edge(v,u):
            super().remove_edge(v,u)

    def has_directed_edge(self,u,v):
        """

        """
        return super().has_edge(u,v) and not super().has_edge(v,u)

    
class PAG(nx.Graph):
    """

    """

    def __init__(self, incoming_data=None, **kwds):
        """

        """ 
        super().__init__(incoming_data, **kwds)
        self.non_colliders = []

    def add_edge(self, u,v, utag = 'o', vtag = 'o'):
        """

        """ 
        super().add_edges_from([(u,v, {u:utag, v:vtag})])
    
    
    def has_directed_edge(self, u,v):
        """

        """
        if super().has_edge(u,v):
            tags = super().get_edge_data(u,v)
            if tags[v] == '>':
                return True
            else:
                return False
        else:
            return False

    def has_fully_directed_edge(self, u,v):
        """

        """
        if super().has_edge(u,v):
            tags = super().get_edge_data(u,v)
            if tags[u] == '-' and tags[v] == '>':
                return True
            else:
                return False
        else:
            return False

    def add_edges_from(self, bunch):
        """

        """
        for edge in bunch:
            super().add_edges_from([(*(edge), {edge[0]:'o', edge[1]:'o'})])

    def setTag(self, edge, node, tag):
        """

        """
        if super().has_edge(*edge):
            self.edges[edge][node] = tag
    
    def direct_edge(self, u,v):
        """

        """
        if super().has_edge(u,v):
            self.edges[(u,v)][v] = '>'

    def fully_direct_edge(self, u,v):
        """

        """
        if super().has_edge(u,v):
            self.edges[(u,v)][v] = '>'
            self.edges[(u,v)][u] = '-'

    def undirect_edge(self, u,v):
        """

        """
        if super().has_edge(u,v):
            self.edges[(u,v)][v] = '-'
            self.edges[(u,v)][u] = '-'    

    def hasDiscPath(self,u, v, b):
        """

        """
        all_paths = nx.all_simple_paths(self, u, v)
        discpath = False
        for path in all_paths:
            if b in path:
                b_pred  = (path.index(v) - path.index(b)) == 1 and self.has_directed_edge(b,v)
                all_colliders = True
                for node in path[1:-1]:
                    prev = path[path.index(node)-1]
                    suc = path[path.index(node)+1]
                    if (node != b) and not ((self.has_directed_edge(prev,node)) and (self.has_directed_edge(suc,node))):
                        all_colliders = False
                all_pred = True
                for node in path[1:-1]:
                    if not (self.has_fully_directed_edge(node, v)):
                        all_pred = False
                nonadj = not self.has_edge(u,v)
                discpath = discpath or (b_pred and all_colliders and all_pred and nonadj)
        return discpath

    def findDiscPath(self,u,v,b):
        """

        """
        all_paths = nx.all_simple_paths(self, u, v)
        discpaths = []
        for path in all_paths:
            if b in path:
                b_pred  = (path.index(v) - path.index(b)) == 1 and self.has_directed_edge(b,v)
                all_colliders = True
                for node in path[1:-1]:
                    prev = path[path.index(node)-1]
                    suc = path[path.index(node)+1]
                    if (node != b) and not ((self.has_directed_edge(prev,node)) and (self.has_directed_edge(suc,node))):
                        all_colliders = False
                all_pred = True
                for node in path[1:-1]:
                    if not (self.has_fully_directed_edge(node, v)):
                        all_pred = False
                nonadj = not self.has_edge(u,v)
                if (b_pred and all_colliders and all_pred and nonadj):
                    discpaths.append(path)
        return discpaths
    
    def has_o(self,u,v,side):
        cond = False
        if self.has_edge(u,v):
            if self[u][v][side] == 'o':
                cond = True
        return cond


    def isUncovered(self, path):
        for x in range(1,len(path)-1):
            pred = path[x-1]
            suc = path[x+1]
            if self.has_edge(pred,suc):
                return False
        return True

    def isPD(self, path):
        for x in range(len(path)-1):
            node = path[x]
            suc = path[x+1]
            edge = self.get_edge_data(node,suc)
            if (edge[suc] == '-' or edge[node] == '<'):
                return False
        return True