'''
Tests in Pytest - FIXED VERSION
'''
from app import app


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences.

    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Frontend",
        "company": "Twitter",
        "start_date": "June 2025",
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
    '''
    Test getting all experiences as a list
    '''
    # GET all experiences
    response = app.test_client().get('/resume/experience')
    assert response.status_code == 200
    
    # Should return a list
    assert isinstance(response.json, list)
    
    # Should have at least the default experience
    assert len(response.json) >= 1


def test_education():
    '''
    Add a new education and then get all educations.

    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    
    # POST to add new education
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    # GET all education entries
    response = app.test_client().get('/resume/education')
    assert response.status_code == 200
    
    # Check that our new education is in the list (without ID)
    assert example_education in response.json


def test_skill():
    '''
    Add a new skill and then get all skills.

    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    # POST to add new skill
    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    # GET all skills
    response = app.test_client().get('/resume/skill')
    assert response.status_code == 200
    
    # Check that our new skill is in the list (without ID)
    assert example_skill in response.json


def test_update_skill():
    """Tests the PUT /resume/skill/<id> endpoint for updating a skill."""
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
