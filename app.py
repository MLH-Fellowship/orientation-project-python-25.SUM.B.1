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
    Test endpoint to verify API is running.
    
    Returns:
        flask.Response: JSON response containing a test message with status 200
        
    Example:
        GET http://127.0.0.1:5000/test
        Response: {"message": "Hello, World!"}
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience/<int:idx>', methods=['GET'])
def get_experience_by_id(idx):
    """
    Retrieve a specific experience entry by its ID.
    
    Args:
        idx (int): The index/ID of the experience entry to retrieve
        
    Returns:
        flask.Response: JSON response containing the experience data if found,
                       or error message with status 404 if not found
                       
    Example:
        GET http://127.0.0.1:5000/resume/experience/0
        Success Response (200): {"company":"A Cool Company","description":"Writing Python Code","end_date":"Present","id":0,"logo":"example-logo.png","start_date":"October 2022","title":"Software Developer"}
    """
    if 0 <= idx < len(data["experience"]):
        return jsonify(data["experience"][idx])
    return jsonify({"error": "Experience not found"}), 404


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle GET and POST requests for experience entries.
    
    GET: Returns all experience entries as a list (excluding ID fields)
    POST: Creates a new experience entry from JSON data
    
    Returns:
        flask.Response: 
            - GET: JSON array of experience objects (without ID)
            - POST: JSON object with new entry ID and status 201
            - Error: JSON error message with appropriate status code
            
    Request Body (POST):
        JSON object containing:
            - title (str): Job title
            - company (str): Company name
            - start_date (str): Start date
            - end_date (str): End date
            - description (str): Job description
            - logo (str): Logo filename
            
    Example:
        GET /resume/experience
        Response: [array of experience objects]
        
        POST /resume/experience
        Request: {experience data}
        Response: {"id": 1}
    '''
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
    '''
    Handle GET and POST requests for education entries.
    
    GET: Returns all education entries as a list (excluding ID fields)
    POST: Creates a new education entry from JSON data
    
    Returns:
        flask.Response:
            - GET: JSON array of education objects (without ID)
            - POST: JSON object with new entry ID and status 201
            - Error: JSON error message with appropriate status code
            
    Request Body (POST):
        JSON object containing:
            - course (str): Course/degree name
            - school (str): School/university name
            - start_date (str): Start date
            - end_date (str): End date
            - grade (str): Grade/percentage achieved
            - logo (str): Logo filename
            
    Example:
        GET /resume/education
        Response: [array of education objects]
        
        POST /resume/education
        Request: {education data}
        Response: {"id": 1}
    '''
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
    '''
    Handle GET and POST requests for skill entries.
    
    GET: Returns all skill entries as a list (excluding ID fields)
    POST: Creates a new skill entry from JSON data
    
    Returns:
        flask.Response:
            - GET: JSON array of skill objects (without ID)
            - POST: JSON object with new entry ID and status 201
            - Error: JSON error message with appropriate status code
            
    Request Body (POST):
        JSON object containing:
            - name (str): Skill name
            - proficiency (str): Proficiency level
            - logo (str): Logo filename
            
    Example:
        GET /resume/skill
        Response: [array of skill objects]
        
        POST /resume/skill
        Request: {skill data}
        Response: {"id": 1}
    '''
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
    '''
    Retrieve a specific education entry by its ID.
    
    Args:
        education_id (int): The ID of the education entry to retrieve
        
    Returns:
        flask.Response: JSON response containing the education data if found,
                       or error message with status 404 if not found
    '''
    for edu in data["education"]:
        if edu.id == education_id:
            return jsonify(edu.__dict__), 200

    return jsonify({"error": "Education not found"}), 404


@app.route('/resume/skill/<int:skill_id>', methods=['PUT'])
def edit_skill(skill_id):
    """
    Update an existing skill by its ID with provided JSON data.
    
    Args:
        skill_id (int): The ID of the skill to update
        
    Returns:
        flask.Response: JSON response containing updated skill data if found,
                       or error message with status 404 if not found
                       
    Request Body:
        JSON object containing skill fields to update:
            - name (str, optional): Skill name
            - proficiency (str, optional): Proficiency level
            - logo (str, optional): Logo filename
    """
    if 0 <= skill_id < len(data["skill"]):
        skill_data = request.json
        new_skill = data["skill"][skill_id]
        new_skill.name = skill_data.get('name', new_skill.name)
        new_skill.proficiency = skill_data.get('proficiency', new_skill.proficiency)
        new_skill.logo = skill_data.get('logo', new_skill.logo)
        return jsonify(new_skill.__dict__), 200

    return jsonify({"error": "Skill not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
