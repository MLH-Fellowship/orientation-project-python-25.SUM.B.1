'''
Flask Application
'''
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Experience, Education, Skill, Contact

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


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
    ],
    "contact": None
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

@app.route('/contact', methods=['GET', 'POST', 'PUT'])
def contact():
    '''Handles GET, POST, and PUT for contact information.'''
    response_data = {}
    status_code = 200

    if request.method == 'GET':
        if data["contact"]:
            response_data = {
                "name": data["contact"].name,
                "email": data["contact"].email,
                "phone": data["contact"].phone,
                "linkedin": data["contact"].linkedin,
                "github": data["contact"].github
            }
        else:
            response_data = {"message": "No contact information found"}
            status_code = 404

    elif request.method in ['POST', 'PUT']:
        try:
            contact_data = request.get_json()
            required_fields = ['name', 'email', 'phone', 'linkedin', 'github']
            missing_fields = [field for field in required_fields if field not in contact_data]
            if missing_fields:
                response_data = {"error": f"Missing required fields: {', '.join(missing_fields)}"}
                status_code = 400
            else:
                new_contact = Contact(
                    name=contact_data['name'],
                    email=contact_data['email'],
                    phone=contact_data['phone'],
                    linkedin=contact_data['linkedin'],
                    github=contact_data['github']
                )
                if not new_contact.validate_email():
                    response_data = {"error": "Invalid email format"}
                    status_code = 400
                elif not new_contact.validate_phone():
                    response_data = {"error": "Invalid phone format. (e.g., +1234567890)"}
                    status_code = 400
                else:
                    data["contact"] = new_contact
                    response_data = {
                        "name": new_contact.name,
                        "email": new_contact.email,
                        "phone": new_contact.phone,
                        "linkedin": new_contact.linkedin,
                        "github": new_contact.github
                    }
                    status_code = 200 if request.method == 'PUT' else 201
        except (KeyError, ValueError) as e:
            response_data = {"error": f"Data validation error: {str(e)}"}
            status_code = 400
        except (TypeError, AttributeError) as e:
            response_data = {"error": f"Data processing error: {str(e)}"}
            status_code = 400

    else:
        response_data = {"error": "Method not allowed"}
        status_code = 405

    return jsonify(response_data), status_code

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
