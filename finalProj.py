import re

# Token definitions
tokens = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('ID', r'id'),
    ('WHITESPACE', r'\s+'),
]

# Regular expression to match tokens
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)

# Lexical analyzer
def tokenize(source_code):
    line_num = 1
    line_start = 0
    for mo in re.finditer(token_regex, source_code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'WHITESPACE':
            continue
        elif kind == 'NUMBER':
            yield ('NUMBER', value)
        elif kind == 'PLUS':
            yield ('PLUS', value)
        elif kind == 'MINUS':
            yield ('MINUS', value)
        elif kind == 'TIMES':
            yield ('TIMES', value)
        elif kind == 'DIVIDE':
            yield ('DIVIDE', value)
        elif kind == 'LPAREN':
            yield ('LPAREN', value)
        elif kind == 'RPAREN':
            yield ('RPAREN', value)
        elif kind == 'ID':
            yield ('ID', value)

# Parser based on recursive descent
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_iter = iter(self.tokens)
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.token_iter)
        except StopIteration:
            self.current_token = None

    def parse(self):
        return self.expr()

    def expr(self):
        term_node = self.term()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            operator = self.current_token
            self.advance()
            term_node = ('binary_op', operator[0], term_node, self.term())
        return term_node

    def term(self):
        factor_node = self.factor()
        while self.current_token and self.current_token[0] in ('TIMES', 'DIVIDE'):
            operator = self.current_token
            self.advance()
            factor_node = ('binary_op', operator[0], factor_node, self.factor())
        return factor_node

    def factor(self):
        if self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self.advance()
            return ('number', value)
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr_node = self.expr()
            if self.current_token[0] == 'RPAREN':
                self.advance()
                return expr_node
            else:
                raise SyntaxError("Expected ')'")
        else:
            raise SyntaxError("Unexpected token: {}".format(self.current_token))

# Code generator for three-address code
class CodeGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.instructions = []

    def generate_temp(self):
        self.temp_counter += 1
        return f'temp{self.temp_counter}'

    def generate_code(self, ast):
        if ast[0] == 'number':
            return ast[1]
        elif ast[0] == 'binary_op':
            left = self.generate_code(ast[2])
            right = self.generate_code(ast[3])
            temp_var = self.generate_temp()
            self.instructions.append(f'{temp_var} = {left} {ast[1]} {right}')
            return temp_var

    def get_instructions(self):
        return self.instructions

# Main function
def main():
    source_code = '4+7*14+(7+6)*3'
    
    # Step 1: Tokenize the input source code
    tokens = list(tokenize(source_code))
    
    # Output Lexical Analyzer Results
    print("Lexical Analyzer Output (Tokens):")
    print(tokens)
    
    # Step 2: Parse the tokens to generate the AST
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Output Parser Results (Abstract Syntax Tree - AST)
    print("\nParser Output (Abstract Syntax Tree):")
    print(ast)
    
    # Step 3: Generate intermediate code
    code_gen = CodeGenerator()
    code_gen.generate_code(ast)
    instructions = code_gen.get_instructions()
    
    # Output Code Generator Results (Intermediate Code)
    print("\nCode Generator Output (Intermediate Code):")
    for instruction in instructions:
        print(instruction)

if __name__ == '__main__':
    main()
