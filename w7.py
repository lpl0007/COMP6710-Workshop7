import random
import string


def divide(v1, v2):
    return v1 / v2


def generateInput():
    characters = string.ascii_letters + string.digits
    length = random.randint(1, 10)
    return ''.join(random.choices(characters, k=length))


def simpleFuzzer(a, b):
    try:
        result = divide(a, b)
        print(f"Input: ({a!r}, {b!r}) -> Result: {result}")
    except Exception as error:
        message = (
            f"Input: ({a!r}, {b!r}) -> "
            f"{type(error).__name__}: {error}"
        )
        print(message)
        return message


if __name__ == '__main__':
    test_cases = [
        ("abc", "def"),
        ("10", 2),
        (2, "10"),
        (None, 2),
        (2, None),
        (10, 0),
        (0, 0),
        ([], 2),
        (2, []),
        ({}, 2),
        (2, {}),
        (True, False),
        (False, 2),
        (2.5, 0.5),
        ("", ""),
        (" ", 1),
        (complex(1, 2), 2),
        (2, complex(1, 2)),
        (float("inf"), 2),
        (float("nan"), 2),
    ]

    for a, b in test_cases:
        simpleFuzzer(a, b)