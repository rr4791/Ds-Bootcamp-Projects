# Program to count vowels in a word

# take input from user
word = input("Enter a word: ")

# define vowels
vowels = "aeiouAEIOU"

# count vowels
count = 0
for letter in word:
    if letter in vowels:
        count += 1

# print result
print("Number of vowels:", count)
