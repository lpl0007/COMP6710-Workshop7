import random
import string
from decimal import Decimal, localcontext, Inexact, Rounded, Subnormal, Underflow, Clamped


def divide(v1, v2):
    return v1 / v2


def generateInput():
    characters = string.ascii_letters + string.digits
    length = random.randint(1, 10)
    return ''.join(random.choices(characters, k=length))


def safe_repr(value):
    try:
        return repr(value)
    except Exception:
        return f"<{type(value).__name__} value>"


def simpleFuzzer(a, b):
    try:
        result = divide(a, b)
        print(f"Input: ({safe_repr(a)}, {safe_repr(b)}) -> Result: {result}")
    except Exception as error:
        message = (
            f"Input: ({safe_repr(a)}, {safe_repr(b)}) -> "
            f"{type(error).__name__}: {error}"
        )
        print(message)
        return type(error).__name__, message


def testDecimalSignals():
    signals = [Inexact, Rounded, Subnormal, Underflow, Clamped]

    for signal in signals:
        with localcontext() as context:
            context.traps[signal] = True
            try:
                if signal in (Inexact, Rounded):
                    divide(Decimal("1"), Decimal("3"))
                elif signal in (Subnormal, Underflow):
                    divide(Decimal("1E-999999"), Decimal("10"))
                elif signal is Clamped:
                    divide(Decimal("1"), Decimal("Infinity"))
            
            except Exception as error:
                message = (
                    f"Decimal signal test {signal.__name__} -> "
                    f"{type(error).__name__}: {error}"
                )
                print(message)

                with open("crashes.txt", "a", encoding="utf-8") as file:
                    file.write(message + "\n")


if __name__ == '__main__':
    test_cases = [
        (generateInput(), generateInput()),
        ("abc", "def"),
        (10, 0),
        (0, 0),
        (None, 2),
        ([], 2),
        ({}, 2),
        (True, False),
        (2.5, 0.5),
        (10**10000, 1),
        (Decimal("1"), Decimal("0")),
        (Decimal("0"), Decimal("0")),
        (Decimal("1e9999999"), Decimal("1")),
        (Decimal("NaN"), Decimal("0")),
        (Decimal("Infinity"), Decimal("0")),
        (Decimal("sNaN"), Decimal("1")),
        (Decimal("1"), Decimal("Infinity")),
        (Decimal("-Infinity"), Decimal("0")),
        (Decimal("1E-999999"), Decimal("1E-999999")),
    ]

    exception_types = set()
    crash_messages = []

    for a, b in test_cases:
        result = simpleFuzzer(a, b)
        if result:
            exception_type, message = result
            exception_types.add(exception_type)
            crash_messages.append(message)

    print("\nUnique exception classes found:")
    for exception_type in sorted(exception_types):
        print(exception_type)

    print(f"Total unique exception classes: {len(exception_types)}")

    with open("crashes.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(crash_messages) + "\n")

    print("\nCrash messages saved to crashes.txt")
    testDecimalSignals()