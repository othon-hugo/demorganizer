# demorganizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`demorganizer` is a Python-based framework for constructing, evaluating, and visualizing Boolean algebra expressions. It leverages object-oriented principles to represent logical expressions as a tree structure, allowing for intuitive construction using Python's operator overloading and generating truth tables.

## Features

*   **Expression Tree:** Build complex Boolean expressions using `Variable`, `Constant`, `UnaryOperation`, and `BinaryOperation` classes.
*   **Operator Overloading:** Use standard Python logical operators (`&`, `|`, `^`, `~`) to intuitively combine expressions.
*   **Expression Evaluation:** Evaluate expressions by providing a dictionary of variable bindings.
*   **Truth Table Generation:** Generate comprehensive truth tables for any given expression, beautifully formatted using the `tabulate` library.

## Project Structure

The project is organized into two main components:

1.  **`algebra` module:** Contains the core classes for defining and manipulating Boolean expressions.
2.  **`format` module:** Provides utilities for presenting expressions, specifically for generating truth tables.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/othonhugo/demorganizer.git
    cd demorganizer
    ```

2.  **Install dependencies:**
    This project requires the `tabulate` library for truth table formatting.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Defining Expressions

You can define variables and constants, then combine them using Python's logical operators.

```python
from algebra import Variable, Constant, TRUE, FALSE

# Define variables
A = Variable("A")
B = Variable("B")
C = Variable("C")

# Construct your expressions
expr1 = (A & B) | ~C
expr2 = A ^ (B | FALSE)

# Example with direct boolean literals (automatically converted to Constants)
expr3 = (A | (B & True)) | ~False
```

### 2. Evaluating Expressions

Use the `evaluate()` method on an expression, passing a dictionary of variable bindings.

```python
from algebra import Variable

A = Variable("A")
B = Variable("B")

expr = A & B

# Evaluate with specific values for A and B
bindings_11 = {"A": True, "B": True}
bindings_12 = {"A": True, "B": False}

print(expr.evaluate(bindings_11)) # True
print(expr.evaluate(bindings_12)) # False
```

### 3. Generating Truth Tables

The `create_truth_table` function from the `format` module will generate a string representation of the truth table.

```python
from algebra import Variable
from format import create_truth_table

A = Variable("A")
B = Variable("B")
C = Variable("C")

expr = (A & B) | ~C

print(create_truth_table(expr))
```

This will output:

```
 A    B    C    ((A & B) | (~C))
---  ---  ---  ------------------
 1    1    1           1
 1    1    0           1
 1    0    1           0
 1    0    0           1
 0    1    1           0
 0    1    0           1
 0    0    1           0
 0    0    0           1
```
