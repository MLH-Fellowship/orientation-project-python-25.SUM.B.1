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
