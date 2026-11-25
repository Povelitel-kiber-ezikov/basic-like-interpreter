from dataclasses import dataclass


@dataclass
class Token:
    
    kind: str
    text: str
    line: int


class Lexer:
    KEYWORDS = {
        "DIM",
        "AS",
        "INTEGER",
        "FLOAT",
        "INPUT",
        "PRINT",
        "IF",
        "THEN",
        "ELSE",
        "ENDIF",
        "WHILE",
        "WEND",
        "AND",
        "OR",
        "NOT",
    }

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1

    @staticmethod
    def is_letter(char: str) -> bool:
        return "A" <= char <= "Z" or "a" <= char <= "z"

    @staticmethod
    def is_digit(char: str) -> bool:
        return "0" <= char <= "9"

    def read_word(self) -> Token:
        """Прочитать ключевое слово или имя переменной."""

        start = self.position
        start_line = self.line

        if (
            self.position >= len(self.source)
            or not self.is_letter(self.source[self.position])
        ):
            raise ValueError("Слово должно начинаться с латинской буквы")

        while self.position < len(self.source):
            char = self.source[self.position]

            if self.is_letter(char) or self.is_digit(char) or char == "_":
                self.position += 1
            else:
                break

        text = self.source[start:self.position]

        if text in self.KEYWORDS:
            kind = text
        else:
            kind = "IDENTIFIER"

        return Token(
            kind=kind,
            text=text,
            line=start_line,
        )