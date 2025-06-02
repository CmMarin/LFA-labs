# Chomsky Normal Form
### Course: Formal Languages & Finite Automata
### Author: [Clima Marin]

----

## Theory
Chomsky Normal Form is a standardized form of context-free grammars (CFGs) where every production rule conforms to a specific structure. A CFG is in CNF if all its production rules are of the following forms:

CNF is important in formal language theory and automata because it simplifies parsing algorithms, especially for the CYK (Cocke–Younger–Kasami) algorithm. By converting any CFG to CNF, we can ensure a consistent and predictable structure, which is essential for theoretical analysis and computational implementation of parsers.

The transformation to CNF involves several steps:

1. Eliminating null productions (productions that derive ε),
Removing unit productions (like A → B),

2. Eliminating useless symbols, and

3. Converting remaining rules into the CNF format.

## Objectives:

1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
   - The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
   - The implemented functionality needs executed and tested.
   - Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description

#### CNF Converter Implementation
I developed a Python implementation that converts context-free grammars to Chomsky Normal Form (CNF). My solution handles the complete conversion process following these five steps:

Elimination of ε-productions
Elimination of unit productions (renaming)
Elimination of inaccessible symbols
Elimination of non-productive symbols
Conversion to standard CNF format

Key features:

Modular Design: Each transformation step is implemented as a separate method
Complete Pipeline: All necessary CNF conversion steps are included
Generic Solution: Works with any context-free grammar, not just the specific variant
### Grammar Representation
```python
class Grammar:
    def __init__(self, non_terminals=None, terminals=None, start_symbol=None, productions=None):
        self.non_terminals = non_terminals if non_terminals else set()
        self.terminals = terminals if terminals else set()
        self.start_symbol = start_symbol
        self.productions = productions if productions else {}
   ```

The Grammar class represents context-free grammars with sets of non-terminals, terminals, a start symbol, and productions. The string representation provides a clear view of the grammar's components.

### Epsilon Production Elimination
```python 
def eliminate_epsilon_productions(self):
    """Step 1: Eliminate ε productions."""
    # Find all nullable symbols (symbols that can derive epsilon)
    nullable = set()
    
    # Find direct nullable symbols
    for left, rights in self.grammar.productions.items():
        if "ε" in rights or "" in rights:
            nullable.add(left)
            rights.discard("ε")
            rights.discard("")
            
    # Find indirect nullable symbols using fixed-point iteration
    changed = True
    while changed:
        changed = False
        for left, rights in self.grammar.productions.items():
            if left in nullable:
                continue
            
            for right in rights:
                if all(symbol in nullable for symbol in right):
                    nullable.add(left)
                    changed = True
                    break```

### Validation System
Validates that generated string matches original regex.
Converts our pattern to standard regex syntax:
- Replaces * with {0,max} 
- Replaces + with {1,max}
- Handles other edge cases
```


### Unit Production Elimination
```python

def eliminate_unit_productions(self):
    """Step 2: Eliminate unit productions (renaming)."""
    # Find all unit pairs (A, B) where A =>* B and B is a non-terminal
    unit_pairs = {(nt, nt) for nt in self.grammar.non_terminals}
    
    # Find direct unit pairs
    for left, rights in self.grammar.productions.items():
        for right in rights:
            if right in self.grammar.non_terminals:
                unit_pairs.add((left, right))
    
    # Find all unit pairs using transitive closure
    changed = True
    while changed:
        changed = False
        new_pairs = set(unit_pairs)
        
        for a, b in unit_pairs:
            for b2, c in unit_pairs:
                if b == b2 and (a, c) not in new_pairs:
                    new_pairs.add((a, c))
                    changed = True
```

### Inaccessible Symbol Elimination
```python
def eliminate_inaccessible_symbols(self):
    """Step 3: Eliminate inaccessible symbols."""
    # Find all accessible symbols starting from the start symbol
    accessible = {self.grammar.start_symbol}
    
    changed = True
    while changed:
        changed = False
        for left in list(accessible):
            if left in self.grammar.productions:
                for right in self.grammar.productions[left]:
                    for symbol in right:
                        if symbol in self.grammar.non_terminals and symbol not in accessible:
                            accessible.add(symbol)
                            changed = True

