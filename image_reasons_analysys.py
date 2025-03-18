# Input path to data set

input_path = "Documents/1_original_data_set.csv"

# Load data frame with data set

df = pd.read_csv(input_path, encoding='latin-1')

# Define function to unpack all reasons in "Reason" column 
# (Several reasons separated by ; sign are sometimes given per paper in the original data set)


def column_unpacker(df, column):

    # Create series with all entries in column by splitting and exploding entries in subject column
    entries_series = df[column].str.split(';').explode()

    # Obtain list with unique entries from series
    unique_entries_list = sorted(entries_series.unique())

    # Obtain series with value counts of unique entries
    unique_entries_value_counts = entries_series.value_counts()

    # Return both series
    return entries_series, unique_entries_list, unique_entries_value_counts


# Call function to obtain list of unique reasons mentioned in column "Reason"

reason_series, unique_reason_list, reason_counts = column_unpacker(df, "Reason")

# Obtained filtered list with reasons that include the word "Image" only

filtered_list = [item for item in unique_reason_list if "Image" in item]

# Display result

filtered_list