"scanner.py"

from typing import List

from pylox.lox import error
from pylox.token import Token, TokenType


globals().update(TokenType.__members__)

class Scanner:
    "scanner.Scanner"

    def __init__(self, source: str) -> None:
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
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        "scanner.Scanner.is_at_end"
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        "scanner.Scanner.scan_token"
        c: str = self.advance()
        match c:
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
                self.add_token(GREATER_EQUAL if match('=') else GREATER)
            case _:
                error(self.line, f"Unexpected character: `{c}`.")

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
