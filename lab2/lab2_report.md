# Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata
### Author: Clima Marin

----

## Theory
Finite automata are abstract machines used to recognize patterns in input sequences, forming the basis for understanding regular languages in computer science. They consist of states, transitions, and input symbols, processing each symbol step-by-step. If the machine ends in an accepting state after processing the input, it is accepted; otherwise, it is rejected. Finite automata come in deterministic (DFA) and non-deterministic (NFA), both of which can recognize the same set of regular languages.
* A DFA is represented as {Q, Σ, q, F, δ}. In DFA, for each input symbol, the machine transitions to one and only one state. DFA does not allow any null transitions, meaning every state must have a transition defined for every input symbol.
* NFA is similar to DFA but includes the following features: It can transition to multiple states for the same input. It allows null (ϵ) moves, where the machine can change states without consuming any input.

## Objectives:

1. Understand what an automaton is and what it can be used for.
2. Continuing the work in the same repository and the same project, the following need to be added:
   * a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
   * b. For this you can use the variant from the previous lab.
3. According to your variant number (9) , get the finite automaton definition and do the following tasks:
   * Implement conversion of a finite automaton to a regular grammar.
   * Determine whether your FA is deterministic or non-deterministic.
   * Implement some functionality that would convert an NDFA to a DFA.
   * Represent the finite automaton graphically (Optional, and can be considered as a bonus point)


## Implementation description

### Task 2:

The classify_grammar method determines the Chomsky classification of a grammar based on its production rules.

* Type 3 (Regular Grammar): The method checks if each production conforms to the structure of a regular grammar, which allows either a terminal symbol or a non-terminal followed by a terminal, or a non-terminal followed by a non-terminal (but no other combinations).
* Type 2 (Context-Free Grammar): It ensures that the left-hand side of every production is a single non-terminal (which is a requirement for context-free grammars).
* Type 1 (Context-Sensitive Grammar): It verifies that for each production, the length of the right-hand side is greater than or equal to the left-hand side. This is the defining property of context-sensitive grammars.

If none of the conditions for Types 3, 2, or 1 hold, the grammar is classified as Type 0 (Unrestricted), which is the most general form in Chomsky's hierarchy.
```
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
```

### Task 3: 
The core of the implementation is a FiniteAutomaton class that encapsulates all the required functionality:
The finite automaton is defined with the following parameters for Variant 9:

* States: Q = {q0, q1, q2, q3, q4}
* Alphabet: Σ = {a, b, c}
* Final States: F = {q4}
* Transitions:

  - δ(q0, a) = q1
  - δ(q1, b) = q2
  - δ(q2, c) = q0
  - δ(q1, b) = q3
  - δ(q3, a) = q4
  - δ(q3, b) = q0

```
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
```


* The method "is_deterministic()" checks if the FA has multiple transitions from the same state on the same input symbol:
The automaton is non-deterministic because state q1 has two different transitions on the symbol 'b' (to both q2 and q3). 
```
 def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                destinations = self.get_transitions(state, symbol)
                if len(destinations) > 1:
                    return False

        return True
```

The method "to_regular_grammar()" implements the conversion of the finite automaton to a right-linear grammar:
For each transition, a production rule is created. If the destination state is a final state, an additional production is added that derives only the terminal symbol.
```
 def to_regular_grammar(self):
        grammar = {}

        for (state, symbol), destinations in self.transitions.items():
            if state not in grammar:
                grammar[state] = []

            dest_list = destinations if isinstance(destinations, list) else [destinations]

            for dest in dest_list:
                if dest in self.final_states:
                    grammar[state].append(f"{symbol}")
                    grammar[state].append(f"{symbol}{dest}")
                else:
                    grammar[state].append(f"{symbol}{dest}")


        if self.start_state in self.final_states:
            if self.start_state not in grammar:
                grammar[self.start_state] = []
            grammar[self.start_state].append("ε")

        return grammar
```

The subset construction algorithm is implemented in the "to_dfa()" method, which:

* Creates composite states representing sets of states from the original NDFA
* Computes transitions for each composite state on each symbol
* Identifies final states in the new DFA

The resulting DFA preserves all the behaviors of the original NDFA but ensures that each state has at most one transition for each input symbol.

```
    def to_dfa(self):
        if self.is_deterministic():
            return self

        dfa_states = []
        dfa_transitions = {}
        dfa_final_states = []

        start_closure = frozenset([self.start_state])
        unprocessed_states = [start_closure]
        dfa_states.append(start_closure)

        while unprocessed_states:
            current_state = unprocessed_states.pop(0)

            for symbol in self.alphabet:
                next_state_set = set()


                for state in current_state:
                    next_states = self.get_transitions(state, symbol)
                    next_state_set.update(next_states)

                if not next_state_set:
                    continue

                next_state = frozenset(next_state_set)

                dfa_transitions[(current_state, symbol)] = next_state

                if next_state not in dfa_states:
                    dfa_states.append(next_state)
                    unprocessed_states.append(next_state)

        for state in dfa_states:
            if any(s in self.final_states for s in state):
                dfa_final_states.append(state)

        state_map = {state: f"q{i}" for i, state in enumerate(dfa_states)}

        new_transitions = {}
        for (state, symbol), next_state in dfa_transitions.items():
            new_transitions[(state_map[state], symbol)] = state_map[next_state]

        return FiniteAutomaton(
            states=[state_map[state] for state in dfa_states],
            alphabet=self.alphabet,
            transitions=new_transitions,
            start_state=state_map[dfa_states[0]],
            final_states=[state_map[state] for state in dfa_final_states]
        )
```

The method visualize() uses Graphviz to create a graphical representation of the automaton:
The visualization follows conventions:

1. Regular states are represented as circles
2. Final states are represented as double circles
3. The start state has an incoming arrow
4. Transitions are represented as labeled arrows

```
    def visualize(self):
        dot = graphviz.Digraph(comment='Finite Automaton')

        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')

        dot.node('start', style='invisible')
        dot.edge('start', self.start_state)

        for (state, symbol), destinations in self.transitions.items():
            if isinstance(destinations, list):
                for dest in destinations:
                    dot.edge(state, dest, label=symbol)
            else:
                dot.edge(state, destinations, label=symbol)

        return dot
```

## Results
``` 
Regular Grammar:
q0 → aq1
q1 → bq2
q1 → bq3
q2 → cq0
q3 → a
q3 → aq4
q3 → bq0

Is the FA deterministic? No
Reason: The state q1 has two transitions on the symbol 'b' (to both q2 and q3)

Converting NDFA to DFA...
DFA states: ['q0', 'q1', 'q2', 'q3']
DFA transitions:
δ(q0, a) = q1
δ(q1, b) = q2
δ(q2, a) = q3
δ(q2, b) = q0
δ(q2, c) = q0
DFA final states: ['q3']

FA visualization saved as 'finite_automaton.png'
DFA visualization saved as 'deterministic_finite_automaton.png'
```
![deterministic_finite_automaton.png](deterministic_finite_automaton.png)
![finite_automaton.png](finite_automaton.png)



## Conclusion

The results highlight the relationship between finite automata and regular grammars, as well as the process of converting from non-deterministic to deterministic automata. This conversion is fundamental in compiler design and pattern matching algorithms.
The implementation of the grammar classification function further demonstrates the relationship between formal languages and their corresponding automata, reinforcing the theoretical foundation of the Chomsky hierarchy.
## References

1. _Formal Languages and Finite Automata, Guide for practical lessons_ by COJUHARI Irina, DUCA Ludmila, FIODOROV Ion.
2. _Graphviz Documentation_: https://graphviz.readthedocs.io/