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
    for _ in range(30):
        a = generateInput()
        b = generateInput()
        simpleFuzzer(a, b)