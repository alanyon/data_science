import numpy as np
import scipy
from scipy.stats import norm, probplot, ttest_ind, ks_2samp, kstest
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv


def main():

    # exercise_1()
    # exercise_2()
    exercise_4_5_and_6()
    exercise_7()
    exercise_8()


def exercise_1():

    # Sorted sample
    rand_nums = np.sort(np.random.normal(0, 1, 100))

    # Get z values for normal cdf
    z_norms = [norm.ppf(prob, loc=0, scale=1)
               for prob in np.arange(0.01, 1.01, 0.01)]

    # Create figure and axis
    fig, ax = plt.subplots()

    # Plot line
    ax.scatter(sorted_nums, z_norms)

    # Save and close figure
    plt.tight_layout()
    fig.savefig('ex_1.png')
    plt.close()


def exercise_2():

    # Sample
    rand_nums = np.random.normal(0, 1, 100)

    # Create figure and axis
    fig, ax = plt.subplots()

    # Plot line
    probplot(rand_nums, plot=plt)

    # Save and close figure
    plt.tight_layout()
    fig.savefig('ex_2.png')
    plt.close()


def exercise_4_5_and_6():

    # To add heights to
    heights_1990_men, heights_1990_women = [], []

    # Read csv file
    with open('heights.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # Look at each row
        for row in reader:

            # Only consider stats from 1990
            if row[3] == '1990':

                # Add height to appropriate list based on sex
                if row[2] == 'Men':
                    heights_1990_men.append(float(row[4]))
                elif row[2] == 'Women':
                    heights_1990_women.append(float(row[4]))

    # Make histogram and do T test
    hist_and_ttest(heights_1990_men, heights_1990_women, 'Men', 'Women',
                   'ex_4', 'ex_5')


def exercise_7():

    # To add heights to
    heights_1990_men, heights_1960_men = [], []

    # Read csv file
    with open('heights.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # Look at each row
        for row in reader:

            # Collect men's heights from 1990 and 1960
            if row[3] == '1990' and row[2] == 'Men':
                heights_1990_men.append(float(row[4]))
            elif row[3] == '1960' and row[2] == 'Men':
                heights_1960_men.append(float(row[4]))

    # Make histogram and do T test
    hist_and_ttest(heights_1990_men, heights_1960_men, 'Men 1990', 'Men 1960',
                   'ex_7_i', 'ex_7_ii')


def hist_and_ttest(data_1, data_2, label_1, label_2, fname_1, fname_2):

    # Create figure and axis
    fig, ax = plt.subplots()

    # Plot line
    ax.hist(data_1, bins=20, label=label_1, color='orange', alpha=0.5,
            lw=0)
    ax.hist(data_2, bins=20, label=label_2, color='blue',
            alpha=0.5, lw=0)

    # Legend, formatting, etc
    ax.legend()
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Mean height (cm)')

    # Save and close figure
    plt.tight_layout()
    fig.savefig(f'{fname_1}.png')
    plt.close()

    # Create figure and axis
    fig, ax = plt.subplots()

    # q-q plot
    probplot(data_1, plot=plt, fit=False)
    probplot(data_2, plot=plt, fit=False)

    # Formatting, etc
    ax.get_lines()[0].set_markerfacecolor('orange')
    ax.get_lines()[1].set_markerfacecolor('blue')
    ax.get_lines()[0].set_markeredgecolor('orange')
    ax.get_lines()[1].set_markeredgecolor('blue')
    patch_1 = mpatches.Patch(color='orange', label=label_1)
    patch_2 = mpatches.Patch(color='blue', label=label_2)
    ax.legend(handles=[patch_1, patch_2])
    ax.set_ylabel('Height (cm)')

    # Save and close figure
    plt.tight_layout()
    fig.savefig(f'{fname_2}.png')
    plt.close()

    # Calculate 2 sample T test
    t_stat, pvalue = ttest_ind(data_1, data_2)
    print(f'Test stat for {label_1}/{label_2}', t_stat)
    print(f'pvalue for {label_1}/{label_2}', pvalue)
    print('')

    # Calculate 2 sample KS test
    ks_stat, pvalue = ks_2samp(data_1, data_2)
    print(f'KS stat for {label_1}/{label_2}', ks_stat)
    print(f'pvalue for {label_1}/{label_2}', pvalue)
    print('')

    # Calculate one-sample KS tests on first dataset
    data_1 = np.array(data_1)
    standardised_data_1 = (data_1 - data_1.mean()) / (data_1.std())
    ks_stat, pvalue = kstest(standardised_data_1, 'norm')
    print(f'One-sample KS stat for {label_1}', ks_stat)
    print(f'pvalue for {label_1}', pvalue)
    print('')

    # Calculate one-sample KS tests on second dataset
    data_2 = np.array(data_2)
    standardised_data_2 = (data_2 - data_2.mean()) / (data_2.std())
    ks_stat, pvalue = kstest(standardised_data_2, 'norm')
    print(f'One-sample KS stat for {label_2}', ks_stat)
    print(f'pvalue for {label_2}', pvalue)
    print('')


def exercise_8():

    # To update with stats
    mens_height_1900, mens_height_1996 = {}, {}
    womens_height_1900, womens_height_1996 = {}, {}

    # Read csv file
    with open('heights.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # Look at each row
        for row in reader:

            # Stats from 1900
            if row[3] == '1900':

                # Collect stats for men or women
                if row[2] == 'Men':
                    mens_height_1900[row[0]] = float(row[4])
                elif row[2] == 'Women':
                    womens_height_1900[row[0]] = float(row[4])

            # Stats from 1996
            if row[3] == '1996':

                # Collect stats for men or women
                if row[2] == 'Men':
                    mens_height_1996[row[0]] = float(row[4])
                elif row[2] == 'Women':
                    womens_height_1996[row[0]] = float(row[4])

    # For collecting biggest and smallest differences
    big_diff_men, big_diff_women = {}, {}
    small_diff_men, small_diff_women = {}, {}

    # Find difference in mean heights for each country
    for ind, country in enumerate(mens_height_1900):

        # Get differences
        diff_men = mens_height_1996[country] - mens_height_1900[country]
        diff_women = womens_height_1996[country] - womens_height_1900[country]

        # For first iteration, add to dictionaries regardless
        if ind == 0:
            big_diff_men['country'] = country
            big_diff_men['diff'] = diff_men
            big_diff_women['country'] = country
            big_diff_women['diff'] = diff_women
            small_diff_men['country'] = country
            small_diff_men['diff'] = diff_men
            small_diff_women['country'] = country
            small_diff_women['diff'] = diff_women

        # Otherwise, replace dictionary values if more extreme
        elif diff_men > big_diff_men['diff']:
            big_diff_men['country'] = country
            big_diff_men['diff'] = diff_men
        elif diff_men < small_diff_men['diff']:
             small_diff_men['country'] = country
             small_diff_men['diff'] = diff_men
        elif diff_women > big_diff_women['diff']:
             big_diff_women['country'] = country
             big_diff_women['diff'] = diff_men
        elif diff_women < small_diff_women['diff']:
             small_diff_women['country'] = country
             small_diff_women['diff'] = diff_men

    print('big_diff_men', big_diff_men)
    print('big_diff_women', big_diff_women)
    print('small_diff_men', small_diff_men)
    print('small_diff_women', small_diff_women)


if __name__ == "__main__":
    main()
    print('Finished')
