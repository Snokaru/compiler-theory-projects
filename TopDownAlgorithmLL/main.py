import sys
from enum import Enum, auto

class TokenType(Enum):
    RPAR = auto()
    LPAR = auto()
    PLUS = auto()
    SLASH = auto()
    ASTERISK = auto()
    MINUS = auto()
    IDENTIFIER = auto()
    NUMBER = auto()

class Token:
    def __init__(self, token_type, token_value=None):
        self.token_type = token_type
        self.value = token_value

    def __repr__(self):
        return str(self.value)

class Lexxer:
    def __init__(self, word):
        self.word = list(word)
        self.position = 0

    def parse_tokens(self):
        tokens = []
        position = 0
        for current_letter in self.word:
            if current_letter == '(':
                tokens.append(Token(TokenType.LPAR, '('))
            elif current_letter == ')':
                tokens.append(Token(TokenType.RPAR, ')'))
            elif current_letter == '+':
                tokens.append(Token(TokenType.PLUS, '+'))
            elif current_letter == '/':
                tokens.append(Token(TokenType.SLASH, '/'))
            elif current_letter == '*':
                tokens.append(Token(TokenType.ASTERISK, '*'))
            elif current_letter == '-':
                tokens.append(Token(TokenType.MINUS, '-'))
            elif current_letter.isalpha():
                tokens.append(Token(TokenType.IDENTIFIER, current_letter))
            elif current_letter.isdigit():
                tokens.append(Token(TokenType.NUMBER, int(current_letter)))
        return tokens

def valid_position():
    return position < len(word)

def handle_E(indent): 
    global position
    if valid_position() and (word[position].token_type == TokenType.LPAR or word[position].token_type == TokenType.IDENTIFIER or word[position].token_type == TokenType.NUMBER):
        print(indent * " ", "E->TE'")
        indent += 2
        handle_T(indent)
        handle_E_prime(indent)
        indent -= 2
    else:
        raise Exception("Cuvantul introdus nu este corect sintactic")

def handle_T(indent):
    global position

    if valid_position() and (word[position].token_type == TokenType.LPAR  or word[position].token_type == TokenType.IDENTIFIER or word[position].token_type == TokenType.NUMBER):
        print(indent * " ","T->FT'")
        indent += 2
        handle_F(indent)
        handle_T_prime(indent)
        indent -= 2
    else:
        raise Exception("Cuvantul introdus nu este corect sintactic")

def handle_E_prime(indent):
    global position

    if valid_position() and (word[position].token_type == TokenType.PLUS or word[position].token_type == TokenType.MINUS):
        print(indent * " ",f"E'->{word[position].value}TE'")
        position+=1
        indent += 2
        handle_T(indent)
        handle_E_prime(indent)
        indent -= 2
    else:
        return

def handle_T_prime(indent):
    global position

    if valid_position() and (word[position].token_type == TokenType.ASTERISK or word[position].token_type == TokenType.SLASH):
        print(indent * " ", f"T'->{word[position].value}FT'")
        position+=1
        indent += 2
        handle_F(indent)
        handle_T_prime(indent)
        indent -= 2
    else:
        return


def handle_F(indent):
    global position

    if valid_position() and (word[position].token_type == TokenType.LPAR):
        print(indent * " ", "F->(E)")
        position+=1
        indent += 2
        handle_E(indent)
        indent -= 2
        if valid_position() and word[position].token_type == TokenType.RPAR:
            position+=1
        else:
            raise Exception("CUVANTUL INTRODUS NU ESTE CORECT SINTACTIC")
    elif valid_position() and (word[position].token_type == TokenType.IDENTIFIER or word[position].token_type == TokenType.NUMBER):
        print(indent * " ", f"F->{word[position].value}")
        position+=1
    else:
        raise Exception("CUVANTUL INTRODUS NU ESTE CORECT SINTACTIC")


position = 0
word = sys.argv[1]
l = Lexxer(word)
word = l.parse_tokens()
print(word)
handle_E(1)
