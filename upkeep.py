##########################################
# Get random question from questions.csv #
##########################################

import pdfplumber
import csv
import random
import pandas as pd

# Generate pdf image of question
def pdf_question(pdf_path, bbox):
    # Get bounding box for text
    x0, top, x1, bottom, page_num = bbox
    # Plot bounding box on page
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        page.crop((x0, top, x1, bottom)).to_image(resolution=500).save("static/question.png", format = "PNG")
 
# Get random question from questions.csv       
def get_random_question():
    with open('questions.csv') as f:
        reader = csv.reader(f)
        row_count = sum(1 for _ in reader)
    randomrow = random.randint(1, row_count)
    row = pd.read_csv('questions.csv', skiprows=randomrow, nrows=0)
    if eval(list(row)[2])[0] != 'a':
        pdf_question(list(row)[1], eval(list(row)[2]))
    # Return error if bounding box is all 'a''s (this means that the question spans multiple pages
    else:
        return 1/0

# Since pdf extraction isn't perfect allow for errors in getting a question    
def run_process():
    try:
        get_random_question()
        return True
    except Exception as e:
        return False

def main():
    max_attempts = 5  # Maximum number of attempts to run the process
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        
        result = run_process()
        
        if result:
            break  # Exit the retry loop if successful
        else:
            print("Process failed. Retrying...")
    
    if result is None:
        print("Maximum attempts reached. Process failed.")
    
