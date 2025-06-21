'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
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


@app.route('/resume/experience/<int:idx>', methods=['GET'])
def get_experience_by_id(idx):
    if 0 <= idx < len(data["experience"]):
        return jsonify(data["experience"][idx].serialize())
    return jsonify({"error": "Experience not found"}), 404
@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    if request.method == 'GET':
        return jsonify([exp.serialize() for exp in data['experience']])

    if request.method == 'POST':
        new_data = request.get_json()
        new_exp = Experience(
            new_data["role"],
            new_data["company"],
            new_data["start"],
            new_data["end"],
            new_data["description"],
            new_data["logo"]
        )
        data["experience"].append(new_exp)
        index = len(data["experience"]) - 1
        return jsonify({"index": index}), 201

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
