from typing import Union

from lox_token_type import TokenType


class Token:
    "token_type.Token"
    def __init__(self, token_type: TokenType, lexeme: str,
            literal: Union[int, str], line: int):
        self.token_type: TokenType = token_type
        self.lexeme: str = lexeme
        self.literal: object = literal
        self.line: int = line

    def __repr__(self) -> str:
        token = f"type: {self.token_type.name}"
        lexeme = f", lexeme: '{self.lexeme}'" if self.lexeme else ""
        literal = ""
        if self.literal:
            if isinstance(self.literal, str):
                literal = f", literal: '{self.literal}'"
            else:
                literal = f", literal: {self.literal}"
        line = f", line: {self.line}"
        return f"Token({token}{lexeme}{literal}{line})"
