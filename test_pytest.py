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


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience


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
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == example_education


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

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill

def test_get_all_education():
    '''
    Checks if all education entries can test GET.
    '''
    client = app.test_client()
    response = client.get('/resume/education')

    assert response.status_code == 200
    education_list = response.get_json()
    assert isinstance(education_list, list)

    if education_list:
        assert "course" in education_list[0]
        assert "school" in education_list[0]

def test_get_all_experience():
    '''
    Checks if all experience entries can test using GET.
    '''
    client = app.test_client()
    response = client.get('/resume/experience')

    assert response.status_code == 200
    experience_list = response.get_json()
    assert isinstance(experience_list, list)

    if experience_list:
        assert "title" in experience_list[0]
        assert "company" in experience_list[0]

def test_get_all_skills():
    '''
    Checks if all skill entries can test GET.
    '''
    client = app.test_client()
    response = client.get('/resume/skill')

    assert response.status_code == 200
    skill_list = response.get_json()
    assert isinstance(skill_list, list)

    if skill_list:
        assert "name" in skill_list[0]
        assert "proficiency" in skill_list[0]

def test_get_education_by_id():
    '''
    Adds a new education entry (POST)
    Gets that entry by its ID
    Checks if the returned data matches the original input
    '''
    client = app.test_client()

    new_education = {
        "course": "Data Science",
        "school": "CUNY SPS",
        "start_date": "2025",
        "end_date": "2026",
        "grade": "90%",
        "logo": "cuny-logo.jpeg"
    }

    post_response = client.post('/resume/education', json=new_education)
    new_id = post_response.get_json()["id"]

    get_response = client.get(f'/resume/education/{new_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()["course"] == "Data Science"

def test_get_experience_by_id():
    '''
    Adds a new experience entry (POST)
    Gets that entry by its ID
    Checks if the returned data matches the original input
    '''
    client = app.test_client()

    new_experience = {
        "title": "Backend Developer",
        "company": "MLH",
        "start_date": "2025",
        "end_date": "Present",
        "description": "Working on APIs",
        "logo": "mlh-logo.png"
    }

    post_response = client.post('/resume/experience', json=new_experience)
    new_id = post_response.get_json()["id"]

    get_response = client.get(f'/resume/experience/{new_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()["title"] == "Backend Developer"

def test_get_skill_by_id():
    '''
    Adds a new skill entry (POST)
    Gets that entry by its ID
    Checks if the returned data matches the original input
    '''
    client = app.test_client()

    new_skill = {
        "name": "Python",
        "proficiency": "2-4 years",
        "logo": "python-logo.png"
    }

    post_response = client.post('/resume/skill', json=new_skill)
    new_id = post_response.get_json()["id"]

    get_response = client.get(f'/resume/skill/{new_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()["name"] == "Python"

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
