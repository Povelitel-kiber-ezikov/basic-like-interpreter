from dataclasses import dataclass

from lexer import Lexer, Token


@dataclass
class Instruction:
    op: str
    args: tuple[str, ...]
    line: int


class Parser:
    def __init__(self, tokens: list[Token]):
        # Сохраняет токены и подготавливает список инструкций.
        if not tokens or tokens[-1].kind != "EOF":
            raise ValueError("Список токенов должен заканчиваться EOF")

        self.tokens = tokens
        self.position = 0
        self.instructions = []

    def current_token(self) -> Token:
        # Возвращает токен на текущей позиции.
        return self.tokens[self.position]

    def advance(self) -> Token:
        # Возвращает текущий токен и переходит к следующему.
        token = self.current_token()

        if token.kind != "EOF":
            self.position += 1

        return token

    def expect(self, kind: str, expected: str) -> Token:
        # Проверяет тип текущего токена и переходит дальше.
        token = self.current_token()

        if token.kind != kind:
            if token.kind == "NEWLINE":
                found = "конец строки"
            elif token.kind == "EOF":
                found = "конец файла"
            else:
                found = repr(token.text)

            raise ValueError(
                f"Строка {token.line}: ожидалось {expected}, получено {found}"
            )

        return self.advance()

    def parse(self) -> list[Instruction]:
        # Разбирает программу и возвращает её инструкции.
        while self.current_token().kind != "EOF":
            if self.current_token().kind == "NEWLINE":
                self.advance()
            else:
                self.parse_statement()

        return self.instructions

    def parse_statement(self):
        # Определяет тип инструкции и запускает её разбор.
        token = self.current_token()

        if token.kind == "DIM":
            self.parse_declaration()
        else:
            raise ValueError(
                f"Строка {token.line}: "
                f"инструкция {token.text!r} пока не поддерживается парсером"
            )

    def parse_declaration(self):
        # Разбирает объявление переменной и создаёт DECLARE.
        dim_token = self.expect("DIM", "DIM")
        name_token = self.expect("IDENTIFIER", "имя переменной")

        self.expect("AS", "AS")

        type_token = self.current_token()

        if type_token.kind not in {"INTEGER", "FLOAT"}:
            raise ValueError(
                f"Строка {type_token.line}: "
                "ожидался тип INTEGER или FLOAT"
            )

        self.advance()
        self.expect("NEWLINE", "конец строки")

        self.instructions.append(Instruction(
            op="DECLARE",
            args=(name_token.text, type_token.text),
            line=dim_token.line,
        ))

