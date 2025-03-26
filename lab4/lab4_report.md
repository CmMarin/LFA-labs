# Regular Expression Generator: Implementation and Demonstration

### Course: Formal Languages & Finite Automata
### Author: [Clima Marin]

----

## Theory
Regular expressions (regex) are powerful pattern-matching tools used in computer science to describe sets of strings according to specific syntactic rules. They play a fundamental role in:

1. String searching and manipulation
2. Input validation
3. Lexical analysis in compilers
4. Text processing applications

A regular expression consists of ordinary characters (like letters and digits) and special characters (metacharacters) that form a search pattern. The theoretical foundation comes from formal language theory, where regular expressions describe regular languages that can be recognized by finite automata.

## Objectives:

1. Understand what regular expressions are and their applications
2. Implement a dynamic regex generator that produces valid strings
3. Handle quantifiers with reasonable limits (max 5 repetitions)
4. (Bonus) Visualize the processing sequence of regex generation

## Implementation description

#### Regex Generator Implementation
I developed a Python class that dynamically interprets regular expressions and generates valid strings that match them. The implementation handles:

1. Character literals
2. Alternation (| operator)
3. Quantifiers (*, +, ?, {n,m})
4. Parentheses for grouping

Key features:
1. Dynamic Interpretation: Doesn't hardcode specific regex patterns
2. Quantifier Handling: Limits repetitions to 5 for * and +
3. Processing Tracking: Records each generation step

### Regex Generator
```python
class RegexGenerator:
    def __init__(self, max_repetitions=5):
        self.max_repetitions = max_repetitions
        self.processing_steps = []
    
    def generate_from_regex(self, regex):
        self.processing_steps = []
        return self._generate_from_pattern(regex)
    
    def _generate_from_pattern(self, pattern):
        # The recursive pattern generator
   ```

The Token class represents individual tokens with a type and optional value. The string representation makes debugging easier by providing a clear view of the token's properties.

### Core Generation Method
```python 
def _generate_from_pattern(self, pattern: str) -> str:
    result = []
    i = 0
    n = len(pattern)
    
    while i < n:
        char = pattern[i]
        
        # Handle escape sequences (like \., \*, etc)
        if char == '\\':
            if i + 1 >= n:
                raise ValueError("Invalid escape sequence at end")
            result.append(pattern[i+1])  # Add the escaped char
            self._log_step(f"Added escaped character: {pattern[i+1]}")
            i += 2  # Skip past the backslash and escaped char
            continue
            
        # Process groups in parentheses (capturing alternations)
        elif char == '(':
            # Find matching closing parenthesis
            balance = 1
            j = i + 1
            while j < n and balance > 0:
                if pattern[j] == '(': balance += 1
                elif pattern[j] == ')': balance -= 1
                j += 1
                
            if balance != 0:
                raise ValueError("Unbalanced parentheses")
            
            # Extract group content and look for quantifiers
            group_content = pattern[i+1:j-1]
            quantifier = self._extract_quantifier(pattern, j)
            
            # Generate content for this group
            generated = self._process_group(group_content, quantifier)
            result.append(generated)
            i = j + len(quantifier) if quantifier else j
```

### Validation System
Validates that generated string matches original regex.
Converts our pattern to standard regex syntax:
- Replaces * with {0,max} 
- Replaces + with {1,max}
- Handles other edge cases

```python 
def _validate_generation(self, regex: str, generated: str) -> bool:
    # Convert our pattern to standard regex syntax
    validation_regex = regex
    validation_regex = re.sub(r'\*', f'{{0,{self.max_repetitions}}}', validation_regex)
    validation_regex = re.sub(r'\+', f'{{1,{self.max_repetitions}}}', validation_regex)
    
    # Handle special cases
    validation_regex = validation_regex.replace('(a|b)', '[ab]')  # Optimize simple alternations
    validation_regex = validation_regex.replace('(c|d)', '[cd]')
    
    try:
        return re.fullmatch(validation_regex, generated) is not None
    except re.error:
        # Fallback to simpler validation if complex regex fails
        return self._basic_validation(regex, generated)
```


### Alternation Handling
Handles groups containing alternation (| operator).
- Args:
        group_content: Content inside parentheses
        quantifier: Optional quantifier after group
- Returns:
        Generated string for this group

```python

def _process_group(self, group_content: str, quantifier: str) -> str:
    # Check for alternation operator
    if '|' in group_content:
        options = [opt for opt in group_content.split('|') if opt]
        if not options:
            raise ValueError("Empty alternation group")
            
        self._log_step(f"Alternation: choosing from {options}")
        selected = random.choice(options)
        
        # Recursively process the selected option
        generated = self._generate_from_pattern(selected)
    else:
        # No alternation - process entire group
        generated = self._generate_from_pattern(group_content)
    
    # Apply quantifier if present
    if quantifier:
        generated = self._apply_quantifier(generated, quantifier)
        
    return generated
```


### Results

The generator successfully handles all three complex regex patterns:

* (a|b)(c|d)E*G → acEG, bcG, adEEEG

* P(Q|R|S)T(UV|W|X)*Z+ → PQTUVZ, PRTZ, PSTXXZZ

* 1(0|1)*2(3|4){5}36 → 1023333336, 1124444436

Validation confirms all generated strings match their respective patterns. The processing steps provide clear insight into the generation sequence.


```
=== Testing regex: (a|b)(c|d)E*G ===
Expected examples: ['acEG', 'bdE', 'adEEG']

Generated strings:
- bcEG

Processing steps:
  Processing group: (a|b)
  Selecting one option from: ['a', 'b']
  Added character: b
  Processing group: (c|d)
  Selecting one option from: ['c', 'd']
  Added character: c
  Processing quantified character: E*
  Applying * quantifier (0 to 5 times)
  Added character: G

- bdEEEEEG
- bdEEEEEG
- bdEEEEEG
- acEEEG

Validation:
- 'acEG' is valid
- 'bdE' is invalid
- 'adEEG' is valid

```

#### Key takeaways from the implementation:

* Recursive Processing: Handles nested structures by recursively processing groups

* Quantifier Limits: Strict enforcement of maximum repetitions

* Validation System: Ensures generated strings actually match the patterns

* Step Tracking: Detailed logging of generation decisions

* Error Handling: Graceful handling of invalid patterns



### Conclusion
Regular expression generation serves as a practical application of formal language theory. Through this laboratory work, I've demonstrated a dynamic approach to interpreting and generating strings from regular expressions, showcasing how abstract patterns can be transformed into concrete outputs. The implementation bridges theoretical concepts with practical software development.
The work highlights how theoretical computer science principles directly enable practical solutions for automated test case generation and other applications requiring structured string production. The processing step visualization particularly helps demystify how regular expressions are interpreted and executed.

Through this project, I've gained deeper insight into both the capabilities and limitations of regular expressions as a generative grammar, while developing a tool that could be extended for more advanced language processing tasks.
### References
[1] Regular Expressions - Wikipedia
[2] Introduction to Automata Theory - Hopcroft & Ullman
[3] Python re module documentation