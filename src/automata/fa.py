from src.automata.state import State


class FiniteAutomata:

    def __init__(self):
        self.initial_state = State()
        self.states = {self.initial_state}
        self.transitions = dict()
        self.final_states = set()
