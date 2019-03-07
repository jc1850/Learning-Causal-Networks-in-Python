import networkx as nx
import itertools
from pandas import DataFrame

class GraphLearner(object):

    def __init__(self, data, indep_test,  alpha = 0.99):
        # TODO: Validate values 
        self.alpha = alpha
        self.data = data
        self.indep_test = indep_test

    def learnSkeleton(self):
        """ A  function to build the skeleton of a causal graph from data
        
        Parameters
        ----------
            data : pandas.DataFrame, 
                The data from which the causal graph is learned, 
            indep_test : function
                A function which will determine if two variables are 
                independent in data based on a conditioning set
            alpha : float, optional
                The minimum p-value returned by the indepence test
                for the data to be considered independent
        Returns
        -------
            networkx.Graph
                The skeleton of the causal network
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
                        if len(condSets) == 0:
                            break
                        condlen += len(condSets) 
                        # Test for independence with each conditioning set
                        for condset in condSets:
                            print('testing {} indep {} given {}'.format(x,y,condset))
                            p, *_ = self.indep_test(self.data, x, y, condset) 
                            indep = p > self.alpha
                            #stop testing if independence is found and remove edge
                            if indep:
                                print('removing edge {},{}'.format(x,y))
                                graph.remove_edge(x,y)
                                sepset[(x,y)] = condset
                                sepset[(y,x)] = condset
                                break
            condsize += 1      
        return graph, sepset

    def gen_cond_sets(self, x,y, g, size):
        """ A  function to build the set of conditioning sets to be for variables x and y
        on graph g of a certain size when generting a skeleton
        
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
        adj = []
        for node in adjy:
            if node != y:
                adj.append(node)
        # Generate all unique combinations of len size
        combos = itertools.combinations(adj, size)
        # Convert to list
        combos = [combo for combo in combos]
        return combos

    def orientEdges(self):
        pass

    @staticmethod
    def prepare_data(data_file, delim = ' ', isLabeled = False, ):
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
