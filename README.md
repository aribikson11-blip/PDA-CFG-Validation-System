# Assignment 3: Case Study-Based Analysis and Design Using PDA and CFG

**Course:** 21CSC301T -- Formal Language and Automata\
**Assessment:** Continuous Learning Assessment 2 -- Task 3

This project demonstrates three applications of Context-Free Grammars
(CFG) and Pushdown Automata (PDA):

1.  Balanced Parentheses Checker
2.  Palindrome Checker
3.  Arithmetic Expression Validator

------------------------------------------------------------------------

## 1. Balanced Parentheses Checker

### Context-Free Grammar (CFG)

The grammar generates correctly balanced parentheses, curly braces, and
square brackets.

``` text
G = (V, T, P, S)

V = {S}
T = {(, ), {, }, [, ]}

Start symbol: S

Production rules:
S -> (S)S
S -> {S}S
S -> [S]S
S -> ε
```

-   `S` represents a balanced expression.
-   `ε` represents the empty string.
-   Nested brackets are allowed.

### PDA State Diagram

The PDA pushes each opening bracket onto the stack. When a closing
bracket is read, it must match the bracket at the top of the stack,
which is then popped. The input is accepted when it ends and the stack
contains no unmatched opening brackets.

``` mermaid
stateDiagram-v2
    direction LR
    [*] --> q0
    q0 --> q0: Opening bracket / push
    q0 --> q0: Matching closing bracket / pop
    q0 --> qReject: Closing bracket with empty or mismatched stack
    q0 --> qAccept: Input ended and stack has no unmatched brackets
    qAccept --> [*]
    qReject --> [*]
```

### Stack Operations

  Input   Stack operation
  ------- ---------------------------
  `(`     Push `(`
  `{`     Push `{`
  `[`     Push `[`
  `)`     Pop only if `(` is on top
  `}`     Pop only if `{` is on top
  `]`     Pop only if `[` is on top

### Example

Input: `{[()]}`

``` text
Read {  -> Push {
Read [  -> Push [
Read (  -> Push (
Read )  -> Pop (
Read ]  -> Pop [
Read }  -> Pop }

No unmatched opening brackets remain -> ACCEPTED
```

Accepted examples: `()`, `{[()]}`, `((a+b)*c)`, `[]{}()`, `([{}])`\
Rejected examples: `(()`, `([)]`, `{[}`, `((a+b)`, `]()`.

------------------------------------------------------------------------

## 2. Palindrome Checker

### Context-Free Grammar (CFG)

This grammar generates palindromes over the alphabet `{a, b}`.

``` text
G = (V, T, P, S)

V = {S}
T = {a, b}

Start symbol: S

Production rules:
S -> aSa
S -> bSb
S -> a
S -> b
S -> ε
```

-   A palindrome reads the same from left to right and right to left.
-   `aSa` adds `a` to both ends.
-   `bSb` adds `b` to both ends.
-   `a`, `b`, and `ε` provide the base cases.

### PDA State Diagram

This is a nondeterministic PDA (NPDA). It pushes symbols from the first
half onto the stack, nondeterministically guesses the middle, and then
compares the remaining input with the stack in reverse order.

``` mermaid
stateDiagram-v2
    direction LR
    [*] --> qPush
    qPush --> qPush: Read a or b / push symbol
    qPush --> qMatch: ε / guess even-length midpoint
    qPush --> qMatch: Read one middle symbol / guess odd-length midpoint
    qMatch --> qMatch: Read a, top is a / pop
    qMatch --> qMatch: Read b, top is b / pop
    qMatch --> qReject: Symbol does not match stack top
    qMatch --> qAccept: Input ended and stack returned to bottom marker
    qAccept --> [*]
    qReject --> [*]
```

### Example 1: Accepted

Input: `abba`

``` text
Push a
Push b
Guess the midpoint
Read b -> Pop b
Read a -> Pop a

All symbols match -> ACCEPTED
```

### Example 2: Rejected

Input: `abab`

