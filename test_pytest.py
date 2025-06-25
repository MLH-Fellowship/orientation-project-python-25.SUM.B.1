'''
Tests in Pytest
'''
from app import app

def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"

def test_get_specific_experience():
    '''Get the first experience by index and check its structure.'''
    client = app.test_client()

    example_experience = {
        "role": "Software Developer",
        "company": "A Cooler Company",
        "start": "October 2022",
        "end": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    post_response = client.post('/resume/experience', json=example_experience)
    assert post_response.status_code == 201
    item_index = post_response.json['index']

    get_response = client.get(f'/resume/experience/{item_index}')
    assert get_response.status_code == 200
    data = get_response.json

    assert data["role"] == example_experience["role"]
    assert data["company"] == example_experience["company"]
    assert data["start"] == example_experience["start"]
    assert data["end"] == example_experience["end"]
    assert data["description"] == example_experience["description"]
    assert data["logo"] == example_experience["logo"]

    post_response = client.post('/resume/experience', json=example_experience)
    assert post_response.status_code == 201
    item_index = post_response.json['index']

    get_response = client.get('/resume/experience')
    assert get_response.status_code == 200
    experiences = get_response.json

    inserted_exp = experiences[item_index]
    assert inserted_exp["role"] == example_experience["role"]
    assert inserted_exp["company"] == example_experience["company"]
    assert inserted_exp["start"] == example_experience["start"]
    assert inserted_exp["end"] == example_experience["end"]
    assert inserted_exp["description"] == example_experience["description"]
    assert inserted_exp["logo"] == example_experience["logo"]

def test_education():
    '''
    Add a new education and then get all education entries.
    Check that it returns the new education in that list.
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    client = app.test_client()

    # POST the new education
    post_response = client.post('/resume/education', json=example_education)
    assert post_response.status_code == 201
    edu_id = post_response.json['id']

    # GET all education entries
    get_response = client.get('/resume/education')
    assert get_response.status_code == 200
    education_list = get_response.json

    inserted_edu = education_list[edu_id]
    assert inserted_edu["course"] == example_education["course"]
    assert inserted_edu["school"] == example_education["school"]
    assert inserted_edu["start_date"] == example_education["start_date"]
    assert inserted_edu["end_date"] == example_education["end_date"]
    assert inserted_edu["grade"] == example_education["grade"]
    assert inserted_edu["logo"] == example_education["logo"]

def test_skill():
    '''
    Add a new skill and then get all skills.
    Check that it returns the new skill in that list.
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    client = app.test_client()

    # POST the new skill
    post_response = client.post('/resume/skill', json=example_skill)
    assert post_response.status_code == 201
    skill_id = post_response.json['id']

    # GET all skills and confirm the one we added exists at the correct index
    get_response = client.get('/resume/skill')
    assert get_response.status_code == 200
    skills = get_response.json


    inserted_skill = skills[skill_id]
    assert inserted_skill["name"] == example_skill["name"]
    assert inserted_skill["proficiency"] == example_skill["proficiency"]
    assert inserted_skill["logo"] == example_skill["logo"]

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill

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
