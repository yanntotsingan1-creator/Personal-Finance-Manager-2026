import random
bot_name = ('Yuno')
print(f'Hello, I am {bot_name}! Lets play Rock, Paper, Scissors?')

while True:
    user_choice = input('Choose Rock, Paper, or Scissors: ').capitalize()
    bot_choice = random.choice(['Rock', 'Paper', 'Scissors'])
    print(f'{bot_name} chose {bot_choice}.')
    if user_choice == bot_choice:
        print('It\'s a tie!')
    elif (user_choice == 'Rock' and bot_choice == 'Scissors') or \
         (user_choice == 'Paper' and bot_choice == 'Rock') or \
         (user_choice == 'Scissors' and bot_choice == 'Paper'):
        print('You win!')
    else:
        print(f'{bot_name} wins!')
    
    play_again = input('Play again? (yes/no): ').lower()
    if play_again == 'yes':
        continue
    elif play_again == 'no':
        print(f'Thanks for playing with {bot_name}!')
        break
    else:
        print('Invalid input. Please enter "yes" or "no".')