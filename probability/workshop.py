import math
import scipy.stats as stats
import matplotlib.pyplot as plt
import random
import numpy as np


def main():

    """ Exercise 1 """

    # Conditional
    con_prob = (1 / 36) / (1 / 6)
    print('Exercise 1 conditional prob', con_prob)
    # Independence
    ind_prob = 1 / 6
    print('Exercise 1 independence prob', ind_prob)

    """ Exercise 2 """

    # No. combinations
    combs = 6 * 6
    # Possibly 7 combinations
    comb_7s = [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]

    # Prob of 4 given sum equal to 7
    prob_4_given_7 = len([x for x in comb_7s if 4 in x]) / len(comb_7s)
    print('Exercise 2 prob', prob_4_given_7)

    # Conditional method
    prob_cond = (len([x for x in comb_7s if 4 in x]) / 36) / (len(comb_7s) /
                                                              combs)
    print('Exercise 2 cond prob', prob_cond)

    """ Exercise 3 """

    # Binomial distribution for 10 coin flips
    bin_dist_1 = stats.binom(10, 0.5)
    prob_5 = bin_dist_1.pmf(5)

    print('Exercise 3 prob 5 heads', prob_5)

    """ Exercise 4 """

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plot binomial distributions
    for n, p in zip([10, 20, 10], [0.5, 0.5, 0.1]):
        x = np.arange(n + 1)
        bin_dist = stats.binom.pmf(x, n, p)
        ax.plot(x, bin_dist, label = f'n={n}, p={p}')

    # Create legend
    ax.legend()

    # Save figure
    plt.tight_layout()
    fig.savefig('bin_dists.png')
    plt.close()

    """ Exercise 6 """
    means = {'nums': [], 'means': []}
    for n in range(10, 1000, 10):
        events = []
        for _ in range(n):
            events.append(flip_coin())
        mean = np.mean(events)
        means['nums'].append(n)
        means['means'].append(mean)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plot distributions
    ax.scatter(means['nums'], means['means'])

    # Save figure
    plt.tight_layout()
    fig.savefig('means.png')
    plt.close()

    """ Exercise 5 """
    data_x = np.array([random.uniform(-3, 3) for _ in range(100)])
    data_y1 = np.array([gaussian(x, 0, 1) for x in data_x])
    data_y2 = np.array([gaussian(x, 1, 1) for x in data_x])
    data_y3 = np.array([gaussian(x, 0, 2) for x in data_x])
    data_y4 = np.array([gaussian(x, -2, 4) for x in data_x])

    # Create figure and axis
    fig, ax = plt.subplots()

    # Plot distributions
    ax.scatter(data_x, data_y1, label='(0, 1)')
    ax.scatter(data_x, data_y2, label='(1, 1)')
    ax.scatter(data_x, data_y3, label='(0, 2)')
    ax.scatter(data_x, data_y4, label='(-2, 4)')

    # Create legend
    ax.legend()

    # Save figure
    plt.tight_layout()
    fig.savefig('gaussians.png')
    plt.close()


    """ Exercise 7 """
    money = 10
    progress = []

    while(money > 0):

        result = flip_coin()
        if result == 1:
            money += 1
        else:
            money -= 1
        progress.append(money)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plot distributions
    ax.plot(range(len(progress)), progress)

    # Save figure
    plt.tight_layout()
    fig.savefig('stakes.png')
    plt.close()

    """ Exercise 8 """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 10))

    # Run experiment for n = 10, 100 and 1000
    for n in [10, 100, 1000]:
        results = []
        for _ in range(1000):
            results.append(np.mean(np.array([flip_coin() for _ in range(n)])))
        ax.hist(results, label=f'n={n}')

    # Create legend()
    ax.legend()

    # Save figure
    plt.tight_layout()
    fig.savefig('flips_hist.png')
    plt.close()

    """ Exercise 9 """
    nums, stds = [], []
    for n in range(10, 1100, 10):
        results = []
        for _ in range(100):
            results.append(np.mean(np.array([flip_coin() for _ in range(n)])))
        stds.append(np.std(results))
        nums.append(n)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Make log-log plot
    ax.scatter(np.log(nums), np.log(stds))

    # Save figure
    plt.tight_layout()
    fig.savefig('stds.png')
    plt.close()

    """ Exercise 10 """
    data1 = np.random.rand(10000)

    fig, ax = plt.subplots()

    plt.hist(data1, bins=100)

    # Save figure
    plt.tight_layout()
    fig.savefig('hist.png')
    plt.close()

    """ Exercise 11 """

    for x in range(100):
        if x == 0:
            data2 = np.random.rand(10000)
        else:
            data2 += np.random.rand(10000)

    fig, ax = plt.subplots()

    plt.hist(data2, bins=100)

    # Save figure
    plt.tight_layout()
    fig.savefig('hist2.png')
    plt.close()


def gaussian(x, mu, sigma):

    first_bit = 1 / (sigma * (2 * math.pi) ** 0.5)
    second_bit = math.exp(-(x-mu) ** 2 / (2 * (sigma ** 2)))
    result = first_bit * second_bit

    return result


def flip_coin():
    if np.random.rand() < 0.5:
        return 0
    return 1


if __name__ == "__main__":
    main()
