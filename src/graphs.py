import networkx as nx
import numpy as np

class PDAG(nx.DiGraph):
    """
    A class implementaing a graph which can have both directed and undirected edges
    """
    def add_edge(self, u,v, directed = True):
        """
        A method to add an edge to a graph
        
        Parameters
        ----------
        u : str
            the from node of an edge
        v: str
            the to node of an edge
        directed: bool, optional 
            determines whether an edge is directed (True) or not (False)
        """
        super().add_edge(u,v)
        if not directed:
            super().add_edge(v,u)
    
    def remove_edge(self, u,v):
        """
        A method to remove an edge from the graph
        
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge

        """
        super().remove_edge(u,v)
        if super().has_edge(v,u):
            super().remove_edge(v,u)

    def has_directed_edge(self,u,v):
        """
        A method to check the graph for a directed edge
       
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge

        Returns
        ------- 
        bool
            True if has directed edge, false if not

        """
        return super().has_edge(u,v) and not super().has_edge(v,u)
    
    def to_matrix(self):
        """
        A method to generate the adjacency matrix of the graph
        
        Returns
        ----------
        numpy.ndarray
            a 2d array containing the adjacency matrix of the graph

        """
        labels = [node for node in self]
        mat = np.zeros((len(labels), (len(labels))))
        for x in labels:
            for y in labels:
                if self.has_edge(x,y):
                    mat[labels.index(x)][labels.index(y)] = 1
        return mat

    def write_to_file(self, path):
        """
        A method to write the adjacency matrix of the graph to a file
        
        Parameters
        ----------
        path: str
            path to file to write adjacency matrix to

        """
        mat = self.to_matrix()
        labels = [node for node in self]
        f = open(path, 'w')
        for label in labels:
            f.write(label)
            f.write(' ')
        f.write('\n')
        for i in range(len(labels)):
            f.write(labels[i])
            f.write(' ')
            for point in mat[i]:
                f.write(str(int(point)))
                f.write(' ')
            f.write('\n')
        f.close()

    
