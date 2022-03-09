import math

def main():

    # Exercise 1
    ex_1_prob = (12 / 24) * (11 / 23) * (10 / 22)
    print('Exercise 1', ex_1_prob)

    # Exercise 2
    prob_no_same_birthdays = 1
    for x in range(50):
        prob_no_same_birthdays *= ((365 - x) / 365)
    prob_same_birthday = 1 - prob_no_same_birthdays
    print('Exercise 2', prob_same_birthday)

    # Exercise 3
    print('Exercise 3', 2 ** 10)


def binomial_distribution(n, k, p):

    n_ch_k = math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

    prob = n_ch_k * 0.5 ** k * (1 - p) ** n - k

    return prob



if __name__ == "__main__":
    main()
