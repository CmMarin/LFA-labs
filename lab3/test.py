import unittest
from recipe_lexer import RecipeLexer, TokenType


class TestRecipeLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = RecipeLexer()

    def test_title_tokenization(self):
        text = "# Banana Bread Recipe"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.TITLE)
        self.assertEqual(tokens[0].value, "Banana Bread Recipe")

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

    def test_fraction_ingredient(self):
        text = "1/2 cup butter, softened"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.INGREDIENT_AMOUNT)
        self.assertEqual(tokens[0].value, "1/2")
        self.assertEqual(tokens[1].type, TokenType.INGREDIENT_UNIT)
        self.assertEqual(tokens[1].value, "cup")

    def test_instruction_tokenization(self):
        text = "1. Mix the dry ingredients in a bowl."
        tokens = self.lexer.tokenize(text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.INSTRUCTION_STEP)
        self.assertEqual(tokens[0].value, "Mix the dry ingredients in a bowl.")

    def test_cooking_time(self):
        text = "Cook time: 30 minute"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.COOKING_TIME)
        self.assertEqual(tokens[0].value, "30 minute")

    def test_temperature(self):
        text = "Preheat the oven to 350°F"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.TEMPERATURE)
        self.assertEqual(tokens[0].value, "350°F")

        text = "Bake at 180 degrees C for 25 minutes"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.INSTRUCTION_STEP)
        self.assertTrue("180 degrees C" in tokens[0].value)

    def test_servings(self):
        text = "Servings: 4-6"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.SERVINGS)
        self.assertEqual(tokens[0].value, "4-6")

    def test_section_header(self):
        text = "## Instructions"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.SECTION_HEADER)
        self.assertEqual(tokens[0].value, "Instructions")

    def test_note(self):
        text = "Note: Store in an airtight container."
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.NOTE)
        self.assertEqual(tokens[0].value, "Store in an airtight container.")

    def test_complex_ingredient(self):
        text = "1 1/2 cups diced tomatoes, drained"
        tokens = self.lexer.tokenize(text)
        self.assertEqual(tokens[0].type, TokenType.INGREDIENT_AMOUNT)
        self.assertEqual(tokens[0].value, "1 1/2")
        self.assertEqual(tokens[1].type, TokenType.INGREDIENT_UNIT)
        self.assertEqual(tokens[1].value, "cups")
        self.assertEqual(tokens[2].type, TokenType.INGREDIENT_NAME)
        self.assertEqual(tokens[2].value, "diced tomatoes, drained")


if __name__ == "__main__":
    unittest.main()