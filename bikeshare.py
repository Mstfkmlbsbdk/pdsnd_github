import time
import pandas as pd
import numpy as np
import math

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    uniq_cityname=['chicago','new york city', 'washington']
    
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington? Enter a valid city : ').lower()
        if city in uniq_cityname:
            print('Thanks, one moment while we fetch the data')
            break
        
        #Exit Program
        else:
            print ("Please, Enter a valid city name. Try again.")
        
    # get user input for month (all, january, february, ... , june)
    while True:
        month=input('Which month - January, February, March, April, May, or June? Please enter a valid month : ').lower()
        if month in ['january','february','march','april','may','june','all']:
            break
        else:
            print('Please, Enter a valid month. Try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Please enter a valid day : ').title()
        if day in  ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
            break
        else:
            print('Please, Enter a valid month. Try again.')


    print('-'*40)
    return city, month, day


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

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    
    # filter by month if applicable
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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    #df['month'] = df['Start Time'].dt.month 

    # find the most popular month
    popular_month = df['month'].value_counts().idxmax()

    print('The Most Popular Month:', popular_month)

    # display the most common day of week
    df['week'] = df['Start Time'].dt.weekday_name

    # find the most popular week
    popular_week = df['week'].value_counts().idxmax()

    print('The Most Popular Start Day of Week:', popular_week)

    # display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].value_counts().idxmax()

    print('The Most Popular Start Hour:', popular_hour, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #a=df.columns
    #print(a)

    return df

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]

    print('Most Commonly Used Start Station: ',start_station, "\n")

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]

    print('Most Commonly Used End Station: ',end_station, "\n")

    # display most frequent combination of start station and end station trip

    df['start_end_combination'] = df.apply(lambda x:'%s - %s' % (x['Start Station'],x['End Station']),axis=1)

    combination=df['start_end_combination'].mode()[0]

    print('Most Frequent Combination of Start Station and End Station Trip: ',combination, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return df

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel=df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel, "\n")


    # display mean travel time
    mean_travel=df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel, "\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    
    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")

    # Display counts of gender
    if city != 'washington':
        
        gender_counts = df.groupby(['Gender'])['Gender'].count()
        
        print('Total Counts of Gender', gender_counts, "\n")
        

        # Display earliest, most recent, and most common year of birth
        birth_year = df['Birth Year']
    
        # the most earliest birth year
        earliest_year = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        print("Most Elderly User Birth Year: ", earliest_year, "\n")
    
        # the most recent birth year
        most_recent = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        print("Youngest User Birth Year: ", most_recent, "\n")
    
        # the most common birth year
        most_common_year =  df['Birth Year'].mode()[0]
        print("The Most Common Birth Year:", most_common_year, "\n")
    else:
        print('There is no information about Gender for Washington\n')
        
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    x = 1
    while True:
        raw_data=input('Do you want to see some raw data? Enter Yes or No.\n')
        if raw_data.lower() == 'yes':
            print(df[x:x+3])
            x +=3
        else:
            break
         
              
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
