# Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata  
### Author: Clima Marin

---

## 1. Theory

Parsing is a fundamental phase in the process of compilation and interpretation of programming languages. It refers to the syntactic analysis of a sequence of tokens to determine their grammatical structure with respect to a given formal grammar. The output of this analysis is usually a tree-based structure known as a parse tree or an abstract syntax tree (AST).

While a parse tree contains all the syntactic details as per the grammar, an Abstract Syntax Tree is a condensed version that abstracts away unnecessary syntactic details to focus on the structure and semantics. The AST provides a hierarchical representation of program constructs and is often used for semantic analysis, optimization, and code generation in compilers.

A parser is typically built upon a lexer, which tokenizes the raw input text into a stream of tokens. The parser then uses grammar rules to analyze this stream and construct the corresponding AST. Regular expressions are often used in the lexical analysis phase to match token types.

---

## 2. Objectives

- Understand the concept of parsing and its application in syntactic analysis.
- Learn the structure and use of Abstract Syntax Trees.
- Extend lexical analysis using `TokenType` enums with regular expressions.
- Build data structures for AST and implement a parser to extract syntax from processed text.

---

## 3. Code

### 3.1 Lexer Part

#### 3.1.1 Token Type Definition

In this lab, a TokenType enum is introduced to categorize lexical units like KEYWORD, IDENTIFIER, NUMBER, etc. Regular expressions are used to match these types during tokenization.

```python
    class TokenType(Enum):
    TITLE = auto()
    INGREDIENT_AMOUNT = auto()
    INGREDIENT_UNIT = auto()
    INGREDIENT_NAME = auto()
    INSTRUCTION_STEP = auto()
    COOKING_TIME = auto()
    TEMPERATURE = auto()
    SERVINGS = auto()
    SECTION_HEADER = auto()
    NOTE = auto()
    UNKNOWN = auto()
```    

The lexer (from Lab 3) reads a pseudo-recipe input and tokenizes it based on patterns. It uses regular expressions to classify each token by its type and stores token metadata (type, value, and position).

```python
    def __init__(self):
        self.units = [
            "cup", "cups", "tablespoon", "tablespoons", "tbsp", "teaspoon", "teaspoons", "tsp",
            "ounce", "ounces", "oz", "pound", "pounds", "lb", "lbs", "gram", "grams", "g",
            "kilogram", "kilograms", "kg", "ml", "milliliter", "milliliters", "liter", "liters",
            "l", "pinch", "pinches", "dash", "dashes", "clove", "cloves", "bunch", "bunches",
            "slice", "slices", "package", "pkg", "can", "cans", "bottle", "bottles"
        ]

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


### 3.2 AST Part

#### 3.2.1 AST Node Definitions

We define a base class ASTNode, and specialized subclasses such as:

- NumberNode

- IngredientNode

- InstructionNode

- RecipeNode

These classes contain node-specific information and a method to format the AST in a readable structure.

```python
    @dataclass
    class RecipeNode:
        """Base class for all AST nodes"""
        pass


    @dataclass
    class Recipe(RecipeNode):
        title: 'Title'
        metadata: 'Metadata'
        ingredients: 'IngredientsSection'
        instructions: 'InstructionsSection'
        notes: List['Note']


    @dataclass
    class Title(RecipeNode):
        value: str


    @dataclass
    class Metadata(RecipeNode):
        servings: Optional['Servings'] = None
        prep_time: Optional['Time'] = None
        cook_time: Optional['Time'] = None
        temperature: Optional['Temperature'] = None


    @dataclass
    class Servings(RecipeNode):
        value: str


    @dataclass
    class Time(RecipeNode):
        value: str


    @dataclass
    class Temperature(RecipeNode):
        value: str


    @dataclass
    class IngredientsSection(RecipeNode):
        ingredients: List['Ingredient']


    @dataclass
    class Ingredient(RecipeNode):
        amount: Optional[str]
        unit: Optional[str]
        name: str


    @dataclass
    class InstructionsSection(RecipeNode):
        steps: List['InstructionStep']


    @dataclass
    class InstructionStep(RecipeNode):
        text: str


    @dataclass
    class Note(RecipeNode):
        text: str
```

#### 3.2.2 Parser Core Components
The Parser class is introduced, which takes a list of tokens and iterates through them using an index pointer. It includes error handling for syntax inconsistencies and functions to check or consume specific tokens.

```python
 def parse_metadata(self):
        metadata = Metadata()

        while self.current_token and self.current_token.type in {
            TokenType.SERVINGS,
            TokenType.COOKING_TIME,
            TokenType.TEMPERATURE
        }:
            {...}

        return metadata
