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

    SINGLE_CHAR_TOKENS = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULTIPLY",
        "/": "DIVIDE",
        "=": "EQUAL",
        ">": "GREATER",
        "<": "LESS",
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
    }

    TWO_CHAR_TOKENS = {
        ">=": "GREATER_EQUAL",
        "<=": "LESS_EQUAL",
        "<>": "NOT_EQUAL",
    }

    def __init__(self, source: str):
        self.source = source.replace("\r\n", "\n").replace("\r", "\n")
        self.position = 0
        self.line = 1

    @staticmethod
    def is_letter(char: str) -> bool:
        return "A" <= char <= "Z" or "a" <= char <= "z"

    @staticmethod
    def is_digit(char: str) -> bool:
        return "0" <= char <= "9"

    def read_word(self) -> Token:
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

    def read_number(self) -> Token:
        start = self.position
        start_line = self.line

        if (
            self.position >= len(self.source)
            or not self.is_digit(self.source[self.position])
        ):
            raise ValueError("Число должно начинаться с цифры")

        while (
            self.position < len(self.source)
            and self.is_digit(self.source[self.position])
        ):
            self.position += 1

        kind = "INTEGER_NUMBER"

        if (
            self.position < len(self.source)
            and self.source[self.position] == "."
        ):
            self.position += 1

            if (
                self.position >= len(self.source)
                or not self.is_digit(self.source[self.position])
            ):
                raise ValueError(
                    f"Строка {start_line}: после точки должна быть цифра"
                )

            while (
                self.position < len(self.source)
                and self.is_digit(self.source[self.position])
            ):
                self.position += 1

            kind = "FLOAT_NUMBER"

        text = self.source[start:self.position]

        return Token(
            kind=kind,
            text=text,
            line=start_line,
        )

    def tokenize(self) -> list[Token]:
        tokens = []

        while self.position < len(self.source):
            char = self.source[self.position]
            two_chars = self.source[self.position:self.position + 2]

            if char == " " or char == "\t":
                self.position += 1

            elif char == "\n":
                tokens.append(Token(
                    kind="NEWLINE",
                    text="\n",
                    line=self.line,
                ))

                self.position += 1
                self.line += 1

            elif char == "'":
                while (
                    self.position < len(self.source)
                    and self.source[self.position] != "\n"
                ):
                    self.position += 1

            elif self.is_letter(char):
                tokens.append(self.read_word())

            elif self.is_digit(char):
                tokens.append(self.read_number())

            elif two_chars in self.TWO_CHAR_TOKENS:
                tokens.append(Token(
                    kind=self.TWO_CHAR_TOKENS[two_chars],
                    text=two_chars,
                    line=self.line,
                ))

                self.position += 2

            elif char in self.SINGLE_CHAR_TOKENS:
                tokens.append(Token(
                    kind=self.SINGLE_CHAR_TOKENS[char],
                    text=char,
                    line=self.line,
                ))

                self.position += 1

            else:
                raise ValueError(
                    f"Строка {self.line}: недопустимый символ {char!r}"
                )

        if tokens and tokens[-1].kind != "NEWLINE":
            tokens.append(Token(
                kind="NEWLINE",
                text="\n",
                line=self.line,
            ))

        tokens.append(Token(
            kind="EOF",
            text="",
            line=self.line,
        ))

        return tokens


if __name__ == "__main__":
    source = """DIM x AS INTEGER
x = 12 + 3
PRINT x"""

    lexer = Lexer(source)

    for token in lexer.tokenize():
        print(token)