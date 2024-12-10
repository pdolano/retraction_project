
# IMPORT LIBRARIES

import pandas as pd  
import requests
import os
import json
import string


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
    

# Define function to get list of already downloaded DOIs

def downloaded_paper_list_getter(directory, log_directory):
    """
    Function takes a file path as input, checks how many .json files there are in that
    direcotry, then reconstructs the DOIs associated to each file from their names by 
    removing the file extension, returns a data frame with resulting DOIs and writes
    the content of this data frame into a .csv file.
    """
    
    # Create list with names of all files in input directory
    
    file_names = [file for file in os.listdir(directory) if file.endswith('.json')]
    
    # Create list with names of all files minus ".json" extension  
    # Given the name structure of our files, this will give us a list of all DOIs in folder
    
    paper_dois = [file[:-5].replace('_', '/') for file in file_names]
    
    # Create data frame with names of all files in folder
    
    df_dois = pd.DataFrame(paper_dois, columns=['doi'])
    
    # Write content of log data frame into resulting path
    
    df_dois.to_csv(log_directory, index=False)
    
    # Return data frame
    
    return df_dois

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


#define abstract_getter function

def abstract_getter(input_path):
    
    # Initialize data and log_entries
    data = []
    log_entries = []
    
    # Obtain file names of .json files in input directory
    files = os.listdir(input_path)
    
    # For loop to iterate over all .json files in input directory
    for i, filename in enumerate(files):
    
        # If sentence to make sure we only process .json files
        if filename.endswith('.json'):
        
            # Construct full path for current .json file in loop
            file_path = os.path.join(input_path, filename)
        
            # Try sentence to account for errors reading current .json file
            try:
            
                # Open and read current .json file
                with open(file_path, 'r', encoding='utf-8') as file:
                
                    # Write content of current .json file into content variable
                    content = json.load(file)
                
                    # Extract DOI of article associated to current .json file
                    doi = filename.replace('.json', '')

                    # Get inverted index from content variable 
                    abstract_inverted_index = content.get('abstract_inverted_index', {})
                
                    # If sentence to make sure we only process non-empty word indeces
                    if abstract_inverted_index:
                    
                        # Initialize list of tuples with each word and the position that it occupies in the abstract text
                        index_word_pairs = [(index, word) for word, indices in abstract_inverted_index.items() for index in indices]
                    
                        # Sort list according to the position of each word in the abstract text
                        index_word_pairs.sort()
                    
                        # Reconstruct abstract by adding words in list of tuples in the order of their occurrence in the text
                        # We add a space at the beginning and strip it at the end
                        abstract_text = ' '.join(word for _, word in index_word_pairs).strip()
                   
                        # Create string with delimiter characters to be removed from reconstructed text
                        delimiters = ",;|{}\n\r\t[]<>"
                    
                        # For loop to iterate over all delimiters in delimiter string
                        for delimiter in delimiters:
                        
                            # Replace current delimiter in loop with blank space
                            abstract_text = abstract_text.replace(delimiter, ' ')
                        
                        # Call function to remove non printable characters from reconstructed text 
                        abstract_text = remove_non_printable(abstract_text)
                    
                    # Else sentence to account for situation in which inverted index is empty
                    else:
                        log_entries.append({'filename': filename, 'success': False, 'message': 'No abstract_inverted_index provided'})
                        continue
                    
                    # Initialize author_country string
                    author_country = 'Unknown'  # Default value
                
                    # If clause to check if authorship information is present in content variable
                    if 'authorships' in content:
                    
                        # For loop to iterate over authorsips list
                        for authorship in content['authorships']:
                        
                            # Extract country code from institution of first author for which information is available
                            if 'institutions' in authorship and any(inst.get('country_code') for inst in authorship['institutions']):
                                author_country = next((inst['country_code'] for inst in authorship['institutions'] if 'country_code' in inst), "Unknown")
                                break

                    # Extract publication year from content variable
                    year = content.get('publication_year', 'Unknown')
                
                    # Check for the presence of "retract%" or "withdraw%" in abstract_text
                    retracted_flag = any(word in abstract_text.lower() for word in ["retract", "withdraw", "retracted", "retraction", "withdrew", "withdrawal","withdrawn", "retracts"])

                    # Update data variable with reconstructed text and additional information
                    data.append({
                        'abstract_text': f'"{abstract_text}"',  # Ensure the text is surrounded by double quotes
                        'target': 1,
                        'doi': doi,
                        'country': author_country,
                        'year': year,
                        'ret_flag': retracted_flag
                    })

                    # Update log variable  with success message
                    log_entries.append({'filename': filename, 'success': True, 'message': 'Processed successfully'})
        
        
            # Clause to account for errors in reading the current .json file
            except Exception as e:
            
                # Update log variable with current error message
                log_entries.append({'filename': filename, 'success': False, 'message': f'Error processing file - {str(e)}'})

    return data, log_entries



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