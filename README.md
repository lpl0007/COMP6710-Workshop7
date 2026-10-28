# COMP6710 Workshop 7: Simplistic White-Box Fuzzing

## Overview

This repository contains my implementation for **Workshop 7 – Simplistic White-Box Fuzzing** in COMP 6710. The goal is to exercise the provided calculator operation with generated and deliberately selected inputs, observe the exceptions that occur, and record one message for each unique exception class.

The starter code provides a `divide(v1, v2)` function. The fuzzer supplies inputs to this function and catches exceptions so that one failing test does not stop the rest of the run.

## Files

- **`w7.py`** — the fuzzer implementation, test cases, exception handling, and code that writes the crash log.
- **`crashes.txt`** — the recorded error messages, with one entry per unique exception class found during the run.

These are the two files required for the workshop submission.

## Requirements

- Python 3
- No third-party packages are required. The script uses Python's standard library, including `random`, `string`, and `decimal`.

## How It Works

The implementation uses several complementary test approaches:

1. **Random alphanumeric inputs:** `generateInput()` creates strings containing letters and digits. `simpleFuzzer()` generates two values and passes them to `divide()`. Since the calculator expects numeric operands, these generated string inputs can produce a `TypeError`.
2. **Additional test cases:** The script tries inputs such as division by zero, `None`, a very large integer, and `Decimal` values to exercise other error paths.
3. **Decimal signal tests:** The script enables selected traps in a local Decimal arithmetic context to exercise additional signal classes, including `Inexact`, `Rounded`, `Subnormal`, `Underflow`, and `Clamped`.
4. **Exception recording:** `runTest()` catches exceptions and records their class names and messages. `safeRepr()` safely formats values for the log, including the very large integer test case.
5. **Unique crash log:** The script stores one message per unique exception class in a dictionary, writes those messages to `crashes.txt`, and prints the total number of unique classes found. It also prints a warning if fewer than 10 classes are collected.

The random string tests alone are not expected to find every class. The additional inputs and Decimal signal tests are used to expand the exception coverage.

## Run the Fuzzer

From the repository directory, run:

```bash
python w7.py
```

The program prints the test inputs and any exceptions found, displays the unique exception class names and total, and rewrites `crashes.txt` with the results from that run.

To inspect the saved messages:

```bash
cat crashes.txt
```

On Windows Command Prompt, you can use:

```bat
type crashes.txt
```

## Results

The latest reported run completed without an unhandled traceback and recorded **11 unique exception classes**, exceeding the workshop's minimum target of 10:

- `TypeError`
- `ZeroDivisionError`
- `OverflowError`
- `DivisionByZero`
- `InvalidOperation`
- `Overflow`
- `Inexact`
- `Rounded`
- `Subnormal`
- `Underflow`
- `Clamped`

The exact messages and inputs are saved in `crashes.txt`. Because the random input generator is randomized, the specific alphanumeric strings and corresponding log entry may differ between runs.

**Important distinction:** some of the recorded classes are raised by deliberately selected test cases or by Decimal signal traps, rather than by the random alphanumeric strings themselves. This broadens the automated test run's exception coverage; it should not be interpreted as evidence that random string generation alone discovers all 11 classes.

## Submission

Submit these two files for the workshop:

1. `w7.py`
2. `crashes.txt`

The README documents the implementation and how to run it; it is not one of the two files specified for submission in the workshop instructions.
