'''
Tests in Pytest
'''
from app import app
from models import Contact


def test_client():
    '''
    Test the basic test endpoint to ensure API is running.
    
    Verifies:
        - API responds with status 200
        - Response contains expected test message
        
    Returns:
        None: Asserts pass/fail for test validation
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Test adding a new experience and retrieving it by ID.
    
    Verifies:
        - POST request creates new experience successfully
        - GET request retrieves the specific experience by ID
        - Response data matches the input data
        
    Returns:
        None: Asserts pass/fail for test validation
    '''
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
    '''
    Test retrieving all experiences as a list.
    
    Verifies:
        - GET request returns status 200
        - Response is a list format
        - List contains at least the default experience entry
        
    Returns:
        None: Asserts pass/fail for test validation
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
    Test adding a new education entry and retrieving all education entries.
    
    Verifies:
        - POST request creates new education successfully
        - GET request returns all education entries as a list
        - New education entry appears in the list
        
    Returns:
        None: Asserts pass/fail for test validation
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
    app.test_client().post('/resume/education',
                           json=example_education)

    # GET all education entries
    response = app.test_client().get('/resume/education')
    assert response.status_code == 200

    # Check that our new education is in the list (without ID)
    assert example_education in response.json


def test_skill():
    '''
    Test adding a new skill and retrieving all skills.
    
    Verifies:
        - POST request creates new skill successfully
        - GET request returns all skills as a list
        - New skill appears in the list
        
    Returns:
        None: Asserts pass/fail for test validation
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    # POST to add new skill
    app.test_client().post('/resume/skill',
                           json=example_skill)

    # GET all skills
    response = app.test_client().get('/resume/skill')
    assert response.status_code == 200

    # Check that our new skill is in the list (without ID)
    assert example_skill in response.json


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

    # Verify the skill was deleted by checking it's not in the list
    get_response = app.test_client().get('/resume/skill')
    skill_ids = [skill.get('id') for skill in get_response.json if isinstance(skill, dict)]
    assert skill_id not in skill_ids


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


def test_edit_experience():
    '''Test updating an experience by ID'''
    # Add a new experience to ensure there is one to update
    example_experience = {
        "title": "Test Developer",
        "company": "Test Company",
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "description": "Testing update endpoint",
        "logo": "example-logo.png"
    }
    post_response = app.test_client().post('/resume/experience', json=example_experience)
    exp_id = post_response.json['id']

    # Update the experience
    updated_experience = {
        "title": "Updated Developer",
        "company": "Updated Company",
        "start_date": "Feb 2025",
        "end_date": "Nov 2025",
        "description": "Updated description",
        "logo": "updated-logo.png"
    }
    put_response = app.test_client().put(f'/resume/experience/{exp_id}', json=updated_experience)
    assert put_response.status_code == 200
    expected_experience = updated_experience.copy()
    expected_experience["id"] = exp_id
    assert put_response.json == expected_experience

    # Get all experiences and ensure the updated one is present
    get_response = app.test_client().get('/resume/experience')
    experiences = get_response.json
    expected_experience_no_id = expected_experience.copy()
    expected_experience_no_id.pop("id")
    assert expected_experience_no_id in experiences


def test_edit_education():
    '''Test updating an education by ID'''
    # Add a new education to ensure there is one to update
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

    # Update the education
    updated_education = {
        "course": "Updated Course",
        "school": "Updated School",
        "start_date": "Feb 2025",
        "end_date": "Nov 2025",
        "grade": "99%",
        "logo": "updated-logo.png"
    }
    put_response = app.test_client().put(f'/resume/education/{edu_id}', json=updated_education)
    assert put_response.status_code == 200
    expected_education = updated_education.copy()
    expected_education["id"] = edu_id
    assert put_response.json == expected_education

    # Get all educations and ensure the updated one is present
    get_response = app.test_client().get('/resume/education')
    educations = get_response.json
    expected_education_no_id = expected_education.copy()
    expected_education_no_id.pop("id")
    assert expected_education_no_id in educations

    # Add these test functions to the end of your test_pytest.py file

def test_experience_validation_missing_fields():
    '''Test that POST /resume/experience returns 400 for missing required fields'''
    # Test with completely empty data
    response = app.test_client().post('/resume/experience', json={})
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']
    
    # Test with some missing fields
    incomplete_experience = {
        "title": "Software Developer",
        "company": "Test Company"
        # Missing: start_date, end_date, description, logo
    }
    response = app.test_client().post('/resume/experience', json=incomplete_experience)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']
    
    # Test with empty string values (should also fail)
    empty_experience = {
        "title": "",
        "company": "Test Company",
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "description": "Test description",
        "logo": "test-logo.png"
    }
    response = app.test_client().post('/resume/experience', json=empty_experience)
    assert response.status_code == 400
    assert 'error' in response.json


def test_education_validation_missing_fields():
    '''Test that POST /resume/education returns 400 for missing required fields'''
    # Test with completely empty data
    response = app.test_client().post('/resume/education', json={})
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']
    
    # Test with some missing fields
    incomplete_education = {
        "course": "Computer Science",
        "school": "Test University"
        # Missing: start_date, end_date, grade, logo
    }
    response = app.test_client().post('/resume/education', json=incomplete_education)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']
    
    # Test with empty string values (should also fail)
    empty_education = {
        "course": "Computer Science",
        "school": "",
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "grade": "A",
        "logo": "test-logo.png"
    }
    response = app.test_client().post('/resume/education', json=empty_education)
    assert response.status_code == 400
    assert 'error' in response.json


