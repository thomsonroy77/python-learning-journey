
print("=== Welcome to My Python Calculator ===")

while True:
    print("\nAvailable operations: +  -  *  /")
    print("Type 'exit' to quit.")

    first_input = input("\nEnter first number: ")

    if first_input.lower() == "exit":
        print("Calculator closed. Goodbye!")
        break

    try:
        num1 = float(first_input)
    except ValueError:
        print("Invalid number. Please enter a valid number.")
        continue

    operator = input("Choose an operation (+, -, *, /): ")

    if operator.lower() == "exit":
        print("Calculator closed. Goodbye!")
        break

    if operator not in ["+", "-", "*", "/"]:
        print("Invalid operator. Please choose +, -, * or /.")
        continue

    second_input = input("Enter second number: ")

    if second_input.lower() == "exit":
        print("Calculator closed. Goodbye!")
        break

    try:
        num2 = float(second_input)
    except ValueError:
        print("Invalid number. Please enter a valid number.")
        continue

    if operator == "+":
        result = num1 + num2

    elif operator == "-":
        result = num1 - num2

    elif operator == "*":
        result = num1 * num2

    elif operator == "/":
        if num2 == 0:
            print("Error: Cannot divide by zero.")
            continue
        result = num1 / num2

    print(f"Result: {result}")

    print("\nYou can perform another calculation!")

