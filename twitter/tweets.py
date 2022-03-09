import json
import os
import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import datetime as dt
from zipfile import ZipFile
from multiprocessing import Process, Queue
import geopandas
import useful_functions as uf

# Data dir path
SCRATCH_PATH = '/scratch/alanyon/data_science/tweets'
# For pickling/unpickling data
T_STRS = ['ids', 'dates', 'geos', 'places', 'duplicates', 'bad_tweets',
          'tweets_by_day', 'tweets_by_hour']


def main(new_data):

    # Collect tweet info from files if running for first time
    if new_data == 'yes':
        get_tweets()

    # Otherwise, unpickle data
    else:

        # Collect all data from pickle files
        tweets_by_day = {}
        tweets_by_hour = {'week': {}, 'weekend': {}}
        for ind in range(8):
            (ids_i, dates_i, geos_i, places_i, duplicates_i,
             bad_tweets_i, tweets_by_day_i, tweets_by_hour_i) =[
                uf.unpickle_data(f'{SCRATCH_PATH}/pickles/{t_str}_{ind}')
                for t_str in T_STRS
                ]

            # Add to big dictionaries
            combine_dicts(tweets_by_day, tweets_by_day_i)
            for period in ['week', 'weekend']:
                tweets_by_hour[period].update(tweets_by_hour_i[period])

    # Make some plots
    day_plot(tweets_by_day)
    box_plot(tweets_by_day)
    hour_plot(tweets_by_hour)

    # # Number of tweets per day
    # tweets_by_day = {}
    # tweets_by_hour = {'week': {}, 'weekend': {}}
    #
    # # Loop through list and add to dictionary
    # for date in dates:
    #
    #     # Get datetime ignoring hours, minutes, etc
    #     day_dt = date.replace(hour=0, minute=0, second=0, microsecond=0)
    #     hour_dt = date.replace(minute=0, second=0, microsecond=0)
    #
    #     # If day already in dictionary, add to count
    #     if day_dt in tweets_by_day:
    #         tweets_by_day[day_dt] += 1
    #
    #     # Add key to dictionary if day not in there, with initial count of 1
    #     else:
    #         tweets_by_day[day_dt] = 1
    #
    #     if date.weekday() in [5, 6]:
    #         if hour_dt in tweets_by_hour['weekend']:
    #             tweets_by_hour['weekend'][hour_dt] += 1
    #         else:
    #             tweets_by_hour['weekend'][hour_dt] = 1
    #
    #     else:
    #         if hour_dt in tweets_by_hour['week']:
    #             tweets_by_hour['week'][hour_dt] += 1
    #         else:
    #             tweets_by_hour['week'][hour_dt] = 1


def get_tweets():

    # List of days split into 8 chunks
    day_chunks = np.array_split(np.array(range(1, 31)), 8)

    # Use multiprocessing to process each date of the chunk in parellel
    queue = Queue()
    processes = []

    # Same process for each date in the chunk
    for chunk_ind, chunk in enumerate(day_chunks):

        # Add to processes list for multiprocessing, using
        # extract_data function
        args = (extract_data, [chunk_ind, chunk], queue)
        processes.append(Process(target=_mp_queue, args=args))

    # Start processes
    for process in processes:
        process.start()

    # Collect output from processes and close queue
    out_list = [queue.get() for _ in processes]
    queue.close()


def extract_data(ind, days):

    # Lists (and dictionary) to add tweet info to
    ids, dates, geos, places, duplicates, bad_tweets = [], [], [], [], [], []
    tweets_by_day = {}
    tweets_by_hour = {'week': {}, 'weekend': {}}

    # Open all json files and append each line to tweets list
    for day in days:
        for hour in range(24):

            # Define zip filename
            zip_fname = (f'{SCRATCH_PATH}/geoEurope_202106{day:02d}{hour:02d}'
                         '.zip')

            # Unzip file
            with ZipFile(zip_fname, 'r') as zip_file:
                zip_file.extractall(path=f'{SCRATCH_PATH}')

            # Define filename
            fname = (f'{SCRATCH_PATH}/geoEurope/geoEurope_202106'
                     f'{day:02}{hour:02d}.json')

            # Move to next iteration if file does not exist
            if not os.path.exists(fname):
                print(f'{fname} does not exist')
                continue

            # Append each line of file to tweets list
            for line in open(fname, 'r'):

                # Load tweet
                tweet = json.loads(line)

                # Add relevant tweet info to list if possible
                if 'id' in tweet:
                    id = tweet['id']

                    # If id not already in ids list, append it and get
                    # other info from tweet
                    if id not in ids:
                        ids.append(id)

                        # Get date tweet created if possible
                        if 'created_at' in tweet:

                            # Get date string from tweet
                            date = tweet['created_at']

                            # Get month string
                            month_str = date[4:7]

                            # Ignore if month not June (some in May)
                            if month_str != 'Jun':
                                continue

                            # Get other time elements to convert to dt
                            d_month = 6 # Month always Jun (ignored if not)
                            d_day = int(date[8:10])
                            d_hour = int(date[11:13])
                            d_minute = int(date[14:16])
                            d_second = int(date[17:19])
                            d_year = int(date[26:30])

                            # Convert to datetime object
                            date_dt = dt.datetime(d_year, d_month, d_day,
                                                  d_hour, d_minute,
                                                  d_second)

                            # Append datetime to list
                            dates.append(date_dt)

                            # Get datetime ignoring hours, minutes, etc
                            day_dt = dt.datetime(d_year, d_month, d_day)

                            # If day already in dictionary, add to count
                            if day_dt in tweets_by_day:
                                tweets_by_day[day_dt] += 1

                            # Add key to dictionary if day not in there,
                            # with initial count of 1
                            else:
                                tweets_by_day[day_dt] = 1

                            # Get datetime ignoring minutes, etc
                            hr_dt = dt.datetime(d_year, d_month, d_day,
                                                d_hour)

                            # Add count to appropriate hour dictionary
                            # Weekend 5-6, week day 0-4
                            if hr_dt.weekday() in [5, 6]:

                                # Add to count if hour in dictionary
                                if hr_dt in tweets_by_hour['weekend']:
                                    tweets_by_hour['weekend'][hr_dt] += 1

                                # Otherwise, make key with initial count 1
                                else:
                                    tweets_by_hour['weekend'][hr_dt] = 1

                            # Same for week days
                            else:

                                # Add to count if hour in dictionary
                                if hr_dt in tweets_by_hour['week']:
                                    tweets_by_hour['week'][hr_dt] += 1

                                # Otherwise, make key with initial count 1
                                else:
                                    tweets_by_hour['week'][hr_dt] = 1

                        # Get location coordinates if possible
                        if tweet['geo']:
                            geo = tweet['geo']['coordinates']
                            geos.append(geo)

                        # Otherwise, get place info
                        elif ('place' in tweet and
                              'bounding_box' in tweet['place'] and
                              'coordinates' in
                              tweet['place']['bounding_box']):
                            plc = tweet['place']['bounding_box']['coordinates']
                            places.append(plc)

                    # Otherwise, append it to duplicates list
                    else:
                        duplicates.append(id)

                # If no id, print tweet
                else:
                    bad_tweets.append(tweet)

            # Remove json file to prevent disk filling up
            os.system(f'rm {fname}')

    # Pickle lists
    t_lists =  [ids, dates, geos, places, duplicates, bad_tweets,
                tweets_by_day, tweets_by_hour]
    for t_list, t_str in zip(t_lists, T_STRS):
        uf.pickle_data(t_list, f'{SCRATCH_PATH}/pickles/{t_str}_{ind}')


