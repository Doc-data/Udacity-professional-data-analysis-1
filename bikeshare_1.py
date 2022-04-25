import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


# Provide an interface for the user to input the filters

def check_input(input_str, input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read = input(input_str).lower()
        try:
            if input_read in ['chicago', 'new york city', 'washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 2:
                break
            elif input_read in ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                                'all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Sorry, your input should be: chicago new york city or washington")
                if input_type == 2:
                    print("Sorry, your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    print("Sorry, your input should be: saturday, sunday, monday, tuesday, wednesday, thursday, "
                          "friday or all")
        except ValueError:
            print("Sorry, your input is not valid \n" + "Please try again")
    return input_read


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """

    # Hello message
    print('Hello! Let\'s explore some US bike share data!')

    # get user input for city
    city = check_input("Please enter the name of the city you want to be analysed", 1)

    # get user input for month
    month = check_input("Please enter the name of the month you want to be analysed or enter (all)", 2)

    # get user input for day of week
    day = check_input("Please enter the name of the day you want to be analysed or enter (all)", 3)

    print('-' * 40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df["month"] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[month == df['month']]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the most common month
    pop_month = df["month"].mode()[0]
    print('The most popular month is: ', pop_month)

    # the most common day of week
    pop_day = df['day_of_week'].mode()[0]
    print('The most day of the week is: ', pop_day)

    # the most common start hour
    pop_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', pop_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print('The most common starting station is:', pop_start)

    # most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print('The most common ending station is:', pop_end)

    # most frequent combination of start station and end station trip
    group_field = df.groupby(['Start Station', 'End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('The most frequent trip is:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    sum_time = df['Trip Duration'].sum()
    print('The total travel time is: ', sum_time)

    # mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The average travel time is:', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Gender and birth year
    if city == 'washington':
        pass
    else:
        # counts of gender
        print('Gender Stats:')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('Birth Year Stats:')
        common_year = df['Birth Year'].mode()[0]
        print('The most common user birth year is: ', common_year)

        recent_year = df['Birth Year'].max()
        print('The most recent users birth year is: ', recent_year)

        earliest_year = df['Birth Year'].min()
        print('The earliest users birth year is: ', earliest_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
