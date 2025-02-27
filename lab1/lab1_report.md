# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Clima Marin

----

## Theory
A formal language consists of an alphabet, a vocabulary, and a grammar.
The grammar defines the rules for constructing valid words in the language, and the automaton defines a mechanism for recognizing strings belonging to the language.
This project explores the relationship between regular grammars and finite automata by converting a given grammar into a finite automaton and checking if a string belongs to the language defined by the grammar.
A finite automaton (FA) is a state machine with a finite number of states that processes input strings one symbol at a time, transitioning between states based on predefined rules.

## Objectives:

* Implement a Grammar class to represent a given grammar with non-terminals, terminals, and production rules
* Implement a method to generate valid strings from the grammar with their derivations
* Implement a Finite Automaton (FA) class to convert the grammar to an automaton
* Implement functionality to check if strings belong to the language accepted by the automaton

## Implementation description

* The Grammar class is initialized with specific sets of non-terminals (VN), terminals (VT), production rules (P), and a start symbol:

* VN = {'S', 'B', 'D', 'Q'}
* VT = {'a', 'b', 'c', 'd'}
* Production rules include: S → aB|bB, B → cD, D → dQ|a, Q → bB|dQ

```
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
```


* "generate_string" generates a single valid string from the grammar using recursive derivation, keeping track of the derivation steps:
```
def generate_string(self, max_depth=100):
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
```

Finite Automaton Class
* The FiniteAutomaton class represents a finite automaton with:

* states: A set of states.

* alphabet: A set of input symbols.

* transitions: A transition function mapping states and symbols to new states.

* start_state: The initial state of the automaton.

* accept_states: A set of accepting states.
```
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
```

* "to_finite_automaton" converts the grammar into a Finite Automaton by creating states corresponding to non-terminals plus a final state:
```
def to_finite_automaton(self):
    states = {'qS', 'qB', 'qD', 'qQ', 'qF'}
    transitions = {
        'qS': {'a': {'qB'}, 'b': {'qB'}},
        'qB': {'c': {'qD'}},
        'qD': {'d': {'qQ'}, 'a': {'qF'}},
        'qQ': {'b': {'qB'}, 'd': {'qQ'}}
    }
    return FiniteAutomaton(states, self.VT, transitions, 'qS', {'qF'})
```

* The FiniteAutomaton class implements string acceptance checking through the "accepts" method:

```
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
```

## Results

The implementation successfully generates valid strings and checks string acceptance. For example:
Generated strings with derivations:

* "bca" (S→bB B→cD D→a)
* "acdbca" (S→aB B→cD D→dQ Q→bB B→cD D→a)
* "aca" (S→aB B→cD D→a)

The automaton correctly accepts strings like "bca" while rejecting invalid strings like "acda", "bcda", and "acddddda" as they don't follow the grammar's rules.

## Conclusion

The program successfully implements both a grammar-based string generator and its equivalent finite automaton. The grammar generates strings through recursive derivation, keeping track of the derivation steps, while the finite automaton provides an efficient mechanism for checking whether strings belong to the language. The implementation demonstrates the relationship between regular grammars and finite automata, showing how they can represent the same language in different ways.

## References

_Formal Languages and Finite Automata, Guide for practical lessons_ by COJUHARI Irina, DUCA Ludmila, FIODOROV Ion.