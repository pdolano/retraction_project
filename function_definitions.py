
# IMPORT LIBRARIES

import pandas as pd  


# NOTEBOOK 1: DATA CLEANING

# Define percentage_finder_nan function

def percentage_finder(df, col_name, val_name):
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

# NOTEBOOK 2A

def separate_and_clean_reasons(reasons_string, delimiter = ";", extra_symbol = ""):
    """Function takes a single string containing multiple reasons separated by a given delimiter 
    and returns a list with all individual reasons as its elements, removing white spaces
    and any other extraneous symbols of choice, and the delimiter simbol."""
    
    
    # Return empty list is reasons string is NaN
    
    if pd.isna(reasons_string):
        return []

    # Store invididual reasons as separated by delimiter in list
    
    individual_reasons_list = reasons_string.split(delimiter)  
    
    # Intialize another list to store cleaned individual reasons
    
    clean_reasons_list = [] 
    
    # For loop to clean individual reasons by dropping delimiter and extra symbols
    
    for individual_reason in individual_reasons_list:
        
        # Clean individual reason and store it in new variable
        
        clean_individual_reason = individual_reason.strip(f"{delimiter}{extra_symbol} ")
        
        # If not empty, append clean individual reason to clean individual reasons list
        
        if clean_individual_reason:  
            clean_reasons_list.append(clean_individual_reason)
            
    # Return list with individual clean reasons
    
    return clean_reasons_list


def get_max_severity(reason_list):
    """Function takes a list with reasons for retraction, checks what are the severity scores
    associated to each individual reason, then returns the maximum score in that collection."""
    
    # Create list with scores associated to reasons in input list
    
    scores = df_severity[df_severity['reason'].isin(reason_list)]['severity_score']
    
    # Return maximum vaue in the scores list
    
    return max(scores) if not scores.empty else None

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