``` text
First half: ab
Second half: ab
Reverse of first half: ba

The second half does not match ba -> REJECTED
```

Accepted examples: `a`, `b`, `aa`, `aba`, `abba`\
Rejected examples: `ab`, `aab`, `abb`, `abab`, `baabx`.

------------------------------------------------------------------------

## 3. Arithmetic Expression Validator

### Context-Free Grammar (CFG)

The grammar validates arithmetic expressions containing numbers,
addition, subtraction, multiplication, division, and parentheses.

The following grammar is suitable for a recursive-descent parser and
avoids left recursion.

``` text
G = (V, T, P, E)

Non-terminals: {E, E', T, T', F}
Terminals: {number, +, -, *, /, (, )}

Start symbol: E

Production rules:
E  -> T E'
E' -> + T E' | - T E' | ε
T  -> F T'
T' -> * F T' | / F T' | ε
F  -> (E) | number
```

-   `E` represents an expression.
-   `T` represents a term.
-   `F` represents a factor.
-   Multiplication and division have higher precedence than addition and
    subtraction.
-   Parentheses allow nested expressions.

### Grammar Flow Diagram

``` mermaid
flowchart TD
    E["Expression E"] --> T["Term T"]
    E --> EP["E'"]
    EP -->|" + T E' or - T E' "| EP
    EP -->|" ε "| END["End"]
    T --> F["Factor F"]
    T --> TP["T'"]
    TP -->|" * F T' or / F T' "| TP
    TP -->|" ε "| TEND["End of term"]
    F --> N["Number"]
    F --> P["( Expression )"]
```

### Example Derivation

Input: `(2 + 3) * 4`

``` text
E
=> T E'
=> F T' E'
=> (E) T' E'
=> (T E') T' E'
=> (F T' E') T' E'
=> (2 + 3) * 4
```

Result: **ACCEPTED**

Accepted examples: `2+3`, `(4+5)*6`, `12/3-2`, `7*(8-2)`, `3.5+2.1`\
Rejected examples: `2+`, `(3+4`, `*5`, `4//2`, `2a+3`.

### Parsing Process Diagram

The arithmetic expression validator uses a recursive-descent parser that
follows the CFG productions. The parser checks whether tokens match the
grammar and rejects an expression if a required token is missing or
unexpected.

``` mermaid
flowchart TD
    A(["Start"]) --> B["Read arithmetic expression"]
    B --> C["Tokenize input"]
    C --> D["Parse using E, T and F rules"]
    D --> E{"All tokens consumed and grammar valid?"}
    E -->|Yes| F(["ACCEPT"])
    E -->|No| G(["REJECT"])
```

------------------------------------------------------------------------

## 4. Why Finite Automata Are Insufficient

1.  **Balanced parentheses:** Arbitrarily nested brackets require memory
    of the opening brackets and their order.
2.  **Palindrome checking:** The first half of the string must be
    remembered to compare it with the second half in reverse order.
3.  **Arithmetic expressions:** Nested parentheses and recursive
    expression structures require grammar-based parsing.

A finite automaton has only a finite number of states and no unbounded
stack. A PDA has stack memory, so it is suitable for these context-free
language problems.

------------------------------------------------------------------------

## 5. Limitations

-   The balanced-parentheses checker validates bracket matching, not the
    full syntax of a programming language.
-   The palindrome checker accepts only strings over `{a, b}`.
-   The arithmetic parser validates syntax; it does not calculate the
    expression's value or check runtime conditions such as division by
    zero.
-   The arithmetic grammar uses conventional operator precedence and
    does not include unary operators or exponentiation.

------------------------------------------------------------------------

## 6. Conclusion

The three case studies demonstrate the use of Context-Free Grammars and
Pushdown Automata in structured-language validation. The
balanced-parentheses checker uses stack operations, the palindrome
checker illustrates nondeterministic midpoint guessing, and the
arithmetic-expression validator uses grammar-based parsing. These
examples show why PDA and CFG are more suitable than finite automata for
languages involving nested or recursive structures.
