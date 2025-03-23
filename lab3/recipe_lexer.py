import re
from enum import Enum, auto
from dataclasses import dataclass


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


@dataclass
class Token:
    type: TokenType
    value: str
    line_number: int

    def __str__(self):
        return f"Token({self.type.name}, '{self.value}', line {self.line_number})"


class RecipeLexer:
    def __init__(self):
        # Common ingredient units
        self.units = [
            "cup", "cups", "tablespoon", "tablespoons", "tbsp", "teaspoon", "teaspoons", "tsp",
            "ounce", "ounces", "oz", "pound", "pounds", "lb", "lbs", "gram", "grams", "g",
            "kilogram", "kilograms", "kg", "ml", "milliliter", "milliliters", "liter", "liters",
            "l", "pinch", "pinches", "dash", "dashes", "clove", "cloves", "bunch", "bunches",
            "slice", "slices", "package", "pkg", "can", "cans", "bottle", "bottles"
        ]

        # Patterns for different token types
        self.patterns = {
            TokenType.TITLE: r'^#\s+(.+)$',
            TokenType.INGREDIENT_AMOUNT: r'^([\d¼½¾⅓⅔⅛⅜⅝⅞]+(?:\s*-\s*[\d¼½¾⅓⅔⅛⅜⅝⅞]+)?(?:\s*\d+/\d+)?)(?:\s+|$)',
            TokenType.COOKING_TIME: r'(?:cook|bake|simmer|boil|prep|total)\s+time:?\s*(\d+\s*(?:minute|minutes|mins|min|hour|hours|hr|hrs)(?:\s+\d+\s*(?:minute|minutes|mins|min))?)',
            TokenType.TEMPERATURE: r'(\d+(?:\s*°[CF]|\s*degrees\s*[CF]?))',
            TokenType.SERVINGS: r'(?:serves|servings|yield):?\s*(\d+(?:-\d+)?)(?:\s+people)?',
            TokenType.SECTION_HEADER: r'^##\s+(.+)$',
            TokenType.NOTE: r'^(?:Note|Tip):?\s*(.+)$',
        }

    def is_unit(self, word):
        return word.lower() in self.units

    def tokenize(self, recipe_text):
        tokens = []
        lines = recipe_text.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            # Try to match the line against known patterns
            matched = False

            # Check for title (lines starting with # )
            title_match = re.match(self.patterns[TokenType.TITLE], line)
            if title_match:
                tokens.append(Token(TokenType.TITLE, title_match.group(1).strip(), line_num))
                matched = True
                continue

            # Check for section headers (lines starting with ## )
            section_match = re.match(self.patterns[TokenType.SECTION_HEADER], line)
            if section_match:
                tokens.append(Token(TokenType.SECTION_HEADER, section_match.group(1).strip(), line_num))
                matched = True
                continue

            # Check for cooking time
            time_match = re.search(self.patterns[TokenType.COOKING_TIME], line, re.IGNORECASE)
            if time_match:
                tokens.append(Token(TokenType.COOKING_TIME, time_match.group(1).strip(), line_num))
                matched = True
                continue

            # Check for servings
            servings_match = re.search(self.patterns[TokenType.SERVINGS], line, re.IGNORECASE)
            if servings_match:
                tokens.append(Token(TokenType.SERVINGS, servings_match.group(1).strip(), line_num))
                matched = True
                continue

            # Check for temperature that is a standalone instruction (like "Preheat to 350°F")
            temp_match = re.search(self.patterns[TokenType.TEMPERATURE], line)
            if temp_match and not line.startswith("1") and "preheat" in line.lower():
                tokens.append(Token(TokenType.TEMPERATURE, temp_match.group(1).strip(), line_num))
                matched = True
                continue

            # Check for notes
            note_match = re.match(self.patterns[TokenType.NOTE], line, re.IGNORECASE)
            if note_match:
                tokens.append(Token(TokenType.NOTE, note_match.group(1).strip(), line_num))
                matched = True
                continue

            # Check for ingredients (typically starts with a number or fraction)
            amount_match = re.match(self.patterns[TokenType.INGREDIENT_AMOUNT], line)
            if amount_match and not matched:
                amount = amount_match.group(1).strip()
                tokens.append(Token(TokenType.INGREDIENT_AMOUNT, amount, line_num))

                # Process the rest of the line for unit and ingredient name
                remaining = line[len(amount_match.group(0)):].strip()
                words = remaining.split()

                if words and self.is_unit(words[0]):
                    tokens.append(Token(TokenType.INGREDIENT_UNIT, words[0], line_num))
                    ingredient_name = ' '.join(words[1:])
                else:
                    ingredient_name = remaining

                if ingredient_name:
                    tokens.append(Token(TokenType.INGREDIENT_NAME, ingredient_name, line_num))

                matched = True
                continue

            # Handle special case for fractions like 1/2 which might not be matched above
            fraction_match = re.match(r'^(\d+/\d+)\s+(.+)$', line)
            if fraction_match and not matched:
                tokens.append(Token(TokenType.INGREDIENT_AMOUNT, fraction_match.group(1), line_num))

                remaining = fraction_match.group(2).strip()
                words = remaining.split()

                if words and self.is_unit(words[0]):
                    tokens.append(Token(TokenType.INGREDIENT_UNIT, words[0], line_num))
                    ingredient_name = ' '.join(words[1:])
                else:
                    ingredient_name = remaining

                if ingredient_name:
                    tokens.append(Token(TokenType.INGREDIENT_NAME, ingredient_name, line_num))

                matched = True
                continue

            # If no specific pattern matched and not part of an already matched pattern,
            # assume it's an instruction step
            if not matched:
                # Strip number prefixes like "1." or "Step 1:"
                clean_line = re.sub(r'^(?:\d+\.|\(\d+\)|Step\s+\d+:)\s*', '', line)
                tokens.append(Token(TokenType.INSTRUCTION_STEP, clean_line, line_num))

        return tokens


if __name__ == "__main__":
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