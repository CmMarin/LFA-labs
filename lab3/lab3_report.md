# Lexical Analysis: Implementation and Demonstration

### Course: Formal Languages & Finite Automata
### Author: [Clima Marin]

----

## Theory
Lexical analysis is the first phase of a compiler or interpreter, responsible for converting a sequence of characters into a sequence of tokens. This process, also known as tokenization, breaks down source code into meaningful units (tokens) that can be processed by subsequent phases of compilation. A lexer (also called scanner or tokenizer) is the software component that performs this task.

Key components of lexical analysis include:

1. **Tokens**: Atomic units of a programming language (identifiers, keywords, operators, literals, etc.)
2. **Lexical patterns**: Rules defining the structure of each token type
3. **Recognition**: The process of identifying tokens in the input stream
4. **State transitions**: How the lexer moves between states as it processes input

## Objectives:

1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Implementation description

For this laboratory work, I implemented two different lexers to demonstrate the principles of lexical analysis:

1. A general-purpose lexer for a programming language (`lexer.py`)
2. A specialized lexer for parsing cooking recipes (`recipe_lexer.py`)

### General-Purpose Lexer Implementation

The general-purpose lexer is designed to tokenize code in a simple programming language. It recognizes various token types including:

- Keywords (`if`, `else`, `while`, etc.)
- Identifiers (variable names)
- Literals (numbers, strings)
- Operators (`+`, `-`, `*`, etc.)
- Symbols (`(`, `)`, `{`, etc.)

The lexer works by scanning the input character by character and applying pattern matching rules to identify tokens. It employs a state-based approach where the current character and context determine the lexer's next action.

Key components of the implementation include:

### Token Class
```python
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}' 
   ```

The Token class represents individual tokens with a type and optional value. The string representation makes debugging easier by providing a clear view of the token's properties.

### Lexer Class
```python 
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
```

The Lexer class initializes with the input text and sets up the position tracker and current character reference. The `advance()` method moves through the input stream.

```python 
def make_tokens(self):
    tokens = []

    while self.current_char is not None:
        if self.current_char in ' \t\n': 
            self.advance()
        elif self.current_char == '#':
            self.skip_comment()
        elif self.current_char.isdigit():
            tokens.append(self.make_number())
        elif self.current_char.isalpha() or self.current_char == '_':
            tokens.append(self.make_identifier())
        elif self.current_char == '"':
            tokens.append(self.make_string())
        elif self.current_char in '+-*/%=!<>':
            tokens.append(self.make_operator())
        elif self.current_char in '(){}[],;:':
            tokens.append(self.make_symbol())
        else:
            raise Exception(f"Illegal character '{self.current_char}'")

    tokens.append(Token('EOF'))
    return tokens
```
The make_tokens() method is the central processing loop that categorizes each character and delegates to specialized methods for constructing specific token types.

### Recipe Lexer Implementation
The recipe lexer is a domain-specific tokenizer designed to parse cooking recipes. It uses regular expressions and pattern matching to identify recipe-specific elements:
Pattern matching is implemented using regular expressions:

```python

self.patterns = {
    TokenType.TITLE: r'^#\s+(.+)$',
    TokenType.INGREDIENT_AMOUNT: r'^([\d¼½¾⅓⅔⅛⅜⅝⅞]+(?:\s*-\s*[\d¼½¾⅓⅔⅛⅜⅝⅞]+)?(?:\s*\d+/\d+)?)(?:\s+|$)',
    TokenType.COOKING_TIME: r'(?:cook|bake|simmer|boil|prep|total)\s+time:?\s*(\d+\s*(?:minute|minutes|mins|min|hour|hours|hr|hrs)(?:\s+\d+\s*(?:minute|minutes|mins|min))?)',
    TokenType.TEMPERATURE: r'(\d+(?:\s*°[CF]|\s*degrees\s*[CF]?))',
    TokenType.SERVINGS: r'(?:serves|servings|yield):?\s*(\d+(?:-\d+)?)(?:\s+people)?',
    TokenType.SECTION_HEADER: r'^##\s+(.+)$',
    TokenType.NOTE: r'^(?:Note|Tip):?\s*(.+)$',
}
```

