# demorganizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`demorganizer` is a Python toolkit for automating common Computer Science calculations. It provides ready-to-use implementations of algebraic structures, propositional logic theorems, and numerical root-finding methods — built to help CS students and educators apply mathematical concepts without getting bogged down by the underlying mechanics.

### Modules

This section outlines the core components and modules that make up the project. Each module encapsulates a specific domain of functionality, promoting a clear separation of concerns, code reusability, and easier maintainability.

### `algebra` — Algebra Engine

| Implementation    | Type               | Description                                                        |
| ----------------- | ------------------ | ------------------------------------------------------------------ |
| `Expression`      | `class` (abstract) | Base class for all algebraic expressions                           |
| `Variable`        | `class`            | A named, single-character symbolic variable                        |
| `Constant`        | `class`            | A fixed boolean value (`True` or `False`)                          |
| `TRUE`, `FALSE`   | `Constant`         | Sentinel instances for the boolean constants                       |
| `UnaryOperation`  | `class`            | Applies a unary operator (e.g. `~`) to one operand                 |
| `BinaryOperation` | `class`            | Applies a binary operator (`&`, `\|`, `^`) to two operands         |
| `Signal`          | `enum`             | Arithmetic sign of a numeric value: positive, negative, or neutral |
| `Number`          | `TypeAlias`        | Numeric scalar — `int \| float`                                    |
| `UnaryFunction`   | `TypeAlias`        | A function mapping a `Number` to a `Number`                        |

### `algo` — Algorithms

#### Propositional Logic

| Implementation                  | Type       | Description                             |
| ------------------------------- | ---------- | --------------------------------------- |
| `apply_double_negation`         | `function` | `~~A → A`                               |
| `apply_unary_constant_folding`  | `function` | `~True → False`, `~False → True`        |
| `apply_binary_constant_folding` | `function` | `True & False → False`                  |
| `apply_idempotent_law`          | `function` | `A \| A → A`, `A & A → A`               |
| `apply_inverse_law`             | `function` | `A \| ~A → True`, `A & ~A → False`      |
| `apply_annihilation_law`        | `function` | `A \| True → True`, `A & False → False` |
| `apply_identity_law`            | `function` | `A \| False → A`, `A & True → A`        |

#### Numerical Methods

| Implementation                  | Type                 | Description                                                      |
| ------------------------------- | -------------------- | ---------------------------------------------------------------- |
| `calculate_bisection_x`         | `function`           | Computes the midpoint of an interval                             |
| `find_required_bisection_steps` | `function`           | Calculates the number of iterations needed for a given precision |
| `apply_bisection_by_steps`      | `generator function` | Runs bisection for a fixed number of steps                       |
| `apply_bisection_by_tolerance`  | `generator function` | Runs bisection until an error tolerance is met                   |
| `calculate_false_position_x`    | `function`           | Computes the false-position root estimate for an interval        |
| `apply_false_position_by_steps` | `generator function` | Runs the Regula Falsi method for a fixed number of steps         |

### `format` — Visualisation

| Implementation       | Type       | Description                                                  |
| -------------------- | ---------- | ------------------------------------------------------------ |
| `create_truth_table` | `function` | Generates a formatted truth table for any Boolean expression |

## Installation

```bash
git clone https://github.com/othonhugo/demorganizer.git
cd demorganizer
pip install .
```

## Usage

<details>
<summary>Boolean algebra</summary>

```python
from demorganizer.algebra import Variable, TRUE, FALSE

A = Variable("A")
B = Variable("B")
C = Variable("C")

expr = (A & B) | ~C

# Evaluate for specific variable bindings
print(expr.evaluate({"A": True, "B": True, "C": False}))  # True
```

</details>

---

<details>
<summary>Truth table</summary>

```python
from demorganizer.algebra import Variable
from demorganizer.format import create_truth_table

A = Variable("A")
B = Variable("B")
C = Variable("C")

print(create_truth_table((A & B) | ~C))
```

```text
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

</details>

---

<details>
<summary>Numerical methods</summary>

```python
from demorganizer.algo.numeric_methods.bisection import apply_bisection_by_tolerance

# Find the root of f(x) = x² - 2 in [1, 2] with precision 1e-6
steps = apply_bisection_by_tolerance(lambda x: x**2 - 2, (1, 2), precision=1e-6)

for x in steps:
    print(x)
```

</details>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
