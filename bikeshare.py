import time
import pandas as pd
import numpy as np

"""
Reads  in rideshare data in three cities from three .csv files
(chicago.csv, new_york_city.csv and washington.read_csv)
Reads data into the dictionary CITY_DATA
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    """
    FUNCTION: get_filters:
    Asks user to specify a city, month, and day to analyze. Uses while loops
    to check for valid input.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city = " "
    day = " "
    month = " "

    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city. Uses while loop to check for valid input

    while city not in ( 'chicago', 'new york city', 'washington'):
        city = input("Which city would you like to analyze: Chicago, New York City or Washington? ").lower()
        if city in ('chicago', 'new york city', 'washington'):
            continue
        else:
            print('Please enter a valid city.')

    # Gets user input for month (all, january, february, ... , june). Uses while loop
    # to check for valid input. Allows for capitalized or non-capitalized forms.


    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input("Which month would you like to analyze? Type 'all' if you would like to see data for all months  ").lower()
        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june' ):
            continue
        else:
            print('Please enter a valid month, January to June only')


    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
        day = input("Which day of the week would you like to analyze? Type 'all' if you would like to see all days  ").lower()
        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            continue
        else:
            print('Please enter a valid day of the week. For example: Monday, Tueday. Wednesday, etc...')


    print('-'*40)
    return city, month, day

"""
Function: load_data
This function loads the the data from the CITY_DATA dictionary based on the
user's requests for city, month and day and returns the DataFrame df.

Returns: df; which is a DataFrame of the CITY_DATA filtered based on user's
requests/
"""

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

# converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name



# filter by month based on user's request, if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

# filter by month to create the new dataframe
        df = df[df['month'] == month]

# filter by day of week if applicable
    if day != 'all':

# filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

"""
Function: time_stats

Loads in the DataFrame df and calculates a variety of time-related statistics
and then prints those statistics

No output of than print statements
"""

def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]

    print('Most popular month is: ', popular_month)

    popular_day = df['day_of_week'].mode()[0]

    print('Most popular day is: ', popular_day)

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)


"""
Function: station_stats

Loads in the DataFrame df and calculates a variety of station-related
statistics and then prints those statistics

No output of than print statements
"""
def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')

    df['Route'] = df['Start Station'] + " TO " + df['End Station']

    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station is: ', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station is: ', popular_end_station)

    popular_route = df['Route'].mode()[0]
    print('Most popular route is: ', popular_route)

"""
Function: trip_duration_stats

Loads in the DataFrame df and calculates a variety of  trip duration-related
statistics and then prints those statistics

No output of than print statements
"""

def trip_duration_stats(df):

    print('\nCalculating average and total travel times...\n')

    tot_travel_time = df['Trip Duration'].sum()
    ave_travel_time = df['Trip Duration'].mean()

    print('The total travel time is: ', tot_travel_time)
    print('The average travel time is: ', ave_travel_time)



"""
Function: user_stats

Loads in the DataFrame df and calculates a variety of user-related statistics
and then prints those statistics

No output of than print statements
"""
def user_stats(df):

    print('\nCalculating User Stats...\n')

    user_types = df['User Type'].value_counts()
    print('The user types are: ', user_types)

# This is an exception b/c Washington doesn't include data on gender.

    try:
        gender_types = df['Gender'].value_counts()
        print('The gender split of users is: ', gender_types)
    except KeyError:
        print("Washington doesn't have gender data")

    try:
        birth_year_min = df['Birth Year'].min()
        birth_year_max = df['Birth Year'].max()
        birth_year_mode = df['Birth Year'].mode()

        print('The minimum birth year is: ', birth_year_min)
        print('The maximum birth year is: ', birth_year_max)
        print('The most common birth year is: ', birth_year_mode)
    except KeyError:
        print("Washington doesn't have data on birth year")


def display_data(df):
    question = input('Would like like to see the first five lines of the data? ')
    count = 0

    if question in ('Yes', 'yes', 'y', 'No', 'no', 'n'):
        if question in ('Yes', 'yes', 'y'):
            print(df.head(5))


            while question in ('Yes', 'yes', 'y'):
                question = input('Would like like to see the five more lines of data? ')
                count += 5

                if question in ('Yes', 'yes', 'y'):
                    print(df[count:count+5])

    else:
        print('Invalid answer. Lines of data not printed')


"""
This is the main() function which calls all the other functions
in a specified order.

This is the section of the program that I found the most difficult.

"""
def main():
    city, month, day = get_filters()
    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    display_data(df)


if __name__ == "__main__":
    main()
