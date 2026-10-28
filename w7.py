import random
import string
from decimal import (
    Decimal,
    localcontext,
    Inexact,
    Rounded,
    Subnormal,
    Underflow,
    Clamped,
)


def divide(v1, v2):
    return v1 / v2


def generateInput():
    characters = string.ascii_letters + string.digits
    length = random.randint(1, 10)
    return ''.join(random.choices(characters, k=length))



def safeRepr(value):
    try:
        return repr(value)
    except Exception as error:
        return f"<{type(value).__name__}: could not format ({type(error).__name__})>"


def runTest(a, b):
    try:
        result = divide(a, b)
        print(f"Input: ({safeRepr(a)}, {safeRepr(b)}) -> Result: {result}")
        return None

    except Exception as error:
        message = (
            f"Input: ({safeRepr(a)}, {safeRepr(b)}) -> "
            f"{type(error).__name__}: {error}"
        )
        print(message)
        return type(error).__name__, message


def simpleFuzzer():
    a = generateInput()
    b = generateInput()

    print("Testing randomly generated alphanumeric inputs:")
    return runTest(a, b)


def testDecimalSignal(signal):
    with localcontext() as context:
        context.traps[signal] = True

        try:
            if signal is Inexact:
                divide(Decimal("1"), Decimal("3"))

            elif signal is Rounded:
                context.prec = 2
                divide(Decimal("1.000"), Decimal("1"))

            elif signal is Subnormal:
                divide(Decimal("1E-999999"), Decimal("10"))

            elif signal is Underflow:
                divide(Decimal("1E-999999"), Decimal("3"))

            elif signal is Clamped:
                context.clamp = 1
                divide(Decimal("1"), Decimal("Infinity"))

        except Exception as error:
            message = (
                f"Decimal signal test {signal.__name__} -> "
                f"{type(error).__name__}: {error}"
            )
            print(message)
            return type(error).__name__, message

    return None


if __name__ == '__main__':
    crashes = {}

    # Generate random alphanumeric inputs.
    for _ in range(10):
        result = simpleFuzzer()

        if result:
            exception_type, message = result
            crashes.setdefault(exception_type, message)

    # Test additional inputs that can trigger different exceptions.
    test_cases = [
        (10, 0),
        (None, 2),
        (10**10000, 1),
        (Decimal("1"), Decimal("0")),
        (Decimal("0"), Decimal("0")),
        (Decimal("1E+9999999"), Decimal("1")),
    ]

    print("\nTesting additional inputs:")

    for a, b in test_cases:
        result = runTest(a, b)

        if result:
            exception_type, message = result
            crashes.setdefault(exception_type, message)

    # Test additional Decimal arithmetic signal classes.
    signals = [Inexact, Rounded, Subnormal, Underflow, Clamped]

    for signal in signals:
        result = testDecimalSignal(signal)

        if result:
            exception_type, message = result
            crashes.setdefault(exception_type, message)

    # Save one actual error message per unique exception class.
    with open("crashes.txt", "w", encoding="utf-8") as file:
        for message in crashes.values():
            file.write(message + "\n")

    print("\nUnique exception classes found:")
    for exception_type in sorted(crashes):
        print(exception_type)

    print(f"\nTotal unique exception classes: {len(crashes)}")
    print("Crash messages saved to crashes.txt.")

    if len(crashes) < 10:
        print("WARNING: Fewer than 10 unique exception classes were found.")