The recipe lexer processes the input line by line instead of character by character, which is more appropriate for the structured format of recipes:

```python 
def tokenize(self, recipe_text):
    tokens = []
    lines = recipe_text.split('\n')

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        
        matched = False
        
        # Check for various patterns...
```
The tokenization process attempts to match each line against the defined patterns, prioritizing certain patterns over others (e.g., titles before ingredients).

### Unit Testing
To verify the correctness of the recipe lexer, I implemented a suite of unit tests:

```python
def test_ingredient_tokenization(self):
    text = "2 cups flour"
    tokens = self.lexer.tokenize(text)
    self.assertEqual(len(tokens), 3)
    self.assertEqual(tokens[0].type, TokenType.INGREDIENT_AMOUNT)
    self.assertEqual(tokens[0].value, "2")
    self.assertEqual(tokens[1].type, TokenType.INGREDIENT_UNIT)
    self.assertEqual(tokens[1].value, "cups")
    self.assertEqual(tokens[2].type, TokenType.INGREDIENT_NAME)
    self.assertEqual(tokens[2].value, "flour")
```
These tests cover various aspects of recipe tokenization, ensuring that each token type is correctly identified.

### Results
#### General-Purpose Lexer
When running the general-purpose lexer on the sample code provided in lexer.py:

```python
# This is a comment
func factorial(n) {
    if n <= 1 return 1
    else return n * factorial(n - 1)
}
print("Factorial of 5 is: ", factorial(5))
```
The lexer successfully produces the following tokens:

```
FUNC:func
IDENTIFIER:factorial
LPAREN:(
IDENTIFIER:n
RPAREN:)
LBRACE:{
IF:if
IDENTIFIER:n
COMPARISON:<=
INTEGER:1
RETURN:return
INTEGER:1
ELSE:else
RETURN:return
IDENTIFIER:n
MULTIPLY:*
IDENTIFIER:factorial
LPAREN:(
IDENTIFIER:n
MINUS:-
INTEGER:1
RPAREN:)
RBRACE:}
PRINT:print
LPAREN:(
STRING:Factorial of 5 is: 
COMMA:,
IDENTIFIER:factorial
LPAREN:(
INTEGER:5
RPAREN:)
RPAREN:)
EOF
```

#### Recipe Lexer
When running the recipe lexer on the sample recipe:

```
# Classic Chocolate Chip Cookies

Serves: 24 cookies
Prep time: 15 minutes
Cook time: 10 minute

## Ingredients
2 1/4 cups all-purpose flour
...
```

The lexer produces tokens such as:

```
Token(TITLE, 'Classic Chocolate Chip Cookies', line 1)
Token(SERVINGS, '24', line 3)
Token(COOKING_TIME, '15 minutes', line 4)
Token(COOKING_TIME, '10 minute', line 5)
Token(SECTION_HEADER, 'Ingredients', line 7)
Token(INGREDIENT_AMOUNT, '2 1/4', line 8)
Token(INGREDIENT_UNIT, 'cups', line 8)
Token(INGREDIENT_NAME, 'all-purpose flour', line 8)
...
```

#### Unit Test Results
All unit tests for the recipe lexer pass successfully, confirming the correct identification of:

1. Recipe titles and section headers
2. Ingredient amounts, units, and names
3. Cooking times and temperatures
4. Serving information
5. Instruction steps
6. Notes and tips

### Conclusion
Lexical analysis serves as the foundational step in language processing. Through this laboratory work, I've demonstrated two different approaches to implementing lexers, each suited to different contexts. The general-purpose lexer follows a traditional character-by-character approach similar to finite automata, while the recipe lexer uses a more domain-specific, pattern-based approach.
The key insights from this implementation include:

Understanding the tradeoffs between different lexer implementation strategies
Recognizing the importance of clear token definitions and pattern recognition rules
Applying formal language concepts to practical programming scenarios
Appreciating the role of lexical analysis in the broader context of language processing

This work provides a solid foundation for further exploration of compiler design, natural language processing, and domain-specific language development.

### References
[1] A sample of a lexer implementation

[2] Lexical analysis