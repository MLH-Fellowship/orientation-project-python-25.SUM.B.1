'''
Flask Application
'''
from flask_cors import CORS
from models import Experience, Education, Skill
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)


data = {
    "experience": [
        Experience(
            id=1,
            title="Software Developer",
            company="A Cool Company",
            start_date="October 2022",
            end_date="Present",
            description="Writing Python Code",
            logo="example-logo.png")
    ],
    "education": [
        Education(
            id=1,
            course="Computer Science",
            school="University of Tech",
            start_date="September 2019",
            end_date="July 2022",
            grade="80%",
            logo="example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify()

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/education/<int:education_id>', methods=['GET'])
def get_education_by_id(education_id):
    '''
    Returns one education object by its ID
    '''
    for edu in data["education"]:
        if edu.id == education_id:
            return jsonify(edu.__dict__), 200

    return jsonify({"error": "Education not found"}), 404