```

```python
    def parse_title(self):
        if self.current_token and self.current_token.type == TokenType.TITLE:
            title = Title(self.current_token.value)
            self.advance()
            return title
        raise SyntaxError("Expected recipe title")

```

#### 3.2.3 Parsing Methods
The following parsing methods are implemented:

- parse() – Entry point; starts parsing and builds the full AST.

- parse_ingredient() – Parses ingredient declarations.

- parse_instruction() – Parses procedural instructions.

- parse_number() – Converts tokens to NumberNode.

Each method performs type checking and node construction based on expected token sequences.
```python
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
        return self.current_token

    def peek(self):
        peek_index = self.token_index + 1
        if peek_index < len(self.tokens):
            return self.tokens[peek_index]
        return None

    def parse(self):
        title = self.parse_title()
        metadata = self.parse_metadata()
        ingredients = self.parse_ingredients_section()
        instructions = self.parse_instructions_section()
        notes = self.parse_notes()
```

#### 3.2.4 AST Visualization
Each node class implements a pretty_print() method, which recursively prints the AST in a structured format, using indentation to show hierarchy.
```python
    def print_ast(node, indent=0):
        if isinstance(node, list):
            for item in node:
                print_ast(item, indent)
            return

        print("  " * indent + node.__class__.__name__)
        for field in node.__dataclass_fields__:
            value = getattr(node, field)
            if isinstance(value, (RecipeNode, list)):
                print("  " * (indent + 1) + f"{field}:")
                print_ast(value, indent + 2)
            elif value is not None:
                print("  " * (indent + 1) + f"{field}: {value}")
```

---

## 4. Results

The parser successfully converts a stream of tokens derived from recipe text into a hierarchical AST structure. This allows further semantic processing and transformations as part of compilation-like workflows.

```python
=== AST ===
Recipe
  title:
    Title
      value: Classic Chocolate Chip Cookies
  metadata:
    Metadata
      servings:
        Servings
          value: 24
      cook_time:
        Time
          value: 10 minute
  ingredients:
    IngredientsSection
      ingredients:
        Ingredient
          amount: 2 1/4
          unit: cups
          name: all-purpose flour
        Ingredient
          amount: 1/2
          unit: teaspoon
          name: baking soda
        Ingredient
          amount: 1
          unit: cup
          name: unsalted butter, softened
        Ingredient
          amount: 1/2
          unit: cup
          name: granulated sugar
        Ingredient
          amount: 1
          unit: cup
          name: packed brown sugar
        Ingredient
          amount: 1
          unit: teaspoon
          name: salt
        Ingredient
          amount: 2
          unit: teaspoons
          name: vanilla extract
        Ingredient
          amount: 2
          name: large eggs
        Ingredient
          amount: 2
          unit: cups
          name: semi-sweet chocolate chips
  instructions:
    InstructionsSection
      steps:
        InstructionStep
          text: Preheat oven to 375°F
        InstructionStep
          text: Combine flour and baking soda in a small bowl
        InstructionStep
          text: Beat butter, both sugars, and salt in a large mixer bowl
        InstructionStep
          text: Add vanilla and eggs one at a time, mixing well
        InstructionStep
          text: Gradually beat in flour mixture
        InstructionStep
          text: Stir in chocolate chips
        InstructionStep
          text: Drop by rounded tablespoon onto baking sheets
        InstructionStep
          text: Bake for 9 to 11 minutes until golden brown
        InstructionStep
          text: Cool on baking sheets for 2 minutes, then transfer to wire racks
  notes:
    Note
      text: For softer cookies, bake for 8 minutes instead.
    Note
      text: Add 1/2 cup of chopped nuts for extra texture.
```

---

## 5. Conclusion

In this laboratory, we implemented a lexical analyzer with categorized token types and extended our project to support parsing and AST construction. The parsing process enabled a deeper syntactic understanding of structured text, simulating how compilers process programming languages. Building the AST proved to be a valuable step toward interpreting and analyzing domain-specific inputs, like recipes, in a structured manner.

---

## 6. References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, & Tools* (2nd ed.). Pearson.
2. Grune, D., van Reeuwijk, K., Bal, H. E., Jacobs, C. J., & Langendoen, K. (2012). *Modern Compiler Design*. Springer.
3. Python Official Documentation - https://docs.python.org/3/
4. Irina Cojuhari, Dumitru Crețu - Laboratory materials

---
