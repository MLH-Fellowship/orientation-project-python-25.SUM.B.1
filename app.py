'''
Flask Application

A REST API for managing resume data including experience, education, and skills.
Provides endpoints for CRUD operations on resume components.
'''
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Experience, Education, Skill, Contact

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
    ],
    "contact": None
}

@app.route('/test')
def hello_world():
    '''
    Test endpoint to verify API is running.
    
    Returns:
        flask.Response: JSON response containing a test message with status 200
        
    Example:
        GET /test
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
        GET /resume/experience/0
        Success Response (200): {experience object}
        Error Response (404): {"error": "Experience not found"}
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
            - proficiency (str): Proficiency level/years of experience
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
                       
    Example:
        GET /resume/education/0
        Success Response (200): {education object with ID}
        Error Response (404): {"error": "Education not found"}
    '''
    for edu in data["education"]:
        if edu.id == education_id:
            return jsonify(edu.__dict__), 200

    return jsonify({"error": "Education not found"}), 404

@app.route('/resume/skill/<int:skill_id>', methods=['GET'])
def get_skill_by_id(skill_id):
    '''Returns one skill entry by ID.'''
    for s in data["skill"]:
        if s.id == skill_id:
            return jsonify(s.__dict__), 200

    return jsonify({"error": "Skill not found"}), 404

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

@app.route('/resume/education/<int:edu_id>', methods=['PUT'])
def edit_education(edu_id):
    '''Updates an existing education by its ID (index) with provided JSON data.'''
    if 0 <= edu_id < len(data["education"]):
        edu_data = request.json
        edu = data["education"][edu_id]
        edu.course = edu_data.get('course', edu.course)
        edu.school = edu_data.get('school', edu.school)
        edu.start_date = edu_data.get('start_date', edu.start_date)
        edu.end_date = edu_data.get('end_date', edu.end_date)
        edu.grade = edu_data.get('grade', edu.grade)
        edu.logo = edu_data.get('logo', edu.logo)
        return jsonify(edu.__dict__), 200
    return jsonify({"error": "Education not found"}), 404

#Update Exisitng Skill by Index
@app.route('/resume/skill/<int:skill_id>', methods=['PUT'])
def edit_skill(skill_id):
    """
    Update an existing skill entry by its ID.
    
    Args:
        skill_id (int): The ID of the skill to update
        
    Returns:
        flask.Response: JSON response containing the updated skill data if found,
                       or error message with status 404 if not found
                       
    Request Body:
        JSON object containing any of:
            - name (str, optional): New skill name
            - proficiency (str, optional): New proficiency level
            - logo (str, optional): New logo filename
            
    Example:
        PUT /resume/skill/0
        Request: {"name": "JavaScript", "proficiency": "3 years"}
        Success Response (200): {updated skill object}
        Error Response (404): {"error": "Skill not found"}
    """
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
    """Deletes an existing skill by its ID (index)."""
    if 0 <= skill_id < len(data["skill"]):
        deleted_skill = data["skill"].pop(skill_id)
        return jsonify(deleted_skill.__dict__), 200

    return jsonify({"error": "Skill not found"}), 404


@app.route('/resume/experience/<int:exp_id>', methods=['DELETE'])
def delete_experience(exp_id):
    '''Deletes an experience by its index (ID).'''
    if 0 <= exp_id < len(data["experience"]):
        del data["experience"][exp_id]
        return jsonify({"message": f"Experience with id {exp_id} deleted."}), 200
    return jsonify({"error": "Experience not found"}), 404


@app.route('/resume/experience/<int:exp_id>', methods=['PUT'])
def edit_experience(exp_id):
    '''Updates an existing experience by its ID (index) with provided JSON data.'''
    if 0 <= exp_id < len(data["experience"]):
        exp_data = request.json
        exp = data["experience"][exp_id]
        exp.title = exp_data.get('title', exp.title)
        exp.company = exp_data.get('company', exp.company)
        exp.start_date = exp_data.get('start_date', exp.start_date)
        exp.end_date = exp_data.get('end_date', exp.end_date)
        exp.description = exp_data.get('description', exp.description)
        exp.logo = exp_data.get('logo', exp.logo)
        return jsonify(exp.__dict__), 200

    return jsonify({"error": "Experience not found"}), 404

# Delete Existing Education by Index
@app.route('/resume/education/<int:edu_id>', methods=['DELETE'])
def delete_education(edu_id):
    '''Deletes an education by its index (ID).'''
    if 0 <= edu_id < len(data["education"]):
        del data["education"][edu_id]
        return jsonify({"message": f"Education with id {edu_id} deleted."}), 200
    return jsonify({"error": "Education not found"}), 404
