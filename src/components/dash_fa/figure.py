import graphviz
from src.automata.fa import FiniteAutomata
from src.components.dash_page_progression.tree import DashTree
from src.regex.conversion import fa_from


def fa_state_diagram_from(tree: DashTree):
    fa: FiniteAutomata = fa_from(tree.regex)

    graph = graphviz.Digraph('finite-automata',
                             comment='Finite Automata',)

    useless_states = {state for state in fa.states if state not in fa.transitions.keys()}
    common_states = fa.states - fa.final_states - {fa.initial_state} - useless_states

    for state in common_states:
        graph.node(str(state), shape='circle', color='black', style='filled', fillcolor='white')

    only_finals = fa.final_states - {fa.initial_state}
    for state in only_finals:
        graph.node(str(state), shape='doublecircle', color='black', style='filled', fillcolor='white')

    initial_state = fa.initial_state
    graph.node(str(initial_state),
               shape='doublecircle' if initial_state in fa.final_states else 'circle',
               color='black',
               style='filled',
               fillcolor='white')

    for transition, arrival in fa.transitions.items():
        origin, symbol = transition
        for dst in arrival:
            graph.edge(str(origin), str(dst), label=symbol)

    graph.node('start', _attributes={'style': 'invis'})
    graph.edge('start', str(initial_state))

    return graph


if __name__ == '__main__':
    dot: graphviz.Digraph = fa_state_diagram_from(DashTree('(a|b)*abb#'))

    for node in dot.body:
        print(node.strip())

    dot.render()
