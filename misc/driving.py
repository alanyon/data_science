# total = 0
# for num in range(1, 101):
#     total += num * num
# print(total)
# total = 0
# for num in range(1, 1001):
#     if num % 3 == 0 or num % 5 == 0:
#         total += num
# print(total)

# x = "supercalifragilisticexpialidocious"
# y = "pneumonoultramicroscopicsilicovolcanoconiosis"
#
# z = [letter for letter in x if letter not in y]

# import random
#
# for iter in range(5):
#     num = f'{random.randint(1, 100)}\n'
#     with open('rand.txt', 'a') as file:
#         file.write(str(num))

# letters = "antidisestablishmentarianism"
# sorted_letters = sorted(letters)
# print(sorted_letters)

# The 4 characters below specify the following update rules
# N -> x + (0,1)
# S -> x + (0,-1)
# E -> x + (1,0)
# W -> x + (-1,0)
# Apply the rules in the string "NNNEEESSWNNSW", starting from the position
# x = (0,0) and print the final position.

def update(tup_x, letters):

    list_x = list(tup_x)

    for char in letters:
        if char == 'N':
            list_x[1] += 1
        elif char == 'S':
            list_x[1] -= 1
        elif char == 'E':
            list_x[0] += 1
        elif char == 'W':
            list_x[0] -= 1

    return tuple(list_x)


old_x = (0, 0)
new_x = update(old_x, 'NNNEEESSWNNSW')

print(new_x)
