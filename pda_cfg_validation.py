
# PDA and CFG Based Validation System
# Course: Formal Language and Automata
# Assignment: Case Study-Based Analysis and Design using PDA and CFG

import re

# ==================================================
# 1. BALANCED PARENTHESES CHECKER USING PDA
# ==================================================

def balanced_parentheses(expression):

    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    opening = ['(', '{', '[']

    for ch in expression:

        if ch in opening:
            stack.append(ch)

        elif ch in pairs:

            if not stack:
                return False

            if stack[-1] != pairs[ch]:
                return False

            stack.pop()

    return len(stack) == 0

# ==================================================
# 2. PALINDROME CHECKER USING PDA
# Language: Palindromes over {a, b}
# ==================================================

def palindrome_checker(string):

    if any(ch not in "ab" for ch in string):
        return False

    n = len(string)

    # PDA nondeterministically guesses the middle
    for middle in range(n + 1):

        left = string[:middle]
        right = string[middle:]

        # Even-length palindrome
        if left[::-1] == right:
            return True

        # Odd-length palindrome
        if middle < n:
            left = string[:middle]
            right = string[middle + 1:]

            if left[::-1] == right:
                return True

    return False

# ==================================================
# 3. ARITHMETIC EXPRESSION VALIDATOR USING CFG
#
# E -> T ((+ | -) T)*
# T -> F ((* | /) F)*
# F -> number | (E)
# ==================================================

class ExpressionParser:

    def __init__(self, expression):

        self.tokens = re.findall(
            r'\d+(?:\.\d+)?|[+\-*/()]|[^\s]',
            expression
        )

        self.position = 0
        self.valid_tokens = all(
            re.fullmatch(r'\d+(?:\.\d+)?|[+\-*/()]', t)
            for t in self.tokens
        )

    def current(self):

        if self.position < len(self.tokens):
            return self.tokens[self.position]

        return None

    def match(self, token):

        if self.current() == token:
            self.position += 1
            return True

        return False

    # E -> T ((+ | -) T)*
    def parse_expression(self):

        self.parse_term()

        while self.current() in ('+', '-'):

            self.position += 1
            self.parse_term()

    # T -> F ((* | /) F)*
    def parse_term(self):

        self.parse_factor()

        while self.current() in ('*', '/'):

            self.position += 1
            self.parse_factor()

    # F -> number | (E)
    def parse_factor(self):

        token = self.current()

        if token is None:
            raise ValueError("Missing operand")

        if re.fullmatch(r'\d+(?:\.\d+)?', token):

            self.position += 1

        elif self.match('('):

            self.parse_expression()

            if not self.match(')'):
                raise ValueError("Missing closing bracket")

        else:
            raise ValueError("Invalid expression")

    def validate(self):

        if not self.tokens or not self.valid_tokens:
            return False

        try:

            self.parse_expression()

            return self.position == len(self.tokens)

        except (ValueError, RecursionError):

            return False

def arithmetic_validator(expression):

    parser = ExpressionParser(expression)
    return parser.validate()

# ==================================================
# MAIN MENU
# ==================================================

def main():

    while True:

        print("\n======================================")
        print("       PDA AND CFG VALIDATION SYSTEM")
        print("======================================")

        print("1. Balanced Parentheses Checker")
        print("2. Palindrome Checker")
        print("3. Arithmetic Expression Validator")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':

            expression = input("Enter an expression: ")

            if balanced_parentheses(expression):
                print("ACCEPTED: Parentheses are balanced")
            else:
                print("REJECTED: Parentheses are not balanced")

        elif choice == '2':

            string = input("Enter a string (a and b only): ")

            if palindrome_checker(string):
                print("ACCEPTED: Palindrome detected")
            else:
                print("REJECTED: Not a palindrome")

        elif choice == '3':

            expression = input("Enter arithmetic expression: ")

            if arithmetic_validator(expression):
                print("ACCEPTED: Valid arithmetic expression")
            else:
                print("REJECTED: Invalid arithmetic expression")

        elif choice == '4':

            print("Exiting PDA and CFG Validation System...")
            break

        else:

            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
