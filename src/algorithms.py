import networkx as nx
import itertools
from pandas import DataFrame
from graphs import PDAG

class GraphLearner(object):
    """
    Base Class for all graph learning algorithms 
    implementing functionality used across algorithms
    """

    def __init__(self, data, indep_test,  alpha = 0.05):
        """
        Initialise graph learner object
        Parameters
        ----------
            data : pandas.DataFrame, 
                DataFrame with rows as datapoints and columns as variables 
            indep_test : function
                A function which can calculate indpendence of variabkles in data
            alpha : float, optional
                The minimum p-value returned by the indepence test
                for the data to be considered independent
        """
        self.alpha = alpha
        self.data = data
        self.indep_test = indep_test

    def learnSkeleton(self):
        """ A  function to build the skeleton of a causal graph from data
        
        Returns
        -------
            networkx.Graph
                The skeleton of the causal network
            dict
                Dicitonary containg separation sets of all pairs of nodes
        """ 
        
        # Find variable labels
        labels = list(self.data.columns)
        # Generate completed graph
        graph = nx.complete_graph(len(labels))
        #Rename nodes in graph with labels
        name_map = {i:label for i,label in enumerate(labels)}
        graph = nx.relabel_nodes(graph, name_map)
        sepset = {}
        condsize = 0
        for x in graph:
            for y in graph.neighbors(x):
                sepset[(x,y)] = ()
                sepset[(y,x)] = ()
        # Iterate over each pair of adjacent nodes
        condlen = 1
        while condlen != 0:
            condlen = 0
            ylabels = labels.copy()
            for x in labels:
                for y in labels:
                    if y in graph.neighbors(x):
                        # Generate the conditioning sets needed for independence tests
                        condSets = self.gen_cond_sets(x,y,graph,condsize)
                        if not len(condSets) == 0:                           
                            condlen += len(condSets) 
                            # Test for independence with each conditioning set
                            for condset in condSets:
                                print('testing {} indep {} given {}'.format(x,y,condset))
                                p, *_ = self.indep_test(self.data, x, y, condset) 
                                indep = p > self.alpha
                                #stop testing if independence is found and remove edge
                                if indep:
                                    print('removing edge {},{}, with certainty {}'.format(x,y,p))
                                    graph.remove_edge(x,y)
                                    sepset[(x,y)] = condset
                                    sepset[(y,x)] = condset
                                    break
            condsize += 1      
        return graph, sepset

    def gen_cond_sets(self, x,y, g, size):
        """ A  function to build the set of conditioning sets to be for variables x and y
        on graph g of a certain size when generating a skeleton
        
        Parameters
        ----------
            X : str, 
                One variable being tested for independence, 
            Y : str
                The other variable being tested for independence
            graph : float, optional
                The minimum p-value returned by the indepence test
                for the data to be considered independent
            size: int
                the size of each conditioning set to be returned
        Returns
        -------
            list of lists of strings
                a list of conditioning sets to be tested
        """ 
        # Handle size 0 case
        if size == 0:
            return [()]
        # Get all neighbors of x in g
        adjy = g.neighbors(x)
        # Remove y from neighbour list
        adj = [node for node in adjy if node!= y]
        # Generate all unique combinations of len size
        combos = itertools.combinations(adj, size)
        # Convert to list
        combos = [combo for combo in combos]
        return combos

    def orientEdges(self):
        pass

    @staticmethod
    def prepare_data(data_file, delim = ' ', isLabeled = False, ):
        """
        A function which reads data from a file into a pandas dataframe
        the file should consist of rows of datapoints with each variable
        separated by some delimination string
        
        Parameters
        ----------
            data_file : str, 
                The path to the file containing data 
            delim : str, optional
                the deliminating string, ',' for csv files
            isLabeled : bool, optional
                True if the first line in the file is the lit of variabe names
        Returns
        -------
            pandas.DataFrame
                data frame containing data from file
        """

        with open(data_file, 'r') as f:
            if isLabeled:
                labels = f.readline().replace('\n','').split(delim)
                line1 = f.readline().replace('\n','').split(delim)
            else:
                line1 = f.readline().replace('\n','').split(delim)
                labels = [str(i) for i in range(len(line1))]
            data = []
            data.append(line1)
            for line in f.readlines():
                line = line.replace('\n','').split(delim)
                data.append(line) 
            data = DataFrame(data, columns = labels)   
        return data


    def orient_V(self, undirected, directed, sepset):
        """
        A method to orient all "V-structures" in a graph

        Parameters
        ----------
        undirected: nx.Graph
            graph containing the undirected edges
        directed: nx.DiGraph
            graph containing the directed edges
        sepset: Dict
            dictionary with pairs of nodes as keys and 
            seperating sets of nodes as values
        """
        skeleton = undirected.copy()
        for i in undirected:
            for j in undirected:
                if i != j:
                    for k in undirected:
                        if i != k and j != k:
                            if skeleton.has_edge(i,k) and skeleton.has_edge(k,j) and not skeleton.has_edge(i,j) and k not in sepset[(i,j)]:
                                directed.add_edge(j,k)
                                if directed.has_edge(k,j):
                                    directed.remove_edge(k,j)
                                if undirected.has_edge(j,k):
                                    undirected.remove_edge(j,k)
                                directed.add_edge(i,k)
                                if directed.has_edge(k,i):
                                    directed.remove_edge(k,i)
                                if undirected.has_edge(i,k):
                                    undirected.remove_edge(i,k)
                            
    @staticmethod
    def findPath( x,y, directed, explored):
        """
        A method to check if there is a path between two nodes in  graph
        ----------
        x: str
            from node of a path
        y: str
            to node of a path
        directed: nx.DiGraph
            Directed graph
        explored: str[]
            list of nodes explored by previous recursive calls left as [] in calling
        
        Returns
        -------
        bool
            True if there is a path between x and y in directed
        """

        explored.append(x)
        neigh = []
        for n in directed.successors(x):
            neigh.append(n)
        Z = []
        for n in neigh:
            if n  not in explored:
                Z.append(n)
        if y in Z:
            return True
        if len(Z) == 0:
            return False
        isPath = False
        for z in Z:    
            zcont =  GraphLearner.findPath(z,y, directed, explored)
            isPath = isPath or zcont
        return isPath