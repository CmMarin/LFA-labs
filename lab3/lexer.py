class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t\n':
                self.advance()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
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

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token('INTEGER', int(num_str))
        else:
            return Token('FLOAT', float(num_str))

    def make_identifier(self):
        id_str = ''

        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()

        keywords = {
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'func': 'FUNC',
            'return': 'RETURN',
            'print': 'PRINT',
            'true': 'TRUE',
            'false': 'FALSE',
            'null': 'NULL'
        }

        return Token(keywords.get(id_str, 'IDENTIFIER'), id_str)

    def make_string(self):
        self.advance()  # Skip opening quote
        str_str = ''

        while self.current_char and self.current_char != '"':
            str_str += self.current_char
            self.advance()

        if self.current_char == '"':
            self.advance()  # Skip closing quote
        else:
            raise Exception("Unterminated string literal")

        return Token('STRING', str_str)

    def make_operator(self):
        op = self.current_char
        self.advance()

        operators = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '%': 'MODULO',
            '=': 'ASSIGN',
            '!': 'NOT',
            '<': 'LT',
            '>': 'GT',
        }

        # Check for multi-character operators
        if op + (self.current_char or '') in ['==', '!=', '<=', '>=']:
            op += self.current_char
            self.advance()
            return Token('COMPARISON', op)
        elif op in ['=', '!', '<', '>'] and self.current_char == '=':
            op += self.current_char
            self.advance()
            return Token('COMPARISON', op)

        return Token(operators.get(op, 'OPERATOR'), op)

    def make_symbol(self):
        symbols = {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LBRACE',
            '}': 'RBRACE',
            '[': 'LBRACKET',
            ']': 'RBRACKET',
            ',': 'COMMA',
            ';': 'SEMICOLON',
            ':': 'COLON'
        }
        tok = Token(symbols[self.current_char], self.current_char)
        self.advance()
        return tok

    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
        self.advance()  # Skip the newline character


# Example usage
if __name__ == '__main__':
    code = """
    # This is a comment
    func factorial(n) {
        if n <= 1 return 1
        else return n * factorial(n - 1)
    }
    print("Factorial of 5 is: ", factorial(5))
    """

    lexer = Lexer(code)
    tokens = lexer.make_tokens()

    for token in tokens:
        print(token)