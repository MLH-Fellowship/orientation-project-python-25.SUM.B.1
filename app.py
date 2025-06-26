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
            id=0,
            title="Software Developer",
            company="A Cool Company",
            start_date="October 2022",
            end_date="Present",
            description="Writing Python Code",
            logo="example-logo.png"
        )
    ],
    "education": [
        Education(
            id=0,
            course="Computer Science",
            school="University of Tech",
            start_date="September 2019",
            end_date="July 2022",
            grade="80%",
            logo="example-logo.png"
        )
    ],
    "skill": [
        Skill(
            id=0,
            name="Python",
            proficiency="1-2 Years",
            logo="example-logo.png"
        )
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
    '''Handles GET and POST for experience.'''
    if request.method == 'GET':
        return jsonify([
            {k: v for k, v in exp.__dict__.items() if k != "id"}
            for exp in data["experience"]
        ])

    if request.method == 'POST':
        exp_data = request.get_json()
        new_id = len(data["experience"])
        new_exp = Experience(id=new_id, **exp_data)
        data["experience"].append(new_exp)
        return jsonify({"id": new_id}), 201

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''Handles GET and POST for education.'''
    if request.method == 'GET':
        return jsonify([
            {k: v for k, v in edu.__dict__.items() if k != "id"}
            for edu in data["education"]
        ])

    if request.method == 'POST':
        edu_data = request.get_json()
        new_id = len(data["education"])
        new_edu = Education(id=new_id, **edu_data)
        data["education"].append(new_edu)
        return jsonify({"id": new_id}), 201

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''Handles GET and POST for skill.'''
    if request.method == 'GET':
        return jsonify([
            {k: v for k, v in s.__dict__.items() if k != "id"}
            for s in data["skill"]
        ])

    if request.method == 'POST':
        skill_data = request.get_json()
        new_id = len(data["skill"])
        new_skill = Skill(id=new_id, **skill_data)
        data["skill"].append(new_skill)
        return jsonify({"id": new_id}), 201

    return jsonify({"error": "Method not allowed"}), 405


@app.route('/resume/education/<int:education_id>', methods=['GET'])
def get_education_by_id(education_id):
    '''Returns one education entry by ID.'''
    for edu in data["education"]:
        if edu.id == education_id:
            return jsonify(edu.__dict__), 200

    return jsonify({"error": "Education not found"}), 404

#Update Exisitng Skill by Index
@app.route('/resume/skill/<int:skill_id>', methods=['PUT'])
def edit_skill(skill_id):
    """Updates an existing skill by its ID (index) with provided JSON data."""
    if 0 <= skill_id < len(data["skill"]):
        skill_data = request.json
        new_skill = data["skill"][skill_id]
        new_skill.name = skill_data.get('name', new_skill.name)
        new_skill.proficiency = skill_data.get('proficiency', new_skill.proficiency)
        new_skill.logo = skill_data.get('logo', new_skill.logo)
        return jsonify(new_skill.__dict__), 200

    return jsonify({"error": "Skill not found"}), 404

#Delete Existing Skill by Index
@app.route('/resume/skill/<int:skill_id>', methods=['DELETE'])

def delete_skill(skill_id):

    if 0 <= skill_id < len(data["skill"]):
        deleted_skill = data["skill"].pop(skill_id)
        return jsonify(deleted_skill.__dict__), 200

    return jsonify({"error": "Skill not found"}), 404
