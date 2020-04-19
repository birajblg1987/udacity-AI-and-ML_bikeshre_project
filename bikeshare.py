import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june','all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington).
    city = ""
    while city not in CITY_DATA:
        city = input("Select a city from chicago, new york city, washington to analyze: ") .lower()
 
    #get user input for month (all, january, february, ... , june)
    month = ""
    while month not in MONTHS:
        month = input("Select a month from {} to analyze \n[remember months are case sensitive]: ".format(MONTHS)).lower()
        
    #get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day not in DAYS:
        day = input("Select a day from {} to analyze \n[remember days are case sensitive]: ".format(DAYS)).lower()

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
    selected_city = CITY_DATA.get(city)
    df = pd.read_csv(selected_city)
    
     # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)+1
        
        # filter by month to create the new dataframe
        df = df[df.month==month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = DAYS.index(day)
        df = df[df.day_of_week==day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    print("Most common month: ",MONTHS[df['month'].mode().values[0]-1])

    #display the most common day of week
    print("Most common day of week: ",DAYS[df['day_of_week'].mode().values[0]])

    #display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    print("Most common start hour: ", df['hour'].mode().values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    print("Most common start station: ", df['Start Station'].mode().values[0])

    #display most commonly used end station
    print("Most common end station: ", df['End Station'].mode().values[0])

    #display most frequent combination of start station and end station trip
    df['Start & End'] = df['Start Station']+', '+df['End Station']
    print("Most common combination of start station and end station: ", 
          df['Start & End'].mode().values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print("Total travel time: ", np.sum(df['Trip Duration'])/3600, "hours")

    #display mean travel time
    print("Mean travel time: ", np.mean(df['Trip Duration']), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print("Count of user types:\n", df['User Type'].value_counts())

    #Display counts of gender
    columns = df.columns
    if 'Gender' in columns:
        print("Count of gender:\n", df['Gender'].value_counts())

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in columns:
        print("Earliest year of birth: ",np.min(df['Birth Year']))
        print("Most recent year of birth: ",np.max(df['Birth Year']))
        print("Most common year of birth: ",df['Birth Year'].mode().values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def dataprint(df):
    pd.set_option('display.max_columns', None)
    
    #asking user if raw data to be displayed or not
    user_input = ""
    user_input2 = ""
    istart = 0
    iend = 5
    while user_input.lower() != 'yes' and user_input.lower() != 'no':
        user_input = input("Do you want to see the first five lines of the data? ('yes' or 'no'): ")
    
    #print data based on user's confirmation
    if user_input.lower() == 'yes':
        print("\n Printing first five lines of raw data...")
        print(df.iloc[istart:iend,:])
        istart += 5
        iend += 5
    
        #take user confirmation for next five items
        while user_input2.lower() != 'no':
            user_input2 = input("Do you want to see next five lines? ('yes' or 'no') ")
            
            #print next five items if user says yes
            if user_input2.lower() == 'yes':
                print(df.iloc[istart:iend,:])
                istart += 5
                iend += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        dataprint(df)
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
