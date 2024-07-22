#########################################################
# Removing questions from a textbook from questions.csv #
#########################################################

import pandas as pd

def remove_text(textbook):
    # Get questions.csv
    data = pd.read_csv('questions.csv')

    # Remove questions that are not from that textbook
    data_filt = data[data.iloc[:, 1] != textbook]
    
    # Save filtered data to csv
    data_filt.to_csv('questions.csv')    