class PAG(nx.Graph):
    """
    A class implementaing a graph which can have
    all edge types of a partial ancestral graph
    """
    def add_edge(self, u,v, utag = 'o', vtag = 'o'):
        """
        A method to add an edge to a graph
        
        Parameters
        ----------
        u : str
            the from node of an edge
        v: str
            the to node of an edge
        utag: str
            the tag of the from node of an edge
        vtag: str
            the tag of the to node of an edge
        """
        super().add_edges_from([(u,v, {u:utag, v:vtag})])
    
    
    def has_directed_edge(self, u,v):
        """
        A method to check the graph for a directed edge 
        (an edge with a > tag on the to node)
        
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge
        
        Returns
        ------- 
        bool
            True if has directed edge, false if not

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
        A method to check the graph for a fully directed edge 
        (an edge with a > tag on the to node and 
        a - tag on the from node)
        
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge

        Returns
        ------- 
        bool
            True if has fully directed edge, false if not

        """
        if super().has_edge(u,v):
            tags = super().get_edge_data(u,v)
            if tags[u] == '-' and tags[v] == '>':
                return True
            else:
                return False
        else:
            return False

    def has_fully_undirected_edge(self, u,v):
        """
        A method to check the graph for a fully undirected edge 
        (an edge with a - tag on the to node and 
        a - tag on the from node)
        
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge

        Returns
        ------- 
        bool
            True if has undirected edge, false if not
        """
        if super().has_edge(u,v):
            tags = super().get_edge_data(u,v)
            if tags[u] == '-' and tags[v] == '-':
                return True
            else:
                return False
        else:
            return False

    def add_edges_from(self, bunch):
        """
        A method to add a list of edges with o tags to a graph
        
        Parameters
        ----------
        bunch: iterable
            a list of pairs of nodes which are edges
        """
        for edge in bunch:
            super().add_edges_from([(*(edge), {edge[0]:'o', edge[1]:'o'})])

    def setTag(self, edge, node, tag):
        """
        A method to set the tag of one side of an edge
        
        Parameters
        ----------
        edge : [str,str]
            the two nodes of the edge to modify
        node: str
            the side of the edge to modify
        tag: str
            the new tag of the edge, in [>,-,o]
        """
        if super().has_edge(*edge):
            self.edges[edge][node] = tag
    
    def direct_edge(self, u,v):
        """
        A method to direct an edge in a graph (set the tag of the to node to >)
        
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge

        """
        if super().has_edge(u,v):
            self.edges[(u,v)][v] = '>'

    def fully_direct_edge(self, u,v):
        """
        A method to fully direct an edge in a graph 
        (set the tag of the to node to > and the from node to -)

        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge

        """
        if super().has_edge(u,v):
            self.edges[(u,v)][v] = '>'
            self.edges[(u,v)][u] = '-'

    def undirect_edge(self, u,v):
        """
        A method to fully undirect an edge in a graph 
        (set the tag of the to node to - and the from node to -)
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge

        """
        if super().has_edge(u,v):
            self.edges[(u,v)][v] = '-'
            self.edges[(u,v)][u] = '-'    

    def hasDiscPath(self,u, v, b):
        """
        A method to see if the pag has a discriminating path 
        between two nodes
        Parameters
        ----------
        u : str
            the from node of the path
        v: str
            the to node of the path
        b: str
            the penultimate node of the disc path
        
        Returns
        -------
        bool
            True if there is a disc path, false if not

        """
        all_paths = nx.all_simple_paths(self, u, v)
        for path in all_paths:             
            if b in path:
                b_pred  = (path.index(v) - path.index(b)) == 1 and self.has_edge(b,v)
                all_colliders = True
                for node in path[1:-1]:
                    prev = path[path.index(node)-1]
                    suc = path[path.index(node)+1]
                    if (node != b) and not ((self.has_directed_edge(prev,node)) and (self.has_directed_edge(suc,node))):
                        all_colliders = False
                all_pred = True
                for node in path[1:-2]:
                    if not (self.has_directed_edge(node, v)):
                        all_pred = False
                nonadj = not self.has_edge(u,v)
                if (b_pred and all_colliders and all_pred and nonadj):       
                    return True
        return False

    def findDiscPath(self,u,v,b):
        """
        A method find all discriminating paths
        between two nodes in the pag
        Parameters
        ----------
        u : str
            the from node of the path
        v: str
            the to node of the path
        b: str
            the penultimate node of the disc path

        Returns
        -------
        str[][]
            List of discriminating paths in pag between the two nodes on the third node
        """
        all_paths = nx.all_simple_paths(self, u, v)
        discpaths = []
        for path in all_paths:
            if b in path:
                b_pred  = (path.index(v) - path.index(b)) == 1 and self.has_edge(b,v)
                all_colliders = True
                for node in path[1:-1]:
                    prev = path[path.index(node)-1]
                    suc = path[path.index(node)+1]
                    if (node != b) and not ((self.has_directed_edge(prev,node)) and (self.has_directed_edge(suc,node))):
                        all_colliders = False
                all_pred = True
                for node in path[1:-2]:
                    if not (self.has_directed_edge(node, v)):
                        all_pred = False
                nonadj = not self.has_edge(u,v)
                if (b_pred and all_colliders and all_pred and nonadj):
                    discpaths.append(path)
        return discpaths
    
    def has_o(self,u,v,side):
        """
        A method to check the graph for a o tag on one side of an edge 
        
        Parameters
        ----------
        u : str
            the from node of the edge
        v: str
            the to node of the edge
        side: str
            the side to test for the tag

        Returns
        ------- 
        bool
            True if has undirected edge, false if not
        """
        cond = False
        if self.has_edge(u,v):
            if self[u][v][side] == 'o':
                cond = True
        return cond


    def isUncovered(self, path):
        """
        A method to see if the path is uncovered in the pag
        Parameters
        ----------
        path: str[]
            list of nodes
        
        Returns
        -------
        bool
            True if path is uncovered path, false if not

        """
        for x in range(1,len(path)-1):
            pred = path[x-1]
            suc = path[x+1]
            if self.has_edge(pred,suc):
                return False
        return True

    def isPD(self, path):
        """
        A method to see if the path is potentially directed in the pag
        Parameters
        ----------
        path: str[]
            list of nodes
        
        Returns
        -------
        bool
            True if path is potentially directed path, false if not

        """
        for x in range(len(path)-1):
            node = path[x]
            suc = path[x+1]
            edge = self.get_edge_data(node,suc)
            if (edge[suc] == '-' or edge[node] == '>'):
                return False
        return True

    def isCirclePath(self,path):
        """
        A method to see if the every tag in the path is an o
        Parameters
        ----------
        path: str[]
            list of nodes
        
        Returns
        -------
        bool
            True if every tag in the path is an o, false if not
        """
        for i in range(len(path[:-1])):
            node = path[i]
            suc = path[i+1]
            if not (self.has_o(node,suc,node) and self.has_o(suc,node,suc)):
                return False
        return True

    
    def findUncoveredCirclePaths(self,u,v):
        """
        A method find all circle paths
        between two nodes in the pag
        Parameters
        ----------
        u : str
            the from node of the path
        v: str
            the to node of the path

        Returns
        -------
        str[][]
            List of circle paths in pag between the two nodes
        """
        paths = []
        for path in nx.all_simple_paths(self, u,v):
            if self.isUncovered(path) and self.isCirclePath(path):
                paths.append(path)
        return paths

    def to_matrix(self):
        """
        A method to generate the adjacency matrix of the graph
        
        Returns
        ----------
        numpy.ndarray
            a 2d array containing the adjacency matrix of the graph

        """
        symbol_map = {'o':1,'>':2,'-':3}
        
        labels = [node for node in self]
        mat = np.zeros((len(labels), (len(labels))))
        for x in labels:
            for y in labels:
                if self.has_edge(x,y):
                    mat[labels.index(x)][labels.index(y)] = symbol_map[self.get_edge_data(x,y)[y]]
        return mat
    
    def write_to_file(self, path):
        """
        A method to write the adjacency matrix of the graph to a file
        
        Parameters
        ----------
        path: str
            path to file to write adjacency matrix to

        """
        mat = self.to_matrix()
        labels = [node for node in self]
        f = open(path, 'w')
        for label in labels:
            f.write(label)
            f.write(' ')
        f.write('\n')
        for i in range(len(labels)):
            f.write(labels[i]) 
            f.write(' ')
            for point in mat[i]:
                f.write(str(int(point)))
                f.write(' ')
            f.write('\n')
        f.close()