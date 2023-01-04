from sys import stderr, stdin
from time import time
from argparse import ArgumentParser, FileType
from random import SystemRandom

def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapping a URL (str) to a list of target URLs (str).
    """

    # First one is key, second is value (data in school_web is a bunch of 2 node graphs)
    # Iterate through the file line by line
    gdict = dict()
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()
        # Check if url in keys, append current target to dict, else create new key and value using current values
        if node in gdict.keys():
            gdict[node].append(target)
        else:
            gdict[node] = [target]

    return gdict


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""

    nodes = len(graph)
    edges = sum(len(target) for target in graph.values())  # Generator is faster than list comprehension

    print(f"Number of Nodes: {nodes}")
    print(f"Number of edges: {edges}")


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """

    # Create hit_count dict with keys being the nodes of the graph and the values all being 0
    # Defined nodes here to avoid creating a new list every single time I want to use the keys
    # initialize hit_count[node] with 0 for all nodes
    nodes = list(graph.keys())
    hit_count = {node: 0 for node in nodes}

    rng = SystemRandom()
    # randomly selects a node a number of times equal to the repetition argument
    # repeat n_repetition times:
    #     current_node < - randomly selected node
    for repeat in range(args.repeats):
        current_node = rng.choice(nodes)

        # select a random url from the target nodes of the previously selected node
        # repeat n_steps times:
        #     current_node <- uniformly randomly chosen among the out edges of current_node

        for step in range(args.steps):
            current_node = rng.choice(graph[current_node])

        # updating hit_count for the current node
        # hit_count[current_node] += 1/n_repetitions

        hit_count[current_node] += 1 / args.repeats

    return hit_count


def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """

    # very similar initialization to the stochastic method
    # initialize node_prob[node] = 1/(number of nodes) for all nodes
    node_prob = dict()
    nodes = list(graph.keys())

    node_prob = {node: 1/len(nodes) for node in nodes}

    # again, similar to stochastic, defining every value in this dict to be 0
    # repeat n_steps times:
    #     initialize next_prob[node] = 0 for all nodes
    for step in range(args.steps):
        next_prob = dict()
        for node in nodes:
            next_prob[node] = 0

        # for each node:
        #     p <- node_prob[node] divided by its out degree
        for node in nodes:
            p = node_prob[node] * 1/len(graph[node])

            # updating probability
            # for each target among out edges of node:
            #     next_prob[target] += p
            for outedges in graph[node]:
                next_prob[outedges] += p

        # node_prob <- next_prob
        node_prob = next_prob

    return node_prob


parser = ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=FileType('r'), default=stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time()
    ranking = algorithm(graph, args)
    stop = time()
    final_time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100 * v:.2f}\t{k}' for k, v in top[:args.number]))
    stderr.write(f"Calculation took {final_time:.2f} seconds.\n")
