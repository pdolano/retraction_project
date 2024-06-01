import os
import json
import csv

# File path of the directory with .json files

#directory = '/Volumes/Hurricane/CellBiology_AllData'

directory = '../data/json_files/cellbiology_retracted_fulljsonfiles'

# File path for .csv file with results

csv_file_path = '../data/results.csv'

# Initialize the header for the .csv file

headers = ['file_name', 'author_country', 'publication_year', 'abstract_info', 'ngram_info', 'error']

# Open the CSV file in write mode

with open(csv_file_path, mode='w', newline='') as file:
    
    writer = csv.DictWriter(file, fieldnames=headers)
    
    writer.writeheader()  # Write the header

    # Loop through all files in the directory
    
    for filename in os.listdir(directory):
        
        if filename.endswith('.json'):
            
            # Construct the full file path
            
            file_path = os.path.join(directory, filename)
            
            file_name = filename.rsplit('.json', 1)[0]  # Correct filename extraction
            
            # Initialize error message and other variables
            
            error_message = ""
            
            author_country = "N/A"
            
            ngram_info = False

            # Try to open and read the JSON file
            
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    
                    content = json_file.read()
                    
                    if not content:
                        
                        raise ValueError("File is empty")
                        
                    data = json.loads(content)
                    
                    # Extract the country code for the first author with a valid country code
                    
                    if 'authorships' in data:
                        
                        for authorship in data['authorships']:
                            
                            if 'institutions' in authorship and any(inst.get('country_code') for inst in authorship['institutions']):
                                
                                author_country = next((inst['country_code'] for inst in authorship['institutions'] if 'country_code' in inst), "N/A")
                                
                                break
                    
                    # Check for ngrams_url content and validate its format
                    
                    ngrams_url = data.get('ngrams_url', '')
                    
                    if ngrams_url.startswith('https://api.'):
                        
                        ngram_info = True

            except Exception as e:
                
                error_message = str(e)

            # Extract publication year and abstract info
            
            publication_year = data.get('publication_year', 'N/A') if not error_message else 'N/A'
            
            abstract_info = bool(data.get('abstract_inverted_index')) if not error_message else False

            # Write data or error to CSV
            
            writer.writerow({
                'file_name': file_name,
                'author_country': author_country,
                'publication_year': publication_year,
                'abstract_info': abstract_info,
                'ngram_info': ngram_info,
                'error': error_message
            })

# Confirmation message

print("Data processing complete and saved to CSV on Desktop.")