def test_skill_validation_missing_fields():
    '''Test that POST /resume/skill returns 400 for missing required fields'''
    # Test with completely empty data
    response = app.test_client().post('/resume/skill', json={})
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']
    
    # Test with some missing fields
    incomplete_skill = {
        "name": "Python"
        # Missing: proficiency, logo
    }
    response = app.test_client().post('/resume/skill', json=incomplete_skill)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']
    
    # Test with empty string values (should also fail)
    empty_skill = {
        "name": "Python",
        "proficiency": "",
        "logo": "python-logo.png"
    }
    response = app.test_client().post('/resume/skill', json=empty_skill)
    assert response.status_code == 400
    assert 'error' in response.json


def test_contact_validation_missing_fields():
    '''Test that POST /contact returns 400 for missing required fields'''
    # Test with completely empty data
    response = app.test_client().post('/contact', json={})
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']
    
    # Test with some missing fields
    incomplete_contact = {
        "name": "John Doe",
        "email": "john@example.com"
        # Missing: phone, linkedin, github
    }
    response = app.test_client().post('/contact', json=incomplete_contact)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']


def test_contact_validation_invalid_email():
    '''Test that POST /contact returns 400 for invalid email format'''
    invalid_contact = {
        "name": "John Doe",
        "email": "invalid-email-format",
        "phone": "+1234567890",
        "linkedin": "https://linkedin.com/in/johndoe",
        "github": "https://github.com/johndoe"
    }
    response = app.test_client().post('/contact', json=invalid_contact)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Invalid email format' in response.json['error']


def test_contact_validation_invalid_phone():
    '''Test that POST /contact returns 400 for invalid phone format'''
    invalid_contact = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",  # Missing + sign
        "linkedin": "https://linkedin.com/in/johndoe",
        "github": "https://github.com/johndoe"
    }
    response = app.test_client().post('/contact', json=invalid_contact)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Invalid phone format' in response.json['error']


def test_no_json_data_experience():
    '''Test that POST /resume/experience returns 400 when no JSON data is provided'''
    response = app.test_client().post('/resume/experience')
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'No JSON data provided' in response.json['error']


def test_no_json_data_education():
    '''Test that POST /resume/education returns 400 when no JSON data is provided'''
    response = app.test_client().post('/resume/education')
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'No JSON data provided' in response.json['error']


def test_no_json_data_skill():
    '''Test that POST /resume/skill returns 400 when no JSON data is provided'''
    response = app.test_client().post('/resume/skill')
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'No JSON data provided' in response.json['error']


def test_none_values_experience():
    '''Test that POST /resume/experience returns 400 when fields have None values'''
    experience_with_none = {
        "title": "Software Developer",
        "company": None,  # None value
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "description": "Test description",
        "logo": "test-logo.png"
    }
    response = app.test_client().post('/resume/experience', json=experience_with_none)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']


def test_none_values_education():
    '''Test that POST /resume/education returns 400 when fields have None values'''
    education_with_none = {
        "course": "Computer Science",
        "school": None,  # None value
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "grade": "A",
        "logo": "test-logo.png"
    }
    response = app.test_client().post('/resume/education', json=education_with_none)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']


def test_none_values_skill():
    '''Test that POST /resume/skill returns 400 when fields have None values'''
    skill_with_none = {
        "name": None,  # None value
        "proficiency": "Expert",
        "logo": "test-logo.png"
    }
    response = app.test_client().post('/resume/skill', json=skill_with_none)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']


def test_experience_validation_success():
    '''Test that POST /resume/experience succeeds with valid data'''
    valid_experience = {
        "title": "Software Developer",
        "company": "Valid Company",
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "description": "Valid description",
        "logo": "valid-logo.png"
    }
    response = app.test_client().post('/resume/experience', json=valid_experience)
    assert response.status_code == 201  # Created
    assert 'id' in response.json


def test_education_validation_success():
    '''Test that POST /resume/education succeeds with valid data'''
    valid_education = {
        "course": "Computer Science",
        "school": "Valid University",
        "start_date": "Jan 2025",
        "end_date": "Dec 2025",
        "grade": "A",
        "logo": "valid-logo.png"
    }
    response = app.test_client().post('/resume/education', json=valid_education)
    assert response.status_code == 201  # Created
    assert 'id' in response.json


def test_skill_validation_success():
    '''Test that POST /resume/skill succeeds with valid data'''
    valid_skill = {
        "name": "Python",
        "proficiency": "Expert",
        "logo": "python-logo.png"
    }
    response = app.test_client().post('/resume/skill', json=valid_skill)
    assert response.status_code == 201  # Created
    assert 'id' in response.json


def test_contact_validation_success():
    '''Test that POST /contact succeeds with valid data'''
    valid_contact = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "linkedin": "https://linkedin.com/in/johndoe",
        "github": "https://github.com/johndoe"
    }
    response = app.test_client().post('/contact', json=valid_contact)
    assert response.status_code == 201  # Created
