def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(expression):
    """Evaluate a simple arithmetic expression string."""
    try:
        result = eval(expression, {"__builtins__": {}}, {
            "abs": abs, "round": round
        })
        return result
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")
    except Exception:
        raise ValueError(f"Invalid expression: {expression}")


def main():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("Enter expression: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue
        try:
            result = calculate(user_input)
            print(f"= {result}")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
