import time
import pandas as pd
import numpy as np
#comment test
# Dictionary to map city names to their respective data files
CITY_FILES = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_user_inputs():
    """Asks the user to specify a city, month, and day to analyze."""
    print('Hello! Welcome To The Bike Share Data Exploration!')

    # City selection
    while True:
        selected_city = input('Choose a city (Chicago, New York City, Washington):\n').lower()
        if selected_city in CITY_FILES:
            break
        else:
            print('Invalid input. Please enter a valid city name.')

    # Time filter selection
    while True:
        filter_type = input('Filter data by day, month, both, or "none" for no filter:\n').lower()
        if filter_type in ['month', 'day', 'both', 'none']:
            break
        else:
            print('Invalid input. Choose "month", "day", "both", or "none".')

    chosen_month = 'none'
    chosen_day = None

    # Month selection
    if filter_type in ['month', 'both']:
        while True:
            chosen_month = input('Which month? January, February, March, April, May, or June?\n').lower()
            if chosen_month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Invalid input. Enter a valid month name.')

    # Day selection
    if filter_type in ['day', 'both']:
        while True:
            try:
                chosen_day = int(input('Which day? Enter an integer (1=Sunday, 7=Saturday):\n'))
                if 1 <= chosen_day <= 7:
                    break
                else:
                    print('Invalid input. Enter a number between 1 and 7.')
            except ValueError:
                print('Invalid input. Enter a valid number between 1 and 7.')

    print('-' * 40)
    return selected_city, chosen_month, chosen_day

def load_bike_data(selected_city, chosen_month, chosen_day):
    """Loads data based on the user's selection."""
    df = pd.read_csv(CITY_FILES[selected_city])
    
    # Convert Start Time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.dayofweek + 1  # 1 = Sunday, 7 = Saturday
    
    # Apply month filter
    if chosen_month != 'none':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(chosen_month) + 1
        df = df[df['Month'] == month_index]
    
    # Apply day filter
    if chosen_day:
        df = df[df['Day of Week'] == chosen_day]
    
    return df

def display_time_stats(df):
    print('\nFinding Most Frequent Travel Times...\n')
    start = time.time()
    
    print('Most common month:', df['Month'].mode()[0])
    print('Most common day of week:', df['Day of Week'].mode()[0])
    print('Most common start hour:', df['Start Time'].dt.hour.mode()[0])
    
    print("\nTime taken: %s seconds." % (time.time() - start))
    print('-' * 40)

def display_station_stats(df):
    print('\nFinding Most Popular Stations and Trips...\n')
    start = time.time()
    
    print('Most common start station:', df['Start Station'].mode()[0])
    print('Most common end station:', df['End Station'].mode()[0])
    
    common_route = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'Most common trip: From {common_route[0]} to {common_route[1]}')
    
    print("\nTime taken: %s seconds." % (time.time() - start))
    print('-' * 40)

def display_trip_duration_stats(df):
    print('\nCalculating Trip Durations...\n')
    start = time.time()
    
    print('Total travel time:', df['Trip Duration'].sum(), 'seconds')
    print('Average travel time:', df['Trip Duration'].mean(), 'seconds')
    
    print("\nTime taken: %s seconds." % (time.time() - start))
    print('-' * 40)

def display_user_stats(df, selected_city):
    print('\nAnalyzing User Data...\n')
    start = time.time()
    
    print('User Type Counts:\n', df['User Type'].value_counts())
    
    if selected_city in ['chicago', 'new york city']:
        print('Gender Counts:\n', df['Gender'].value_counts(dropna=True))
        print('Earliest birth year:', int(df['Birth Year'].min()))
        print('Most recent birth year:', int(df['Birth Year'].max()))
        print('Most common birth year:', int(df['Birth Year'].mode()[0]))
    
    print("\nTime taken: %s seconds." % (time.time() - start))
    print('-' * 40)

def display_raw_data(df):
    row_index = 0
    while True:
        show_data = input('\nWould you like to see the raw data? Enter yes or no:\n').lower()
        if show_data != 'yes':
            break
        print(df.iloc[row_index: row_index + 5])
        row_index += 5
        if row_index >= len(df):
            print("\nNo more data to display.")
            break
            
def main():
    """Main function to execute the bike data analysis program."""
    while True:
        selected_city, chosen_month, chosen_day = get_user_inputs()
        df = load_bike_data(selected_city, chosen_month, chosen_day)

        display_time_stats(df)
        display_station_stats(df)
        display_trip_duration_stats(df)
        display_user_stats(df, selected_city)
        
        # Display raw data upon request
        display_raw_data(df)

        restart_prompt = input('\nWould you like to restart? Enter yes or no:\n').lower()
        if restart_prompt != 'yes':
            break

if __name__ == "__main__":
    main()
