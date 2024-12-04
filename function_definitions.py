
# IMPORT LIBRARIES

import pandas as pd  


# NOTEBOOK 1A: GENERAL DATA CLEANING 

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
    
# NOTEBOOK 1B: SEVERITY SCORE

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

# NOTEBOOK 1C: SELECT SUBJECT

def subject_selector(df, subject):
    """
    Function takes a data frame and a string with a subject name as input.
    It processes the 'subject' column by splitting its values separated by semicolons, 
    filters the data frame to include only rows with the specified subject, then
    returns the filtered data frame.
    """

    # Create series with exploded subjects by splitting the 'subject' column
    
    exploded_subjects = df['subject'].str.split(';').explode()
    
    # Drop the original 'subject' column and join the exploded subjects
    
    df = df.drop('subject', axis=1).join(exploded_subjects.rename('subject'))
    
    # Filter the data frame for the specified subject
    
    subject_df = df[df['subject'] == subject]
    
    # Return filtered data frame
    
    return subject_df

# NOTEBOOK 2A: GET JSON RETRACTED

# Define address_builder function

def address_builder(doi):
    """Takes a DOI identifier and builds the full URL address to perform an API call
    on OpenAlex from it"""
    
    # Build url address and store it in string   
    
    base_address = "https://api.openalex.org/works/https://doi.org/" + doi
    polite_address = base_address + "?mailto=" + "pabloruizdeolano@gmail.com" # Use polite address for faster API call performance
    
    # Return url address
    
    return polite_address


# Define function to obtain .json files for all papers in our data frame

"""
Function takes a data frame two file paths to two directories, extracts a list of DOIs from
the "original_paper_doi" column of input data frame and performs one API call per DOI, 
writes outcome as .json file in one of the two specified directories. If also keeps a log of successful and
failed API calls, writes log as a .csv file in second directory.

"""

def fetch_json_files(df, json_directory, log_directory):
    
    # Create empty list to store log with success or failure of each API call
    
    log = []
    
   # For loop to perform one API call per DOI in input data frame

    for doi in df['original_paper_doi']:
    
        # Skip empty or invalid DOIs
    
        if not isinstance(doi, str) or not doi.strip(): 
            log.append({'DOI': doi, 'Status': 'Skipped - Empty or Invalid DOI'}) 
            continue  
    
        try:
            # Build url address by calling address_builder function
            
            url = address_builder(doi)
        
            # Perform API call using URL address and store result in variable
            
            response = requests.get(url, timeout=10)  # Added timeout to prevent hanging requests
        
            # If clause to control for case in which API call fails
            
            if response.status_code == 200:
            
                # Convert result of API call to json format
            
                data = response.json()
            
                # Create file path to save .json file with result of API call
            
                full_path = os.path.join(json_directory, doi.replace('/', '_') + '.json')
            
                # Save result of API call to .json file
                
                with open(full_path, 'w') as file:
                    json.dump(data, file)
            
                # Update log list with dictionary specifying success for current DOI
            
                log.append({'DOI': doi, 'Status': 'Success'})
        
            else:
                # Update log list with dictionary specifying failure for current DOI
                
                log.append({'DOI': doi, 'Status': f"Failed - {response.status_code}"})
    
        except requests.RequestException as e:
            
            # Handle exceptions during the API call (e.g., connection errors, timeouts)
            
            log.append({'DOI': doi, 'Status': f"Failed - {str(e)}"})

    # Convert log list to data frame 
    
    df_log = pd.DataFrame(log)
    
    # Write content of log data frame into resulting path
    
    df_log.to_csv(log_directory, index=False)
    

# Define function to obtain .json files for all papers in our data frame

"""
Function takes a data frame two file paths to two directories, extracts a list of DOIs from
the "original_paper_doi" column of input data frame and performs one API call per DOI, 
writes outcome as .json file in one of the two specified directories. If also keeps a log of successful and
failed API calls, writes log as a .csv file in second directory.

"""

def fetch_json_files(df, json_directory, log_directory):
    
    # Create empty list to store log with success or failure of each API call
    
    log = []
    
   # For loop to perform one API call per DOI in input data frame

    for doi in df['original_paper_doi']:
    
        # Skip empty or invalid DOIs
    
        if not isinstance(doi, str) or not doi.strip(): 
            log.append({'DOI': doi, 'Status': 'Skipped - Empty or Invalid DOI'}) 
            continue  
    
        try:
            # Build url address by calling address_builder function
            
            url = address_builder(doi)
        
            # Perform API call using URL address and store result in variable
            
            response = requests.get(url, timeout=10)  # Added timeout to prevent hanging requests
        
            # If clause to control for case in which API call fails
            
            if response.status_code == 200:
            
                # Convert result of API call to json format
            
                data = response.json()
            
                # Create file path to save .json file with result of API call
            
                full_path = os.path.join(json_directory, doi.replace('/', '_') + '.json')
            
                # Save result of API call to .json file
                
                with open(full_path, 'w') as file:
                    json.dump(data, file)
            
                # Update log list with dictionary specifying success for current DOI
            
                log.append({'DOI': doi, 'Status': 'Success'})
        
            else:
                # Update log list with dictionary specifying failure for current DOI
                
                log.append({'DOI': doi, 'Status': f"Failed - {response.status_code}"})
    
        except requests.RequestException as e:
            
            # Handle exceptions during the API call (e.g., connection errors, timeouts)
            
            log.append({'DOI': doi, 'Status': f"Failed - {str(e)}"})

    # Convert log list to data frame 
    
    df_log = pd.DataFrame(log)
    
    # Write content of log data frame into resulting path
    
    df_log.to_csv(log_directory, index=False)
    

# Define function to remove papers for which we already have a .json file from original data frame

def non_downloaded_papers_selector(df, existing_doi_df):
    """
    Function takes an input data frame and a data frame with a list of DOIs, returns 
    the input data frame without those papers whose DOIs where included in the list.
    """

    # Create data frame with DOIs of papers that have not been downloaded only
    
    df_not_downloaded = df[~df['original_paper_doi'].isin(existing_doi_df['doi'])]
    
    # Return data frame
    
    return df_not_downloaded

# NOTEBOOK 2C: EXTRACT ABSTRACTS RETRACTED

# Define function to remove non-printable characters

def remove_non_printable(text):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, text))

# NOTEBOOK 3A: FETCHING DOIS NON-RETRACTED




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

# 