def _mp_queue(function, args, queue):
    """
    Wrapper function for allowing multiprocessing of a function and
    ensuring that the output is appended to a queue, to be picked up later.

    :param function: Function being called in queue
    :type function: function
    :param args: Arguments used in funtion
    :type args: list
    :param queue: Queue
    :type queue: multiprocessing.Queue
    """
    queue.put(function(*args))


def day_plot(day_dict):

    # Sort dictionary and return list of tuples
    days_tweets = sorted(day_dict.items())

    # Unpack into x and y lists
    days, tweets = zip(*days_tweets)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot line
    ax.plot(days, tweets)

    # Formatting, etc
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.set_ylabel('Number of tweets')
    ax.set_xlabel('Date')
    ax.grid(axis='x')

    # Save and close figure
    plt.tight_layout()
    fig.savefig('tweets_per_day.png')
    plt.close()


def box_plot(tweets_by_day):

    # Get dictionary with number of tweets on weekend/week days
    week_weekend_tweets = {'week': [], 'weekend': []}

    # Add numbers of tweets to dictionary
    for day in tweets_by_day:

        # Check if weekday (0-4) or weekend (5-6) and append value to
        # appropriate list
        if day.weekday() in [5, 6]:
            week_weekend_tweets['weekend'].append(tweets_by_day[day])
        else:
            week_weekend_tweets['week'].append(tweets_by_day[day])

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Make box and whisker plots
    ax.boxplot(week_weekend_tweets.values())

    # Formatting, etc
    ax.set_xticklabels(week_weekend_tweets.keys())
    ax.set_ylabel('Number of tweets')
    ax.set_xlabel('Date')

    # Save and close figure
    plt.tight_layout()
    fig.savefig('box_days.png')
    plt.close()


def hour_plot(tweets_by_hour):

    # Get mean number of tweets per hour for weekend and week days
    hrs_week, mean_tweets_week = mean_hours(tweets_by_hour, 'week')
    hrs_weekend, mean_tweets_weekend = mean_hours(tweets_by_hour, 'weekend')

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot line
    ax.plot(hrs_week, mean_tweets_week, label='week days')
    ax.plot(hrs_weekend, mean_tweets_weekend, label='weekend days')

    # Formatting, etc
    ax.set_ylabel('Mean number of tweets')
    ax.set_xlabel('Hour (UTC)')
    ax.grid(axis='x')
    ax.legend()

    # Save and close figure
    plt.tight_layout()
    fig.savefig('tweets_per_hour.png')
    plt.close()


def mean_hours(date_dict, day_type):

    # Dictionary with lists to append to
    mean_tweets = {hour: [] for hour in range(24)}

    # Append number of tweets per hour to appropriate list in dictionary
    for hour_dt in date_dict[day_type]:
        hr = hour_dt.hour
        mean_tweets[hr].append(date_dict[day_type][hour_dt])

    # Get mean of each list in dictionary
    hour_means = {hour: np.mean(mean_tweets[hour]) for hour in mean_tweets}

    # Sort dictionary
    sorted_hour_means = sorted(hour_means.items())

    # Unpack into x and y lists for plotting
    hours, mean_tweets = zip(*sorted_hour_means)

    return hours, mean_tweets


def combine_dicts(big_dict, small_dict):

    for period in small_dict:
        if period in big_dict:
            big_dict[period] += small_dict[period]
        else:
            big_dict[period] = small_dict[period]

    return big_dict


if __name__ == "__main__":

    # Print time
    time_1 = uf.print_time('started')

    # Get user argument
    new_data = sys.argv[1]

    # Run main function
    main(new_data)

    # Print time
    time_2 = uf.print_time('Finished')

    # Print time taken
    uf.time_taken(time_1, time_2, unit='seconds')
