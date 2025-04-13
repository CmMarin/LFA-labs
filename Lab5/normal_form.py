class Grammar:
    def __init__(self, non_terminals=None, terminals=None, start_symbol=None, productions=None):
        self.non_terminals = non_terminals if non_terminals else set()
        self.terminals = terminals if terminals else set()
        self.start_symbol = start_symbol
        self.productions = productions if productions else {}

    def __str__(self):
        result = f"G = ({self.non_terminals}, {self.terminals}, P, {self.start_symbol})\n"
        result += "P = {\n"
        for left, rights in self.productions.items():
            for right in rights:
                result += f"    {left} -> {right}\n"
        result += "}"
        return result

    def copy(self):
        """Create a deep copy of the grammar."""
        new_productions = {}
        for left, rights in self.productions.items():
            new_productions[left] = set(rights)
        return Grammar(
            non_terminals=set(self.non_terminals),
            terminals=set(self.terminals),
            start_symbol=self.start_symbol,
            productions=new_productions
        )


class CNFConverter:
    def __init__(self, grammar):
        self.grammar = grammar.copy()
        self.new_symbol_counter = 0

    def _generate_new_symbol(self):
        """Generate a new non-terminal symbol that doesn't exist in the grammar."""
        while True:
            self.new_symbol_counter += 1
            new_symbol = f"X{self.new_symbol_counter}"
            if new_symbol not in self.grammar.non_terminals:
                return new_symbol

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
                        break

        # Replace productions with nullable symbols
        new_productions = {}
        for left, rights in self.grammar.productions.items():
            new_productions[left] = set(rights)

            for right in rights:
                # Generate all possible combinations without nullable symbols
                nullable_positions = [i for i, symbol in enumerate(right) if symbol in nullable]
                for mask in range(1, 1 << len(nullable_positions)):
                    new_right = list(right)
                    # Remove nullable symbols according to the current mask
                    for i, pos in enumerate(nullable_positions):
                        if mask & (1 << i):
                            new_right[pos] = ""

                    new_right_str = "".join(new_right)
                    if new_right_str:  # Don't add empty string as a production
                        new_productions[left].add(new_right_str)

        self.grammar.productions = new_productions
        return self.grammar

    def eliminate_unit_productions(self):
        """Step 2: Eliminate unit productions (renaming)."""
        # Find all unit pairs (A, B) where A =>* B and B is a non-terminal
        unit_pairs = {(nt, nt) for nt in self.grammar.non_terminals}  # Initialize with (A, A) for all A

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

            unit_pairs = new_pairs

        # Replace unit productions
        new_productions = {}
        for left in self.grammar.non_terminals:
            new_productions[left] = set()

        for left, rights in self.grammar.productions.items():
            for right in rights:
                if right not in self.grammar.non_terminals:  # Not a unit production
                    if left not in new_productions:
                        new_productions[left] = set()
                    new_productions[left].add(right)

        # Add non-unit productions based on unit pairs
        for a, b in unit_pairs:
            if a != b:  # Skip the reflexive pairs
                if b in self.grammar.productions:
                    for right in self.grammar.productions[b]:
                        if right not in self.grammar.non_terminals:  # Not a unit production
                            if a not in new_productions:
                                new_productions[a] = set()
                            new_productions[a].add(right)

        self.grammar.productions = new_productions
        return self.grammar

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

        # Create new grammar with only accessible symbols
        new_productions = {}
        for left in accessible:
            if left in self.grammar.productions:
                new_productions[left] = set()
                for right in self.grammar.productions[left]:
                    new_productions[left].add(right)

        # Update non-terminals
        new_non_terminals = self.grammar.non_terminals.intersection(accessible)

        self.grammar.non_terminals = new_non_terminals
        self.grammar.productions = new_productions
        return self.grammar

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

                for right in rights:
                    if all(symbol in productive or symbol in self.grammar.terminals for symbol in right):
                        productive.add(left)
                        changed = True
                        break

        # Create new grammar with only productive symbols
        new_productions = {}
        for left in productive:
            new_productions[left] = set()
            if left in self.grammar.productions:
                for right in self.grammar.productions[left]:
                    all_productive = True
                    for symbol in right:
                        if symbol in self.grammar.non_terminals and symbol not in productive:
                            all_productive = False
                            break

                    if all_productive:
                        new_productions[left].add(right)

        # Update non-terminals
        new_non_terminals = self.grammar.non_terminals.intersection(productive)

        self.grammar.non_terminals = new_non_terminals
        self.grammar.productions = new_productions
        return self.grammar

    def convert_to_cnf(self):
        """Step 5: Convert to Chomsky Normal Form."""
        # Create a new start symbol if the start symbol appears on the right side of any production
        for left, rights in self.grammar.productions.items():
            for right in rights:
                if self.grammar.start_symbol in right:
                    new_start = self._generate_new_symbol()
                    self.grammar.non_terminals.add(new_start)
                    self.grammar.productions[new_start] = {self.grammar.start_symbol}
                    self.grammar.start_symbol = new_start
                    break
            if self.grammar.start_symbol != left:
                break

        # Replace terminal symbols in productions with more than one symbol
        terminal_replacements = {}
        new_productions = {}

        for left, rights in self.grammar.productions.items():
            new_productions[left] = set()

            for right in rights:
                if len(right) > 1:
                    new_right = ""
                    for symbol in right:
                        if symbol in self.grammar.terminals:
                            if symbol not in terminal_replacements:
                                new_nt = self._generate_new_symbol()
                                terminal_replacements[symbol] = new_nt
                                self.grammar.non_terminals.add(new_nt)
                                if new_nt not in new_productions:
                                    new_productions[new_nt] = set()
                                new_productions[new_nt].add(symbol)
                            new_right += terminal_replacements[symbol]
                        else:
                            new_right += symbol
                    new_productions[left].add(new_right)
                else:
                    new_productions[left].add(right)

        self.grammar.productions = new_productions

        # Break productions with more than two non-terminals
        new_productions = {}
        for left, rights in self.grammar.productions.items():
            new_productions[left] = set()

            for right in rights:
                if len(right) > 2:
                    symbols = list(right)
                    while len(symbols) > 2:
                        new_nt = self._generate_new_symbol()
                        self.grammar.non_terminals.add(new_nt)
                        if new_nt not in new_productions:
                            new_productions[new_nt] = set()

                        # Take the last two symbols and replace with new non-terminal
                        last_two = symbols[-2] + symbols[-1]
                        symbols = symbols[:-2] + [new_nt]
                        new_productions[new_nt].add(last_two)

                    new_productions[left].add(''.join(symbols))
                else:
                    new_productions[left].add(right)

        self.grammar.productions = new_productions
        return self.grammar

    def to_cnf(self):
        """Convert grammar to Chomsky Normal Form by applying all steps in sequence."""
        self.eliminate_epsilon_productions()
        self.eliminate_unit_productions()
        self.eliminate_inaccessible_symbols()
        self.eliminate_nonproductive_symbols()
        self.convert_to_cnf()
        return self.grammar


