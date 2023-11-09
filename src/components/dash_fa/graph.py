from igraph import Graph
from src.automata.fa import FiniteAutomata


def graph_from(fa: FiniteAutomata):
    graph = Graph(directed=True)

    transitions = fa.transitions
    graph_states = set()

    for src_with_symbol, destination_set in transitions.items():
        source_state, symbol = src_with_symbol
        destination_set: set

        destination_state = destination_set.pop()

        if source_state not in graph_states:
            graph.add_vertex(str(source_state))
            graph_states |= {source_state}

        if destination_state not in graph_states:
            graph.add_vertex(str(destination_state))
            graph_states |= {destination_state}

        graph.add_edge(str(source_state), str(destination_state), label=symbol)

    to_delete_ids = [v.index for v in graph.vs if v.degree() == 0]  # Gathers all vertices without edges and...
    graph.delete_vertices(to_delete_ids)  # Removes them from the graph.

    return graph
