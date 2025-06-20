'''
Flask Application
'''
from flask import Flask, jsonify, request
from flask_cors import CORS

from models import Experience, Education, Skill


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
        return jsonify([exp.__dict__ for exp in data["experience"]])

    if request.method == 'POST':
        exp_data = request.get_json()
        new_id = len(data["experience"]) + 1
        new_exp = Experience(id=new_id, **exp_data)
        data["experience"].append(new_exp)
        return jsonify({"id": new_id}), 201

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify([e.__dict__ for e in data["education"]])

    if request.method == 'POST':
        edu_data = request.get_json()
        new_id = len(data["education"])
        new_edu = Education(id=new_id, **edu_data)
        data["education"].append(new_edu)
        return jsonify({"id": new_id}), 201

@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify([s.__dict__ for s in data["skill"]])

    if request.method == 'POST':
        skill_data = request.get_json()
        new_id = len(data["skill"])
        new_skill = Skill(id=new_id, **skill_data)
        data["skill"].append(new_skill)
        return jsonify({"id": new_id}), 201

@app.route('/resume/education/<int:education_id>', methods=['GET'])
def get_education_by_id(education_id):
    '''
    Returns one education object by its ID
    '''
    for edu in data["education"]:
        if edu.id == education_id:
            return jsonify(edu.__dict__), 200

    return jsonify({"error": "Education not found"}), 404