# Test with the variant 9 grammar
def test_variant_9():
    # Manually create the grammar from variant 9
    non_terminals = {'S', 'A', 'B', 'C', 'D'}
    terminals = {'a', 'b'}
    start_symbol = 'S'
    productions = {
        'S': {'bA', 'BC'},
        'A': {'a', 'aS', 'bAaAb'},
        'B': {'A', 'bS', 'aAa'},
        'C': {'ε', 'AB'},
        'D': {'AB'}
    }

    grammar = Grammar(non_terminals, terminals, start_symbol, productions)
    print("Original Grammar:")
    print(grammar)
    print("\n")

    converter = CNFConverter(grammar)
    cnf_grammar = converter.to_cnf()

    print("Grammar in Chomsky Normal Form:")
    print(cnf_grammar)


# Run the test
test_variant_9()


# Additional test with a different grammar
def test_custom_grammar():
    # Manually create a custom grammar
    non_terminals = {'S', 'A', 'B', 'C'}
    terminals = {'a', 'b', 'c'}
    start_symbol = 'S'
    productions = {
        'S': {'ABC', 'aB'},
        'A': {'a', 'ε'},
        'B': {'b', 'A'},
        'C': {'c', 'SC'}
    }

    grammar = Grammar(non_terminals, terminals, start_symbol, productions)
    print("\n\nOriginal Custom Grammar:")
    print(grammar)
    print("\n")

    converter = CNFConverter(grammar)
    cnf_grammar = converter.to_cnf()

    print("Custom Grammar in Chomsky Normal Form:")
    print(cnf_grammar)


# Run the additional test
test_custom_grammar()