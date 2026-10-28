import random
import string


def divide(v1, v2):
    return v1 / v2


def generateInput():
    characters = string.ascii_letters + string.digits
    length = random.randint(1, 10)
    return ''.join(random.choices(characters, k=length))


def runTest(a, b):
    try:
        result = divide(a, b)
        print(f"Input: ({a!r}, {b!r}) -> Result: {result}")
        return None

    except Exception as error:
        message = (
            f"Input: ({a!r}, {b!r}) -> "
            f"{type(error).__name__}: {error}"
        )
        print(message)
        return message


def simpleFuzzer():
    a = generateInput()
    b = generateInput()

    print("Testing randomly generated alphanumeric inputs:")
    return runTest(a, b)


if __name__ == '__main__':
    crashes = []

    # Generate and test six random alphanumeric input pairs.
    for _ in range(6):
        message = simpleFuzzer()
        if message:
            crashes.append(message)

    # Test four additional inputs that should cause errors.
    test_cases = [
        (10, 0),
        (None, 2),
        ([], 2),
        ({}, 2),
    ]

    print("\nTesting additional inputs:")

    for a, b in test_cases:
        message = runTest(a, b)
        if message:
            crashes.append(message)

    # Save the collected crash messages.
    with open("crashes.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(crashes) + "\n")

    print(f"\nCollected {len(crashes)} crash messages.")
    print("Crash messages saved to crashes.txt.")