import os
import json
import pandas as pd
import csv
import string

# Paths
source_directory = '/Volumes/Hurricane/cellbiology_non-retracted_fulljsonfiles'
output_csv_path = '/Users/jennyluise/Desktop/Spiced_repos/data/cellbio_abstracts/cellbio_abstracts_non-retracted_text.csv'
log_csv_path = '/Users/jennyluise/Desktop/Spiced_repos/data/cellbio_abstracts/cellbio_abstracts_non-retracted_error_log.csv'

# Function to remove non-printable characters
def remove_non_printable(text):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, text))

# Preparing to store data and log entries
data = []
log_entries = []

# Processing files
files = os.listdir(source_directory)
for i, filename in enumerate(files):
    if filename.endswith('.json'):
        file_path = os.path.join(source_directory, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                doi = filename.replace('.json', '')

                # Extract abstract text and clean it
                abstract_inverted_index = content.get('abstract_inverted_index', {})
                if abstract_inverted_index:
                    index_word_pairs = [(index, word) for word, indices in abstract_inverted_index.items() for index in indices]
                    index_word_pairs.sort()
                    abstract_text = ' '.join(word for _, word in index_word_pairs).strip()
                    # Remove extended range of delimiters and special characters, including non-printable characters
                    delimiters = ",;|{}\n\r\t[]<>"
                    for delimiter in delimiters:
                        abstract_text = abstract_text.replace(delimiter, ' ')
                    abstract_text = remove_non_printable(abstract_text)
                else:
                    log_entries.append({'filename': filename, 'success': False, 'message': 'No abstract_inverted_index provided'})
                    continue

                # Extract country from the authorships
                author_country = 'Unknown'  # Default value
                if 'authorships' in content:
                    for authorship in content['authorships']:
                        if 'institutions' in authorship and any(inst.get('country_code') for inst in authorship['institutions']):
                            author_country = next((inst['country_code'] for inst in authorship['institutions'] if 'country_code' in inst), "Unknown")
                            break

                # Extract publication year
                year = content.get('publication_year', 'Unknown')

                # Append data for CSV output
                # Check for the presence of "retract%" or "withdraw%" in abstract_text
                retracted_flag = any(word in abstract_text.lower() for word in ["retract", "withdraw", "retracted", "retraction", "withdrew", "withdrawal", "withdrawn", "retracts"])

                data.append({
                    'abstract_text': f'"{abstract_text}"',  # Ensure the text is surrounded by double quotes
                    'target': 0,
                    'doi': doi,
                    'country': author_country,
                    'year': year,
                    'ret_flag': retracted_flag
                })

                # Log entry for success
                log_entries.append({'filename': filename, 'success': True, 'message': 'Processed successfully'})
                
        except Exception as e:
            log_entries.append({'filename': filename, 'success': False, 'message': f'Error processing file - {str(e)}'})

        # Progress message
        if (i + 1) % 200 == 0:
            print(f'Processed {i + 1} files')

# Save data to CSV with pipe delimiter
df = pd.DataFrame(data)
print(f'Number of rows to be written to CSV: {len(df)}')  # Print the number of rows
df.to_csv(output_csv_path, sep='|', index=False, quoting=csv.QUOTE_MINIMAL)

# Save log entries to CSV
log_df = pd.DataFrame(log_entries)
log_df.to_csv(log_csv_path, index=False, quoting=csv.QUOTE_MINIMAL)

print('Processing complete.')
