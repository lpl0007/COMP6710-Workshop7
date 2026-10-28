
import random
import string


def divide(v1, v2):
    return v1 / v2


def simpleFuzzer(a, b):
    try:
        result = divide(a, b)
        print(f"Input: ({a!r}, {b!r}) -> Result: {result}")
    except Exception as error:
        print(f"Input: ({a!r}, {b!r}) -> {type(error).__name__}: {error}")



def generateInput():
    choices = [
        10,
        0,
        -5,
        2.5,
        "hello",
        "",
        None,
        [],
        [1, 2],
        {},
        True,
        "0",
        "123",
        "3.14",
        " ",
    ]
    return random.choice(choices)



if __name__ == '__main__':
    test_cases = [
        ("hello", 2),
        (10, "hello"),
        ([], 10),
        (10, []),
        (None, 2),
        (10, None),
        ({}, 2),
        (2, {}),
        (10, 0),
        (0, 0),
        ("3.14", 2),
        (True, "2"),
        ([1, 2], [3, 4]),
        ("", 1),
        (1, ""),
    ]

    for a, b in test_cases:
        simpleFuzzer(a, b)