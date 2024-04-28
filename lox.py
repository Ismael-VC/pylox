#!/usr/bin/env python3

"lox"

import sys
from sys import argv
from typing import List
from pprint import pprint

from pylox.lox_token import Token
from pylox.lox_token_type import TokenType
from pylox.lox_scanner import Scanner


class Lox:
    "lox.Lox"
    def __init__(self, args: List[str]):
        self.args = args
        self.had_error = False

    def main(self) -> None:
        "lox.Lox.main"
        args_len = len(self.args)
        if args_len > 2:
            print("Usage: pylox [script]")
        elif args_len == 2:
            self.run_file(self.args[1])
        else:
            self.run_prompt()

    def run_file(self, path: str) -> str:
        "lox.Lox.run_file"
        with open(path, encoding="utf8") as file:
            tokens = Scanner(self, file.read()).scan_tokens()
            pprint(tokens)

    def run_prompt(self) -> None:
        "lox.Lox.run_prompt"
        while True:
            try:
                line = input("> ")
                if line.strip() in ["exit", "quit", "bye"]:
                    sys.exit()
                self.run(line)
                self.had_error = False
            except EOFError:
                print()
                sys.exit()
            except KeyboardInterrupt:
                sys.exit()

    def run(self, source: str) -> None:
        "lox.Lox.run"
        tokens = Scanner(self, source).scan_tokens()
        pprint(tokens)
        if self.had_error:
            sys.exit(65)

    def _report(self, line: int, where: str, message: str) -> None:
        "lox.Lox.report"
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True

    def error(self, line: int, message: str) -> None:
        "lox.error"
        self._report(line, "", message)

if __name__ == "__main__":
    lox = Lox(argv)
    lox.main()
