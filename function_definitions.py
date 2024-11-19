

# NOTEBOOK 1: DATA CLEANING

# Define percentage_finder_nan function

def percentage_finder_nan(df, col_name, val_name):
    """This function takes a data frame, the name of a column, and one of the 
    possible values of the column. It then returns how often that one value 
    occurs in that column of the data frame."""
    
    if pd.isna(val_name):  # In case we want to check how many entries are NanNs
        count = df[col_name].isna().sum()
    else:
        count = df[df[col_name] == val_name][col_name].count()
        
    percentage = (count / len(df[col_name])) * 100
        
    #print(f"The percentage of entries with value {val_name} in column {col_name} is: {round(percentage,2)}%")
    
    return percentage

# Define percentage_printer function

def percentage_printer(df, col_name):
    """This function takes a data frame and a column name as input. It then calls
    the percentage_finder function to print the percentage of occurrances of each
    value of the column."""
        
    val_list = []
    val_list = df[col_name].unique()
        
    for value in val_list:
        percentage = percentage_finder(df, col_name, value)
        print(f"{value}: {round(percentage,2)}%")


# Define histogram printer function

def histogram_printer(df, col_name):
    """Takes a data frame and a column name as input, produces a histogram
    for the vaulues of that column of the data frame"""
    
    df[col_name].hist()


# NOTEBOOK X

def seconds_to_hms(seconds):
    """
    Convert seconds to hours, minutes, and seconds.
    
    Args:
        seconds (int): Number of seconds.
        
    Returns:
        tuple: A tuple containing the number of hours, minutes, and remaining seconds.
    """
    
    # Calculate hours, minutes, and remaining seconds
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return hours, minutes, seconds
