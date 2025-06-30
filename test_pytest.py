'''
Tests in Pytest
'''
from app import app
from models import Contact


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

def test_contact_creation():
    '''Test creating a contact with valid data'''
    contact = Contact(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe"
    )
    assert contact.name == "John Doe"
    assert contact.email == "john.doe@example.com"
    assert contact.phone == "+1234567890"
    assert contact.linkedin == "https://linkedin.com/in/johndoe"
    assert contact.github == "https://github.com/johndoe"


def test_validate_email_valid():
    '''Test email validation with valid email'''
    contact = Contact(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe"
    )
    assert contact.validate_email() is True


def test_validate_email_invalid():
    '''Test email validation with invalid email'''
    contact = Contact(
        name="John Doe",
        email="invalid-email",
        phone="+1234567890",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe"
    )
    assert contact.validate_email() is False


def test_validate_phone_valid():
    '''Test phone validation with valid international format'''
    contact = Contact(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe"
    )
    assert contact.validate_phone() is True


def test_validate_phone_invalid():
    '''Test phone validation with invalid format'''
    contact = Contact(
        name="John Doe",
        email="john.doe@example.com",
        phone="1234567890",  # Missing + sign
        linkedin="https://linkedin.com/in/johndoe",
        github="https://github.com/johndoe"
    )
    assert contact.validate_phone() is False


def test_contact_post_and_get():
    '''Test POST and GET for /contact endpoint'''
    example_contact = {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone": "+19876543210",
        "linkedin": "https://linkedin.com/in/janesmith",
        "github": "https://github.com/janesmith"
    }
    # POST the contact
    post_response = app.test_client().post('/contact', json=example_contact)
    assert post_response.status_code == 201
    assert post_response.json == example_contact

    # GET the contact
    get_response = app.test_client().get('/contact')
    assert get_response.status_code == 200
    assert get_response.json == example_contact


def test_update_skill():
    """Tests the PUT /resume/skill/<id> endpoint for updating a skill."""
    client = app.test_client()

    # First create a new skill
    new_skill = {
        "name": "Python",
        "proficiency": "2 years",
        "logo": "example-logo.png"
    }

    # Post the skill to create it
    post_response = client.post('/resume/skill', json=new_skill)
    new_id = post_response.get_json()["id"]

    # Update the skill
    updated_skill = {
        "name": "Python",
        "proficiency": "5 years",  # Changed proficiency
        "logo": "example-logo.png"
    }

    # Put the updated skill
    put_response = client.put(f'/resume/skill/{new_id}', json=updated_skill)
    assert put_response.status_code == 200

    # Get the skill to verify it was updated
    get_response = client.get(f'/resume/skill/{new_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()["proficiency"] == "5 years"



def test_delete_skill():
    """Tests the DELETE /resume/skill/<skill_id> endpoint."""
    new_skill = {
        "name": "C++",
        "proficiency": "4 years",
        "logo": "example-logo.png"
    }

    skill_id = app.test_client().post('/resume/skill', json=new_skill).json['id']

    response = app.test_client().delete(f'/resume/skill/{skill_id}')
    assert response.status_code == 200
    assert response.json['name'] == new_skill['name']

    get_response = app.test_client().get('/resume/skill')
    assert skill_id not in get_response.json

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

def test_delete_education():
    '''Test deleting an education by ID'''
    # Add a new education to ensure there is one to delete
    example_education = {
        "course": "Test Course",
        "school": "Test School",
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "grade": "100%",
        "logo": "example-logo.png"
    }
    post_response = app.test_client().post('/resume/education', json=example_education)
    edu_id = post_response.json['id']

    # Delete the education
    delete_response = app.test_client().delete(f'/resume/education/{edu_id}')
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == f"Education with id {edu_id} deleted."

    # Try to get all educations and ensure the deleted one is not present
    get_response = app.test_client().get('/resume/education')
    educations = get_response.json
    assert all(education['id'] != edu_id for education in educations)
