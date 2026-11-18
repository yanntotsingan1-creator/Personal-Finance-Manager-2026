import random
bot_name = ('Chester')
print(f'{bot_name}: Hello! My name is {bot_name}. Would you like to play my guessing game?')

while True:
    user_input = input('You: ').lower()
    
    if user_input in ['yes', 'y', 'sure']:
        print(f'{bot_name}: Great! I will think of a number between 1 and 100. Try to guess it!')
        number_to_guess = random.randint(1, 100)
        attempts = 0
        
        while True:
            guess = int(input('Your guess: '))
            attempts += 1
        
            if guess < number_to_guess:
                print(f'{bot_name}: Too low! Try again.')
            elif guess > number_to_guess:
                print(f'{bot_name}: Too high! Try again.')
            else:
                print(f'{bot_name}: Congratulations! You guessed the number {number_to_guess} in {attempts} attempts. Would you like to play again? (yes/no)')
                play_again = input('You: ').lower()
                if play_again in ['yes']:
                    print(f'{bot_name}: Great! I will think of a number between 1 and 100. Try to guess it!')
                    number_to_guess = random.randint(1, 100)
                    attempts = 0
                else:
                    print(f'{bot_name}: Goodbye!')
                    break

    elif user_input in ['no', 'n', 'not now']:
        print(f'{bot_name}: Alright, goodbye!')
        break
    elif user_input in ['bye', 'exit', 'quit']:
        print(f'{bot_name}: Goodbye! Have a great day!')
        break
    else:
        print(f'{bot_name}: I didn\'t understand that. Please respond with "yes" or "no".')