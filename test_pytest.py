"""
Tests in Pytest
"""
from app import app


def test_client():
    """
    Test the basic test endpoint to ensure API is running.
    
    Verifies:
        - API responds with status 200
        - Response contains expected test message
        
    Returns:
        None: Asserts pass/fail for test validation
    """
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    """
    Test adding a new experience and retrieving it by ID.
    
    Verifies:
        - POST request creates new experience successfully
        - GET request retrieves the specific experience by ID
        - Response data matches the input data
        
    Returns:
        None: Asserts pass/fail for test validation
    """
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    # POST to add new experience
    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']

    # GET individual experience by ID (fixed URL)
    response = app.test_client().get(f'/resume/experience/{item_id}')
    assert response.status_code == 200

    # The individual GET returns the full object including ID
    returned_experience = response.json

    # Check each field (excluding ID since it's auto-generated)
    for key, value in example_experience.items():
        assert returned_experience[key] == value


def test_experience_list():
    """
    Test retrieving all experiences as a list.
    
    Verifies:
        - GET request returns status 200
        - Response is a list format
        - List contains at least the default experience entry
        
    Returns:
        None: Asserts pass/fail for test validation
    """
    # GET all experiences
    response = app.test_client().get('/resume/experience')
    assert response.status_code == 200

    # Should return a list
    assert isinstance(response.json, list)

    # Should have at least the default experience
    assert len(response.json) >= 1


def test_education():
    """
    Test adding a new education entry and retrieving all education entries.
    
    Verifies:
        - POST request creates new education successfully
        - GET request returns all education entries as a list
        - New education entry appears in the list
        
    Returns:
        None: Asserts pass/fail for test validation
    """
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    # POST to add new education
    app.test_client().post('/resume/education', json=example_education)

    # GET all education entries
    response = app.test_client().get('/resume/education')
    assert response.status_code == 200

    # Check that our new education is in the list (without ID)
    assert example_education in response.json


def test_skill():
    """
    Test adding a new skill and retrieving all skills.
    
    Verifies:
        - POST request creates new skill successfully
        - GET request returns all skills as a list
        - New skill appears in the list
        
    Returns:
        None: Asserts pass/fail for test validation
    """
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    # POST to add new skill
    app.test_client().post('/resume/skill', json=example_skill)

    # GET all skills
    response = app.test_client().get('/resume/skill')
    assert response.status_code == 200

    # Check that our new skill is in the list (without ID)
    assert example_skill in response.json


def test_update_skill():
    """
    Test the PUT endpoint for updating an existing skill.
    
    Verifies:
        - POST request creates a new skill successfully
        - PUT request updates the skill with new data
        - Updated skill contains the new values
        - Response returns status 200
        
    Returns:
        None: Asserts pass/fail for test validation
    """
    new_skill = {
        "name": "Python",
        "proficiency": "2 years",
        "logo": "example-logo.png"
    }

    skill_id = app.test_client().post('/resume/skill', json=new_skill).json['id']

    updated_skill = {
        "name": "C++",
        "proficiency": "3 years",
        "logo": "updated-logo.png"
    }

    response = app.test_client().put(f'/resume/skill/{skill_id}', json=updated_skill)
    assert response.status_code == 200
    assert response.json['name'] == updated_skill['name']
    assert response.json['proficiency'] == updated_skill['proficiency']
    assert response.json['logo'] == updated_skill['logo']