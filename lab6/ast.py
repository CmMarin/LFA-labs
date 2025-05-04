from dataclasses import dataclass
from typing import List, Optional, Union


# AST Node Definitions
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


class RecipeParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

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
        # Start parsing the recipe
        title = self.parse_title()
        metadata = self.parse_metadata()
        ingredients = self.parse_ingredients_section()
        instructions = self.parse_instructions_section()
        notes = self.parse_notes()

        return Recipe(
            title=title,
            metadata=metadata,
            ingredients=ingredients,
            instructions=instructions,
            notes=notes
        )

    def parse_title(self):
        if self.current_token and self.current_token.type == TokenType.TITLE:
            title = Title(self.current_token.value)
            self.advance()
            return title
        raise SyntaxError("Expected recipe title")

    def parse_metadata(self):
        metadata = Metadata()

        while self.current_token and self.current_token.type in {
            TokenType.SERVINGS,
            TokenType.COOKING_TIME,
            TokenType.TEMPERATURE
        }:
            if self.current_token.type == TokenType.SERVINGS:
                metadata.servings = Servings(self.current_token.value)
                self.advance()
            elif self.current_token.type == TokenType.COOKING_TIME:
                # Check if it's prep time or cook time
                if "prep" in self.current_token.value.lower():
                    metadata.prep_time = Time(self.current_token.value)
                else:
                    metadata.cook_time = Time(self.current_token.value)
                self.advance()
            elif self.current_token.type == TokenType.TEMPERATURE:
                metadata.temperature = Temperature(self.current_token.value)
                self.advance()

        return metadata

    def parse_ingredients_section(self):
        # Skip section header if present
        if self.current_token and self.current_token.type == TokenType.SECTION_HEADER:
            if "ingredients" in self.current_token.value.lower():
                self.advance()

        ingredients = []
        while self.current_token and (
                self.current_token.type == TokenType.INGREDIENT_AMOUNT or
                (self.current_token.type == TokenType.INGREDIENT_NAME and
                 not (self.peek() and self.peek().type == TokenType.SECTION_HEADER))
        ):
            amount = None
            unit = None
            name = None

            if self.current_token.type == TokenType.INGREDIENT_AMOUNT:
                amount = self.current_token.value
                self.advance()

                if self.current_token and self.current_token.type == TokenType.INGREDIENT_UNIT:
                    unit = self.current_token.value
                    self.advance()

            if self.current_token and self.current_token.type == TokenType.INGREDIENT_NAME:
                name = self.current_token.value
                self.advance()

            if name:  # At least the name should be present
                ingredients.append(Ingredient(amount=amount, unit=unit, name=name))

        return IngredientsSection(ingredients)

    def parse_instructions_section(self):
        # Skip section header if present
        if self.current_token and self.current_token.type == TokenType.SECTION_HEADER:
            if "instructions" in self.current_token.value.lower() or "steps" in self.current_token.value.lower():
                self.advance()

        steps = []
        while self.current_token and (
                self.current_token.type == TokenType.INSTRUCTION_STEP or
                (self.current_token.type == TokenType.TEMPERATURE and
                 "preheat" in self.current_token.value.lower()) or
                not (self.peek() and self.peek().type in {TokenType.SECTION_HEADER, TokenType.NOTE})
        ):
            if self.current_token.type == TokenType.INSTRUCTION_STEP:
                steps.append(InstructionStep(self.current_token.value))
                self.advance()
            elif self.current_token.type == TokenType.TEMPERATURE and "preheat" in self.current_token.value.lower():
                # Special case for preheat instructions
                steps.append(InstructionStep(f"Preheat to {self.current_token.value}"))
                self.advance()
            else:
                # Skip unexpected tokens in instructions
                self.advance()

        return InstructionsSection(steps)

    def parse_notes(self):
        notes = []
        while self.current_token and self.current_token.type == TokenType.NOTE:
            notes.append(Note(self.current_token.value))
            self.advance()
        return notes


# Example usage with your existing lexer
if __name__ == "__main__":
    from recipe_lexer import RecipeLexer, TokenType, Token

    sample_recipe = """# Classic Chocolate Chip Cookies

Serves: 24 cookies
Prep time: 15 minutes
Cook time: 10 minute

## Ingredients
2 1/4 cups all-purpose flour
1/2 teaspoon baking soda
1 cup unsalted butter, softened
1/2 cup granulated sugar
1 cup packed brown sugar
1 teaspoon salt
2 teaspoons vanilla extract
2 large eggs
2 cups semi-sweet chocolate chips

## Instructions
1. Preheat oven to 375°F
2. Combine flour and baking soda in a small bowl
3. Beat butter, both sugars, and salt in a large mixer bowl
4. Add vanilla and eggs one at a time, mixing well
5. Gradually beat in flour mixture
6. Stir in chocolate chips
7. Drop by rounded tablespoon onto baking sheets
8. Bake for 9 to 11 minutes until golden brown
9. Cool on baking sheets for 2 minutes, then transfer to wire racks

Note: For softer cookies, bake for 8 minutes instead.
Tip: Add 1/2 cup of chopped nuts for extra texture.
"""

    lexer = RecipeLexer()
    tokens = lexer.tokenize(sample_recipe)

    print("=== Tokens ===")
    for token in tokens:
        print(token)

    print("\n=== AST ===")
    parser = RecipeParser(tokens)
    ast = parser.parse()


    # Pretty print the AST
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


    print_ast(ast)