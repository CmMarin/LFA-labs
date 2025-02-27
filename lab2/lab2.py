import random

class Grammar:
    def __init__(self):
        self.VN = {'S', 'B', 'D', 'Q'}
        self.VT = {'a', 'b', 'c', 'd'}
        self.P = {
            'S': ['aB', 'bB'],
            'B': ['cD'],
            'D': ['dQ', 'a'],
            'Q': ['bB', 'dQ']
        }
        self.start = 'S'

    def generate_string(self, max_depth=10):
        def derive(symbol, depth, derivation):
            if depth > max_depth:
                return '', derivation
            if symbol in self.VT:
                return symbol, derivation
            production = random.choice(self.P[symbol])
            derived_string = ''
            new_derivation = derivation + f"{symbol}→{production} "
            for s in production:
                result, new_derivation = derive(s, depth + 1, new_derivation)
                derived_string += result
            return derived_string, new_derivation

        return derive(self.start, 0, "")

    def generate_strings(self, count, max_depth=10):
        results = []
        for _ in range(count):
            derived_string, derivation = self.generate_string(max_depth)
            results.append((derived_string, derivation.strip()))
        return results

    def to_finite_automaton(self):
        states = {'qS', 'qB', 'qD', 'qQ', 'qF'}
        transitions = {
            'qS': {'a': {'qB'}, 'b': {'qB'}},
            'qB': {'c': {'qD'}},
            'qD': {'d': {'qQ'}, 'a': {'qF'}},
            'qQ': {'b': {'qB'}, 'd': {'qQ'}}
        }
        return FiniteAutomaton(states, self.VT, transitions, 'qS', {'qF'})

    def classify_grammar(self):
        is_type_3 = True
        is_type_2 = True
        is_type_1 = True

        for non_terminal, productions in self.P.items():
            for production in productions:
                # Check for Type 3 (Regular Grammar)
                if len(production) == 1 and production[0] in self.VT:
                    continue
                elif len(production) == 2 and production[0] in self.VT and production[1] in self.VN:
                    continue
                elif len(production) == 2 and production[0] in self.VN and production[1] in self.VT:
                    continue
                else:
                    is_type_3 = False

                # Check for Type 2 (Context-Free Grammar)
                if len(non_terminal) != 1 or non_terminal not in self.VN:
                    is_type_2 = False

                # Check for Type 1 (Context-Sensitive Grammar)
                if len(production) < len(non_terminal):
                    is_type_1 = False

        if is_type_3:
            return "Type 3 (Regular)"
        elif is_type_2:
            return "Type 2 (Context-Free)"
        elif is_type_1:
            return "Type 1 (Context-Sensitive)"
        else:
            return "Type 0 (Unrestricted)"

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        current_states = {self.start_state}
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])
            if not next_states:
                return False
            current_states = next_states
        return bool(current_states & self.accept_states)

if __name__ == "__main__":
    grammar = Grammar()
    generated_strings = grammar.generate_strings(5, max_depth=10)
    print("Generated strings with derivations:")
    for string, derivation in generated_strings:
        print(f"String: {string}, Derivation: {derivation}")

    fa = grammar.to_finite_automaton()
    test_strings = [
        "aca",
        "bca",
        "bcda",
        "acddbca",
        "acdddbca",
        "acddddda",
        "bcdddddda",
    ]

    print("\nTesting strings in automaton:")
    for s in test_strings:
        print(f"String {s} is {'accepted' if fa.accepts(s) else 'rejected'} by FA")

    # task 2
    print("\nClassifying the grammar based on Chomsky hierarchy:")
    print(grammar.classify_grammar())