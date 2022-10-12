from lexer import *

file = open('code.txt', 'r')
lines = file.readlines()

for line in lines:
    lexer = Lexer('filename', line)
    tokens, error = lexer.make_tokens()
    if error is None:
        print(tokens)
    else:
        print(tokens, error.as_string())
        



