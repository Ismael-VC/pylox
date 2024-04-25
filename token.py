from token_type import TokenType


class Token:
    "token_type.Token"
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self.token_type: TokenType = token_type
        self.lexeme: str = lexeme
        self.literal: object = literal
        self.line: int = line

    def __repr__(self) -> str:
        return (
            f"Token({self.token_type}, {self.lexeme}, {self.literal}, {self.line})"
        )
