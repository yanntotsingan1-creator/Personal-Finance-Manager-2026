from phone import Phone

first_phone = Phone("iPhone 13", "black", "128GB", 999)
second_phone = Phone("Samsung Galaxy S21", "white", "256GB", 1199)
print(f'First phone: {first_phone.version}, {first_phone.color}, {first_phone.storage}, ${first_phone.price}')
print(f'Second phone: {second_phone.version}, {second_phone.color}, {second_phone.storage}, ${second_phone.price}')

first_phone.turn_off()
second_phone.make_call('518-598-7682')