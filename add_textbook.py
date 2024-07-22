###################################################
# Adding questions from textbook to questions.tsv #
###################################################

import pdfplumber
import csv

# Convert pdf into a list of lines and their associated bounding box
def text_bbox_extractor(path):
    # Extract list of dictionaries for each word
    words = []
    with pdfplumber.open(path) as pdf:
        for page_num, page in enumerate(pdf.pages):
                words += [{**d, 'page_num': page_num} for d in page.extract_words()]
    
    # Group dictionaries by those in the same line
    grouped_dicts = {}
    for d in words:
        value = d['top']
        if value not in grouped_dicts:
            grouped_dicts[value] = []
        grouped_dicts[value].append(d)
        
    grouped_lists = list(grouped_dicts.values())
    
    # Extract the text and associated bounding box for each line
    lines = []
    bboxs = []
    for line in grouped_lists:
        line_string = ' '.join([d['text'] for d in line])
        lines.append(line_string)
        
        x0 = min([d['x0'] for d in line])
        top = line[0]['top']
        x1 = max([d['x1'] for d in line])
        bottom = max([d['bottom'] for d in line])
        page_num = line[0]['page_num']
        bboxs.append((x0, top, x1, bottom, page_num))
    
    return lines, bboxs

# Get the index of lines which associate with questions
def get_question_indices(list_of_lines, THRESHOLD):
    # Get list of lines from text
    #list_of_lines = text.split('\n')
    # Filter to lines which start with a number
    index_of_potentials = [list_of_lines.index(line) for line in list_of_lines if line.split('.')[0].isnumeric() and len(line.split('.'))>1]
    list_of_potentials = [list_of_lines[i].split('.')[0] for i in index_of_potentials]    
    
    # Get index of lines which start with a one
    index_of_ones = [index for index in range(len(list_of_potentials)) if list_of_potentials[index] == '1']
    
    # Get index of lines for which there are at least THRESHOLD consecutive questions
    OnetoThreshold = list(map(str, range(1, THRESHOLD + 1)))
    index_valid_q1 = [index for index in index_of_ones if list_of_potentials[index: index + THRESHOLD] == OnetoThreshold]
    
    # Get a list of lists of the indices from list_of_lines which correspond to a valid question
    set_of_questions = []
    for q1 in index_valid_q1:
        if q1 != index_valid_q1[-1]:
            next_one = index_of_ones[index_of_ones.index(q1) + 1]
        else:
            next_one = index_of_potentials[-1]
        question_set = index_of_potentials[q1: next_one]
        set_of_questions.append(question_set)        
    
    return set_of_questions, list_of_lines

# Get the list of questions
def get_questions_bbox(set_of_questions, list_of_lines, bounding_box_list):
    questions = []
    bboxs = []
    # Loop over each set of problems
    for problemset in set_of_questions:
        # Loop over each questioin in the problem set
        for q_index in range(len(problemset)-3):
            # Add the text of questions to the ongoing list of questions
            question_list = list_of_lines[problemset[q_index]: problemset[q_index+1]]
            bbox_list = bounding_box_list[problemset[q_index]: problemset[q_index+1]]
            if len(question_list) < 25 and problemset[q_index] < problemset[q_index+1]:
                question = '\n'.join(question_list)
                questions.append(question)
                
                x0 = min( list(zip(*bbox_list))[0])
                top = min( list(zip(*bbox_list))[1])
                x1 = max( list(zip(*bbox_list))[2])
                bottom = max( list(zip(*bbox_list))[3])
                page_nums = list(zip(*bbox_list))[4]
                
                if len(set(page_nums)) == 1:
                    bboxs.append((x0, top, x1, bottom, page_nums[0]))
                else:
                    bboxs.append(('a', 'a', 'a', 'a', 'a'))              
    return questions, bboxs

# Overall function which generates list of questions from pdf
def questions_from_pdf(path, THRESHOLD):
    text, bboxs_total = text_bbox_extractor(path)
    question_set, lines_set = get_question_indices(text, THRESHOLD)
    
    questions, bboxs = get_questions_bbox(question_set, lines_set, bboxs_total)
    
    return questions, bboxs
        
# Update the questions.csv with new questions from the textbook at path
def update_questions(questions, bboxs, path):
    # Isolate textbook name (filename)
    name = path.split("\\")[-1]
    
    # Create data to be entered into questions.csv
    data = []
    for i in range(len(questions)):
        data.append((questions[i], name, bboxs[i]))
    
    with open ('questions.csv', "w", newline="") as csvfile:
        q_csv = csv.writer(csvfile)
        for x in data:
            q_csv.writerow(x)
            
#if __name__ == '__main__':
#    # Prompt user to provide textbook path
#    path = input("Enter the path to the textbook:")
#    # Set threshold
#    THRESHOLD = 10
#    
#    # Get questions from textbook
#    questions, bboxs = questions_from_pdf(path, THRESHOLD)
#    # Add questions to csv (assuming add_textbook.py is being run in same directory as questions.csv
#    update_questions(questions, bboxs, path)