```


### Non-productive Symbol Elimination


```python
def eliminate_nonproductive_symbols(self):
    """Step 4: Eliminate non-productive symbols."""
    # Find all productive symbols (symbols that can derive a string of terminals)
    productive = set()
    
    # Initially, all terminals are productive
    for left, rights in self.grammar.productions.items():
        for right in rights:
            if all(symbol in self.grammar.terminals for symbol in right):
                productive.add(left)
    
    # Fixed-point iteration to find all productive symbols
    changed = True
    while changed:
        changed = False
        for left, rights in self.grammar.productions.items():
            if left in productive:
                continue
```


### Final CNF Conversion

```python

def convert_to_cnf(self):
    """Step 5: Convert to Chomsky Normal Form."""
    # Create a new start symbol if the start symbol appears on the right side
    for left, rights in self.grammar.productions.items():
        for right in rights:
            if self.grammar.start_symbol in right:
                new_start = self._generate_new_symbol()
                self.grammar.non_terminals.add(new_start)
                self.grammar.productions[new_start] = {self.grammar.start_symbol}
                self.grammar.start_symbol = new_start
                break

```


### Results

The converter successfully handles various grammars, including the variant 9 example:

```python
Original Grammar:
G = ({'B', 'D', 'S', 'C', 'A'}, {'b', 'a'}, P, S)
P = {
    S -> bA
    S -> BC
    A -> bAaAb
    A -> a
    A -> aS
    B -> aAa
    B -> bS
    B -> A
    C -> AB
    C -> ε
    D -> AB
}

Grammar in Chomsky Normal Form:
G = ({'X8', 'X33', 'X20', 'S', 'X31', 'X15', 'X4', 'A', 'B', 'X23', 'X26', 'X21', 'X12', 'X5', 'X29', 'X30', 'X7', 'X10', 'X14', 'C', 'X24', 'X32', 'X27', 'X22', 'X2', 'X6', 'X19', 'X13', 'X3', 'X9', 'X17', 'X28', 'X1', 'X16', 'X25', 'X11', 'X18'}, {'b', 'a'}, P, X1)
P = {
    B -> XX11
    B -> XX14
    B -> a
    B -> XX5
    B -> XX4
    ...
}
```

The implementation also handles other grammars correctly:

```python
Original Custom Grammar:
G = ({'B', 'S', 'C', 'A'}, {'c', 'b', 'a'}, P, S)
P = {
    S -> ABC
    S -> aB
    A -> ε
    A -> a
    B -> b
    B -> A
    C -> c
    C -> SC
}

Custom Grammar in Chomsky Normal Form:
G = ({'B', 'X3', 'S', 'X2', 'X1', 'C', 'A'}, {'c', 'b', 'a'}, P, S)
P = {
    B -> b
    B -> a
    S -> SC
    S -> BC
    ...
}
```

#### Key takeaways from the implementation:

* Fixed-point Algorithms: Used in multiple transformation steps to handle recursive cases
* Symbol Generation: Dynamic creation of new non-terminals when breaking down complex productions
* Clear Transformations: Each step transforms the grammar while preserving the language
* Deep Copy Handling: Careful management of grammar copies to avoid unintended side effects
* Systematic Approach: Methodical application of transformation rules


### Conclusion
This implementation demonstrates how formal language theory can be applied to transform context-free grammars into an equivalent standardized form. The Chomsky Normal Form conversion is essential for many algorithms in formal language processing, including the CYK parsing algorithm.
The modular approach allows for easy debugging and verification of each transformation step. While the final CNF may contain many new non-terminals (as seen in the output), this is an expected consequence of the conversion process as we break down complex productions into simpler forms that conform to the CNF restrictions.
This converter serves as a practical tool for formal language processing tasks, demonstrating the connection between theoretical formal language concepts and practical implementations in computational linguistics and compiler design.

### References
* [1] Chomsky Normal Form - Wikipedia
* [2] Geeksforgeeks.com
* [3] Python documentation
