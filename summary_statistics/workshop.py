import csv
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def main():

    # ex_1()
    # ex_2()
    # ex_3()
    ex_5_6()


def ex_1():

    # Load data as numpy array
    data = np.loadtxt('corr.csv', delimiter=',')

    # Index to get 3 columns
    first_col = data[:, 0]
    second_col = data[:, 1]
    third_col = data[:, 2]

    # Get correlation coefficients between each pair of columns
    cor_1_2 = stats.pearsonr(first_col, second_col)
    cor_1_3 = stats.pearsonr(first_col, third_col)
    cor_2_3 = stats.pearsonr(second_col, third_col)

    # Print correlation coefficients
    print('cor_1_2', cor_1_2)
    print('cor_2_3', cor_2_3)
    print('cor_1_3', cor_1_3)


def ex_2():

    # Define data
    x = [29.8, 30.1, 30.5, 30.6, 31.3, 31.7, 32.6, 33.1, 32.7, 32.8]
    y = [327, 456, 509, 497, 596, 573, 661, 741, 809, 717]

    # Calculate and print correlation coefficient
    corr_xy = stats.pearsonr(x, y)
    print('corr_xy', corr_xy)

    # Create figure and axis
    fig, ax = plt.subplots()

    # Make scatter plot
    ax.scatter(x, y)

    # Save and close figure
    plt.tight_layout()
    fig.savefig('pop_scatter.png')
    plt.close()


def ex_3():

    # Define data
    drowned = [109, 102, 102, 98, 85, 95, 96, 98, 123, 94, 102]
    cage = [2, 2, 2, 3, 1, 1, 2, 3, 4, 1, 4]

    # Calculate and print correlation coefficient
    corr_drown_cage = stats.pearsonr(drowned, cage)
    print('corr_drown_cage', corr_drown_cage)


def ex_5_6():

    # Load data to numpy array
    old_data = np.loadtxt('old.csv', delimiter=',')

    # Define columns from array
    first_col = old_data[:, 0]
    second_col = old_data[:, 1]

    # Logs of columns
    first_col_log = np.log(first_col)
    second_col_log = np.log(second_col)

    # Calculate and print correlation coefficients
    corr_old = stats.pearsonr(first_col, second_col)
    corr_old_log = stats.pearsonr(first_col_log, second_col_log)
    print('corr_old', corr_old[0])
    print('corr_old_log', corr_old_log[0])

    # Create figure and axis
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Make scatter plots
    ax[0].scatter(first_col, second_col, label=f'r = {corr_old[0]:.4f}')
    ax[0].set_ylabel('Elderly population density')
    ax[0].set_xlabel('Population density')
    ax[0].legend()

    ax[1].scatter(first_col_log, second_col_log,
                  label=f'r = {corr_old_log[0]:.4f}')
    ax[1].set_ylabel('Log of elderly population density')
    ax[1].set_xlabel('Log of population density')
    ax[1].legend()

    # Save and close figure
    plt.tight_layout()
    fig.savefig('old_scatter.png')
    plt.close()


if __name__ == "__main__":
    main()
