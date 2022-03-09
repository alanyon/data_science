"""
The file "population.txt" contains the 2011 England and Wales census data.
Each number represents the population of a sampling area called an LSOA.

Load the data and plot a histogram.
Write your own code to compute the mean, median, mode, standard deviation and
mean deviation.
Compare the results of your code to the values returned by library routines in
numpy/scipy
"""
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
from collections import Counter
from scipy import stats


def main():

    # Load data
    data = np.loadtxt('population.txt')

    # Calculate mean, median, mode, standard deviation and mean deviation
    data_mean = calc_mean(data)
    data_median = calc_median(data)
    data_mode = calc_mode(data)
    data_sd = calc_sd(data, data_mean)
    data_md = calc_md(data, data_mean)

    # Numpy/scipy values
    np_mean = np.mean(data)
    np_median = np.median(data)
    scipy_mode = stats.mode(data)
    np_std = np.std(data)
    np_mdev = np.mean(np.absolute(data - np.mean(data)))

    # Skew values
    skew_val = stats.skew(data)
    mode_skew = (data_mean - data_mode) / data_sd
    median_skew = 3 * (data_mean - data_median) / data_sd
    data_kurtosis = stats.kurtosis(data, fisher=False)
    excess_kurtosis = data_kurtosis - 3

    # Compare values
    print('data_mean', data_mean)
    print('np_mean', np_mean)
    print('data_median', data_median)
    print('np_median', np_median)
    print('data_mode', data_mode)
    print('scipy_mode', scipy_mode)
    print('data_sd', data_sd)
    print('np_std', np_std)
    print('data_md', data_md)
    print('np_mdev', np_mdev)

    # Print skewness value
    print('')
    print(f'Standard skew: {skew_val}')
    print(f'Mode skew: {mode_skew}')
    print(f'Median skew: {median_skew}')
    print('')
    print('Positive/right skew. There are more area with populations larger '
          'than the mean than areas with populations smaller than the mean.'
          ' This could be because there are many small towns and '
           'villages (with similar population sizes) and relatively few'
           ' big towns/cities with much larger populations.')
    print('')
    print(f'Kurtosis: {data_kurtosis}')
    print(f'Excess kurtosis: {excess_kurtosis}')
    print('The population data is leptokurtic')
    print('')

    # Create figure and axis
    fig, ax = plt.subplots(2, 1, figsize=(15, 10))

    # Make histogram
    bins = [50 * i for i in range(601)]
    ax[0].hist(data, bins=bins)

    # Plot mean, median and mode
    ax[0].axvline(data_mean, color='r', linestyle='dashed', label='Mean')
    ax[0].axvline(data_median, color='g', linestyle='dashed', label='Median')
    ax[0].axvline(data_mode, color='y', linestyle='dashed', label='Mode')
    ax[0].axvline(data_median - data_sd, color='k', linestyle='dashed',
               label='Standard deviation')
    ax[0].axvline(data_median + data_sd, color='k', linestyle='dashed')
    ax[0].axvline(data_median - data_md, color='magenta', linestyle='dashed',
               label='Mean deviation')
    ax[0].axvline(data_median + data_md, color='magenta', linestyle='dashed')

    # Label axes, title
    ax[0].set_xlabel('Population')
    ax[0].set_ylabel('Number of LSOAs')
    ax[0].set_title('Histogram of Population Data')

    # Set limit on x-axis
    ax[0].set_xlim(900, 3000)

    # Create legend
    ax[0].legend(loc='upper right')

    # Make box plot on log scale
    ax[1].boxplot(data, vert=False)
    ax[1].set_xscale('log')
    ax[1].get_xaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax[1].xaxis.set_minor_formatter(FormatStrFormatter("%d"))

    # Label axes, title
    ax[1].set_xlabel('Population')
    ax[1].set_title('Box Plot of Population Data')

    # Save figure
    plt.tight_layout()
    fig.savefig('population_plots.png')
    plt.close()

    print('Finished')


def calc_mean(data):

    mean_data = np.sum(data) / len(data)

    return mean_data


def calc_median(data):

    # Number of data points
    num_pts = len(data)

    # Sort data
    s_data = sorted(data)

    # If number of data points even, take mean of middle values
    if num_pts % 2 == 0:
        median = (s_data[num_pts // 2] + s_data[num_pts // 2 - 1]) / 2

    # Otherwise, just take middle value
    else:
        median = s_data[num_pts // 2]

    return median


def calc_mode(data):

    counts = Counter(data)
    data_mode = max(counts, key=counts.get)

    return data_mode


def calc_sd(data, data_mean):

    num_pts = len(data)

    first_bit = 1 / (num_pts - 1)

    sum_bit = 0
    for val in data:
        sum_bit += (val - data_mean) ** 2

    variance = first_bit * sum_bit

    std_dev = variance ** 0.5

    return std_dev


def calc_md(data, data_mean):

    num_pts = len(data)

    first_bit = 1 / num_pts

    sum_bit = 0
    for val in data:
        sum_bit += abs(val - data_mean)

    mean_dev = first_bit * sum_bit

    return mean_dev


if __name__ == "__main__":
    main()
