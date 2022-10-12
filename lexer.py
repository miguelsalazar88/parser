from strings_with_arrows import *

import string

#######################################
# CONSTANTES
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POW = 'POW'
TT_EQUAL = 'EQUAL'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_EOF = 'EOF'

# Faltan
TT_COMMA = 'COMMA'
TT_COLON = 'COLON'
TT_SEMICOLON = 'SEMICOLON'
TT_LBRACKET = 'LBRACKET'
TT_RBRACKET = 'RBRACKET'
TT_LBRACE = 'LBRACE'
TT_RBRACE = 'RBRACE'
TT_COMMENT = 'COMMENT'
TT_TAB = 'TAB'
TT_DOT = 'DOT'
TT_EOL = 'EOL'

# PARA HACER:
# OMITIR COMENTARIOS
# INCLUIR COMA
# INCLUIR COLON
# INCLUIR SEMICOLON
# INCLUIR LBRACKET
# INCLUIR RBRACKET
# INCLUIR LBRACE
# INCLUIR RBRACE
#


KEYWORDS = {
	'range': 'TT_RANGE',
	'False': 'TT_FALSE',
	'def': 'TT_DEF',
	'if': 'TT_IF',
	'raise': 'TT_RAISE',
	'None': 'TT_NONE',
	'del': 'TT_DEL',
	'import': 'TT_IMPORT',
	'return': 'TT_RETURN',
	'True': 'TT_TRUE',
	'elif': 'TT_ELIF',
	'in': 'TT_IN',
	'try': 'TT_TRY',
	'and': 'TT_AND',
	'else': 'TT_ELSE',
	'is': 'TT_IS',
	'while': 'TT_WHILE',
	'as': 'TT_AS',
	'except': 'TT_EXCEPT',
	'lambda': 'TT_LAMBDA',
	'with': 'TT_WITH',
	'assert': 'TT_ASSERT',
	'finally': 'TT_FINALLY',
	'nonlocal': 'TT_NONLOCAL',
	'yield': 'TT_YIELD',
	'break': 'TT_BREAK',
	'for': 'TT_FOR',
	'not': 'TT_NOT',
	'class': 'TT_CLASS',
	'from': 'TT_FROM',
	'or': 'TT_OR',
	'continue': 'TT_CONTINUE',
	'global': 'TT_GLOBAL',
	'pass': 'TT_PASS',
	'self': 'TT_SELF',
	'__peg_parser__': 'TT_PEG',
	'async': 'TT_ASYNC'
}

####################################
# CLASE TOKEN 
####################################

class Token:
	def __init__(self, type_, value=None, pos_start=None, pos_end=None):
		self.type = type_
		self.value = value

		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()

		if pos_end:
			self.pos_end = pos_end.copy()

	def matches(self, type_, value):
		return self.type == type_ and self.value == value

	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'

#######################################
# CLASE LEXER
#######################################


class Lexer:
	def __init__(self, fn, text): # fn = file name
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			# Espacio
			if self.current_char in ' ':
				self.advance()
			# Tab
			elif self.current_char in '\t': # No reconoce el tab!!!!!!
				tokens.append(Token(TT_TAB, pos_start=self.pos))
				self.advance()
			# Salto de linea
			elif self.current_char in '\n':
				tokens.append(Token(TT_EOL, pos_start=self.pos))
				self.advance()
			# Comentario	
			elif self.current_char in '#':
				while self.current_char != '\n':
					self.advance()
			# Coma
			elif self.current_char in ',':
				tokens.append(Token(TT_COMMA, pos_start=self.pos))
				self.advance()
			# COLON
			elif self.current_char in ':':
				tokens.append(Token(TT_COLON, pos_start=self.pos))
				self.advance()
			# SEMICOLON
			elif self.current_char in ';':
				tokens.append(Token(TT_SEMICOLON, pos_start=self.pos))
				self.advance()
			# LBRACKET
			elif self.current_char in '[':
				tokens.append(Token(TT_LBRACKET, pos_start=self.pos))
				self.advance()
			# RBRACKET
			elif self.current_char in ']':
				tokens.append(Token(TT_RBRACKET, pos_start=self.pos))
				self.advance()
			# LBRACE
			elif self.current_char in '{':
				tokens.append(Token(TT_LBRACE, pos_start=self.pos))
				self.advance()
			# INCLUIR RBRACE
			elif self.current_char in '}':
				tokens.append(Token(TT_RBRACE, pos_start=self.pos))
				self.advance()
			elif self.current_char in '.':
				tokens.append(Token(TT_DOT, pos_start=self.pos))
				self.advance()
			
			# Números
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char in LETTERS:
				tokens.append(self.make_identifier())
			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS, pos_start=self.pos))
				self.advance()
			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS, pos_start=self.pos))
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(TT_MUL, pos_start=self.pos))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(TT_DIV, pos_start=self.pos))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(TT_POW, pos_start=self.pos))
				self.advance()
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN, pos_start=self.pos))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN, pos_start=self.pos))
				self.advance()
			elif self.current_char == '!':
				token, error = self.make_not_equals()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == '=':
				tokens.append(self.make_equals())
			elif self.current_char == '<':
				tokens.append(self.make_less_than())
			elif self.current_char == '>':
				tokens.append(self.make_greater_than())
			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

		return tokens, None

	def make_number(self):
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
			num_str += self.current_char
			self.advance()

		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

	def make_identifier(self):
		id_str = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.advance()
		if id_str in KEYWORDS:
			tok_type = KEYWORDS[id_str] 
			return(Token(tok_type, pos_start=pos_start, pos_end=self.pos))
		else:
			tok_type = TT_IDENTIFIER
			return Token(tok_type, id_str, pos_start, self.pos)

	def make_not_equals(self):
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

		self.advance()
		return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")
	
	def make_equals(self):
		tok_type = TT_EQUAL
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_EE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_less_than(self):
		tok_type = TT_LT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_LTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_greater_than(self):
		tok_type = TT_GT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_GTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

################################################
# CLASE ERROR Y SUS SUBCLASES
################################################

class Error:
	def __init__(self, pos_start, pos_end, error_name, details):
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.error_name = error_name
		self.details = details
	
	def as_string(self):
		result  = f'{self.error_name}: {self.details}\n'
		result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

class IllegalCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
	def __init__(self, pos_start, pos_end, details=''):
		super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result

#######################################
# POSICION
#######################################

class Position:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

	def advance(self, current_char=None):
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0

		return self

	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)