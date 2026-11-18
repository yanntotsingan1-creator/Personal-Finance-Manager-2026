# Weight conversion script
weight_num = float(input('Enter your weight number: '))
unit = input('In kg or lbs?: ').lower()

if unit == 'lbs':
    weight_num = weight_num * 0.453592
    print(f'Your weight is {weight_num} kg.')
elif unit == 'kg':
    weight_num = weight_num / 0.453592
    print(f'Your weight is {weight_num} lbs.')
else:
    print('Invalid unit. Please enter "kg" or "lbs".')
