import sqlite3
import csv
import matplotlib.pyplot as plt
from random import randrange, randint
import numpy as np


def main():

    # ex_1_to_4()
    # ex_5_to_6()
    # ex_7_to_8()
    ex_9()


def ex_1_to_4():

    conn = sqlite3.connect("SE4ALL.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE energy (CountryName TEXT
              NOCASE, IndicatorCode TEXT NOCASE, Year INTEGER,
              Value REAL)''')
    conn.commit()

    with open("SE4ALLData.csv", 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        headers = next(reader)

        headerid = {}

        for i,h in enumerate(headers):
            headerid[h] = i

        for row in reader:

            # Update the table
            for year in range(1990,2017):
                c.execute("INSERT INTO energy VALUES (:CountryName, "
                          ":IndicatorCode, :Year, :Value)", {
                               'CountryName': row[0],
                               'IndicatorCode': row[3],
                               'Year': year,
                               'Value': float_or_none(row[headerid[str(year)]])
                               })
                conn.commit()

    # Exercise 2 - Write a SQL query to find the countries with the highest
    # renewable electricity share of total electricity output in 2015.
    c.execute('SELECT CountryName, Value, Year FROM energy WHERE '
              'IndicatorCode="4.1_SHARE.RE.IN.ELECTRICITY" AND '
              'CountryName IN ("United Kingdom", "New Zealand", "France", '
              '"United States", "Channel Islands", "Portugal", "Bolivia", '
              '"Australia", "Iceland") ORDER BY Value DESC')
    shares = c.fetchall()

    # c.execute('SELECT DISTINCT CountryName FROM energy')
    # print(c.fetchall())

    data_dict = {}
    for row in shares:
        if row[0] not in data_dict:
            data_dict[row[0]] = {}
        data_dict[row[0]][row[2]] = row[1]


    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))

    # Make time series plots
    for country in data_dict:

        # Sort dictionary
        sorted_dict = dict(sorted(data_dict[country].items()))

        # Get lists from dictionary
        years = sorted_dict.keys()
        shares = [sorted_dict[year] for year in years]

        # Plot line
        ax.plot(years, shares, label=country)

    # Formatting and legend
    ax.legend(loc='upper center', bbox_to_anchor=(1.12, 0.95))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.set_ylabel('Renewable electricity share of total electricity output '
                  '(%)')
    ax.set_xlabel('Year')
    ax.grid(axis='x')

    # Save and close figure
    # plt.tight_layout()
    fig.savefig('shares.png')
    plt.close()


def ex_5_to_6():

    # Exercise 6

    # Make list of lots of a, b, c elements
    a_b_c_list = (['a' for _ in range(50)] + ['b' for _ in range(48)] +
                  ['c' for _ in range(98)])

    # Find majority element (if any)
    maj_ele = boyer_moore(a_b_c_list)
    print(maj_ele)


def ex_7_to_8():

    # To collect count values in
    counts = []

    # Find 3 zeros 1000 times
    for _ in range(1000):

        # Initial variables
        all_zeros = False
        count = 0

        # Run while loop until 3 random zeros found
        while all_zeros == False:

            # Get 3 random integers between 0 and 10
            rand_nums = [randrange(10) for _ in range(3)]

            # Add to count
            count += 1

            # Change all zeros bool if 3 zeros found
            if all(num == 0 for num in rand_nums):
                all_zeros = True

        # Add count to counts list
        counts.append(count)

    # Get mean number of times taken to get zeros
    mean_count = np.mean(counts)
    print('Mean number of attempts to get 3 random zeros', mean_count)


def ex_9():

    print(random_sample(range(1000), 50))


def random_sample(big_list, sample_number):

    # To add random elements to
    reservoir = []

    # Fill reservoir with number of random elements defines by ample_number
    for ind, ele in enumerate(big_list):
        if ind < sample_number:
            reservoir.append(ele)
        else:
            ind_2 = randint(0, ind);
            if ind_2 < sample_number:
                reservoir[ind_2] = ele

    return reservoir


def boyer_moore(big_list):

    # Run Boyer-Moore algorithm
    elem = None
    count = 0
    for d in big_list:
        if count == 0:
            elem = d
            count = 1
        else:
            if elem == d:
                count += 1
            else:
                count -= 1

    # Number of times element apears in list
    elem_num = len([x for x in big_list if x == elem])

    # Check if majority element
    if elem_num >= len(big_list) / 2:
        return f'Majority element is {elem}'
    return f'No majority element'


def float_or_none(val):
    try:
        return float(val)
    except:
        return None



if __name__ == "__main__":
    main()
    print('Finished')
