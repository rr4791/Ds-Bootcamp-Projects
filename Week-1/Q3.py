# Program to print numbers from 1 to 20 with odd/even check

for num in range(1, 21):   # range goes from 1 to 20
    if num % 2 == 0:
        print(num, "is Even")
    else:
        print(num, "is Odd")
