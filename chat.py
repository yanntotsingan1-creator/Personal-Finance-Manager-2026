from math import sqrt
bot_name: str = 'Bob'
print(f'Hello, my name is {bot_name}. How can I assist you today?')

while True:
    user_input: str = input('You: ').lower()
    
    if user_input in ['hi', 'hello', 'hey']:
        print(f'{bot_name}: Hi there! How can I help you today?')
    elif user_input in ['bye', 'exit', 'quit']:
        print(f'{bot_name}: Goodbye, have a good day!')
    elif user_input in ['+', 'add', 'sum']:
        print(f'{bot_name}: Sure! Please provide two numbers to add.')
        num1 = float(input('First number: '))
        num2 = float(input('Second number: '))
        result = num1 + num2
        print(f'{bot_name}: The sum of {num1} and {num2} is {result}.')
    elif user_input in ['-', 'subtract', 'difference']:
        print(f'{bot_name}: Sure! Please provide two numbers to subtract.')
        num1 = float(input('First number: '))
        num2 = float(input('Second number: '))
        result = num1 - num2
        print(f'{bot_name}: The difference between {num1} and {num2} is {result}.')
    elif user_input in ['*', 'multiply', 'product']:
        print(f'{bot_name}: Sure! Please provide two numbers to multiply.')
        num1 = float(input('First number: '))
        num2 = float(input('Second number: '))
        result = num1 * num2
        print(f'{bot_name}: The product of {num1} and {num2} is {result}.')
    elif user_input in ['/', 'divide', 'quotient']:
        print(f'{bot_name}: Sure! Please provide two numbers to divide.')
        num1 = float(input('First number: '))
        num2 = float(input('Second number: '))
        if num2 == 0:
            print(f'{bot_name}: Division by zero is not allowed.')
        else:
            result = num1 / num2
            print(f'{bot_name}: The quotient of {num1} and {num2} is {result}.')
    elif user_input in ['power', 'exponent', '^']:
        print(f'{bot_name}: Sure! Please provide a base and an exponent.')
        base = float(input('Base: '))
        exponent = float(input('Exponent: '))
        result = base ** exponent
        print(f'{bot_name}: {base} raised to the power of {exponent} is {result}.')
    elif user_input in ['sqrt', 'square root']:
        print(f'{bot_name}: Sure! Please provide a number to find the square root.')
        num = float(input('Number: '))
        if num < 0:
            print(f'{bot_name}: Square root of negative numbers is not defined in real numbers.')
        else:
            result = sqrt(num)
            print(f'{bot_name}: The square root of {num} is {result}.')
    elif user_input in ['help']:
        print(f'{bot_name}: Here are some commands you can use:')
        print(' - hi, hello, hey: Greet the bot')
        print(' - bye, exit, quit: Exit the chat')
        print(' - +, add, sum: Add two numbers')
        print(' - -, subtract, difference: Subtract two numbers')
        print(' - *, multiply, product: Multiply two numbers')
        print(' - /, divide, quotient: Divide two numbers')
        print(' - power, exponent, ^: Raise a number to a power')
        print(' - sqrt, square root: Find the square root of a number')
    else:
        print(f'{bot_name}: I\'m sorry, I didn\'t understand that. Can you please try again? Type "help" to see the list of commands.')