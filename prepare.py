import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

########################################################################################## 
# My Prepare Functions

##########################################################################################
def set_index(df, date_col):
    '''
    Converts column to datetime and sets as the index
    '''
    df[date_col] = pd.to_datetime(df[date_col])
    
    df = df.set_index(date_col).sort_index()
    
    return df

def visualize(df, x, y, title):
    '''
    plots a scatter plot of x vs y, and then a pairplot of the complete df
    '''

    plt.scatter(x=x, y=y)
    plt.title('title')
    plt.show()
    
    sns.pairplot(df)

def sales_total():
    
    df['sales_total'] = df.sale_amount * df.item_price
    
    return df

def create_date_columns(df, date_types, date_col):
    '''
    'year','month','day','hour','week','weekday','weekday_name','quarter'
    create columns of these date types using date index or column
    date_col must be set to a pandas datetime
    '''
    
    # if date columns has already been set to index
    if date_col == 'index':
        for x in date_types:
            
            # will add the date column for every date type in the list
            if x == 'year':
                df['year'] = df.index.year
                
            if x == 'month':
                df['month'] = df.index.month
                
            if x == 'day':
                df['day'] = df.index.day
                
            if x == 'hour':
                df['hour'] = df.index.hour
                
            if x == 'week':
                df['week'] = df.index.week
                
            if x == 'weekday':
                df['weekday'] = df.index.weekday
                
            if x == 'weekday_name':
                df['weekday_name'] = df.index.day_name()
                
            if x == 'quarter':
                df['quarter'] = df.index.quarter
                
    # if date column has not yet been set to index
    else:
        for x in date_types:
            
            # will add the date column for every date type in the list
            if x == 'year':
                df['year'] = df[date_col].dt.year
                
            if x == 'month':
                df['month'] = df[date_col].dt.month
                
            if x == 'day':
                df['day'] = df[date_col].dt.day
                
            if x == 'hour':
                df['hour'] = df[date_col].dt.hour
                
            if x == 'week':
                df['week'] = df[date_col].dt.week
                
            if x == 'weekday':
                df['weekday'] = df[date_col].dt.weekday
                
            if x == 'weekday_name':
                df['weekday_name'] = df[date_col].dt.day_name()
                
            if x == 'quarter':
                df['quarter'] = df[date_col].dt.quarter
    
    return df
    
def sales_total():
    '''
    creates a new column for sales total
    '''
    df['sales_total'] = df.sale_amount * df.item_price
    
    return df




##########################################################################################

# Preparation of Zach's Sales Data

##########################################################################################



def prep_sales():
    '''
    
    In order to run this function: the function complete_data must have been run.
    
    This function takes output of complete_data from the acquire.py function, preps, and returns the dataframe for exploration.
    
    '''
    
    # Creates dataframe from complete_data function in acquire.py
    df = a.complete_data(cached=True)
    
    # sale_date column is converted to datetime and set as the index
    df.sale_date = pd.to_datetime(df.sale_date)
    df.set_index(df.sale_date, inplace=True)
    
    # Create the columns 'month' and 'day_of_week'
    df['month'] = df.index.month
    df['day_of_week'] = df.index.day_name()
    
    # Create 'sale_total' column
    df['sales_total'] = df.sale_amount * df.item_price
    
    return df




##########################################################################################

# Preparation of Germany Energy Consumption Data

##########################################################################################


def prep_germany(cached=False):
    '''
    
    This function pulls and preps the Germany Energy Consumption dataframe for exploration
    
    if cached == False: collects the csv from the url
    if cached == True: pulls the already saved dataframe
    
    '''
    
    if cached == False: 
        # url to opsd_germany_daily.csv
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        # uses pull_csv function from acquire.py to collect the dataset
        df = a.pull_csv(url)
        # caches the dataset as a csv 
        df = pd.to_csv('opsd_germany_daily.csv')
        
    # cached == True
    else:
        # pulls csv as data from
        df = pd.read_csv('opsd_germany_daily.csv')
    
    # Lowercases the columns and renames 'wind+solar' columns to 'wind_and_solar'
    df.columns = df.columns.str.lower() 
    df.rename(columns={'wind+solar': 'wind_and_solar'}, inplace=True)
    
    # Conver date to datetime and set date as index
    df.date = pd.to_datetime(df.date)
    df.set_index(df.date, inplace=True)
    
    # Creates the month and year columns
    df['month'] = df.index.month
    df['year'] = df.index.year
    
    # Fills nulls with 0 
    df.fillna(0, inplace=True)
    
    return df






##########################################################################################

# Zero's and NULLs

##########################################################################################



#----------------------------------------------------------------------------------------#
###### Easley




def prep_store_data(df):
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y %H:%M:%S %Z')
    # make sure we sort by date/time before resampling or doing other time series manipulations
    df = df.set_index('sale_date').sort_index()
    df = df.rename(columns={'sale_amount': 'quantity'})
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['sales_total'] = df.quantity * df.item_price
    return df

def prep_opsd_data(df):
    df.columns = [column.lower() for column in df]
    df = df.rename(columns={'wind+solar': 'wind_and_solar'})

    df.date = pd.to_datetime(df.date)
    df = df.set_index('date').sort_index()

    df['month'] = df.index.month
    df['year'] = df.index.year

    df = df.fillna(0)
    return df