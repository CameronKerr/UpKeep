########################
# Flask app for upkeep #
########################

from flask import Flask, render_template, redirect, request, url_for, jsonify
from upkeep import *
from add_textbook import *
from remove_textbook import *
import os
import atexit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upkeep.html')

@app.route('/run-script')
def run_script():
    if os.path.exists("static/question.png"):
        os.remove("static/question.png")    
    main()
    #return jsonify({"image_url": url_for('static', filename='question.png')})
    return jsonify({"image_url": url_for('static', filename='question.png', _external=True) + f"?t={os.path.getmtime('static/question.png')}"})

@app.route('/run-script-string', methods=['GET'])
def run_script_string():
    filename = request.args.get('input')
    path = 'textbooks/' + filename
    THRESHOLD = 10
    # Get questions from textbook
    questions, bboxs = questions_from_pdf(path, THRESHOLD)
    # Add questions to csv (assuming add_textbook.py is being run in same directory as questions.csv
    update_questions(questions, bboxs, path)
    return 'Done'

@app.route('/run-script-remove', methods=['GET'])
def run_script_remove():
    filename = request.args.get('input')
    path = 'textbooks/' + filename
    remove_text(path)
    return 'Done'

def cleanup():
    if os.path.exists("static/question.png"):
        os.remove("static/question.png")
        
atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug = True)