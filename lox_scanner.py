"scanner.py"

from typing import List

from pylox.lox_token import Token
from pylox.lox_token_type import TokenType

globals().update(TokenType.__members__)


class Scanner:
    "scanner.Scanner"
    keywords = {
        "and":    AND,
        "class":  CLASS,
        "else":   ELSE,
        "false":  FALSE,
        "for":    FOR,
        "fun":    FUN,
        "if":     IF,
        "nil":    NIL,
        "or":     OR,
        "print":  PRINT,
        "return": RETURN,
        "super":  SUPER,
        "this":   THIS,
        "true":   TRUE,
        "var":    VAR,
        "while":  WHILE
    }

    def __init__(self, lox: 'pylox.Lox', source: str) -> None:
        self.lox = lox
        self.source: str = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> List[Token]:
        "scanner.Scanner.scan_tokens"
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        "scanner.Scanner.is_at_end"
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        "scanner.Scanner.scan_token"
        c: str = self.advance()
        match c:
            # Ignore whitespace.
            case ' ':
                pass
            case '\r':
                pass
            case '\t':
                pass
            case '\n':
                self.line += 1
            case "(":
                self.add_token(LEFT_PAREN)
            case ")":
                self.add_token(RIGHT_PAREN)
            case "{":
                self.add_token(LEFT_BRACE)
            case "}":
                self.add_token(RIGHT_BRACE)
            case ",":
                self.add_token(COMMA)
            case ".":
                self.add_token(DOT)
            case "-":
                self.add_token(MINUS)
            case "+":
                self.add_token(PLUS)
            case ";":
                self.add_token(SEMICOLON)
            case "*":
                self.add_token(STAR)
            case '!':
                self.add_token(BANG_EQUAL if self.match('=') else BANG)
            case '=':
                self.add_token(EQUAL_EQUAL if self. match('=') else EQUAL)
            case '<':
                self.add_token(LESS_EQUAL if self.match('=') else LESS)
            case '>':
                self.add_token(GREATER_EQUAL if self.match('=') else GREATER)
            case '/':
                if self.match('/'):
                    # A comment goes until the end of the line.
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(SLASH)
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    self.lox.error(self.line, f"Unexpected character: `{c}`.")

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        "scanner.Scanner.add_token"
        text: str = ''
        if literal:
            text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self) -> str:
        "scanner.Scanner.advance"
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.lox.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        value = self.source[self.start + 1:self.current-1]
        self.add_token(STRING, value)

    def is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.is_digit(self.peek_next()):
          # Consume the "."
          self.advance()

          while self.is_digit(self.peek()):
            self.advance()

        self.add_token(NUMBER, float(self.source[self.start:self.current]));

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        token = self.keywords.get(text)
        if not token:
            token = IDENTIFIER
        self.add_token(token)

    def is_alpha(self, c: str) -> bool:
        return ('a' <= c <= 'z' or
                'A' <= c <= 'Z' or
                c == '_')

    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)
