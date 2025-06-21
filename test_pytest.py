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
    '''Add a new experience and then get all experiences.
    Confirm that it returns the new experience in the correct position.'''
    example_experience = {
        "role": "Software Developer",
        "company": "A Cooler Company",
        "start": "October 2022",
        "end": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    client = app.test_client()


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

# def test_education():
#     '''Add a new education and then get all educations.
#     Check that it returns the new education in that list'''
#     example_education = {
#         "course": "Engineering",
#         "school": "NYU",
#         "start_date": "October 2022",
#         "end_date": "August 2024",
#         "grade": "86%",
#         "logo": "example-logo.png"
#     }
#     item_id = app.test_client().post('/resume/education',
#                                      json=example_education).json['id']
#
#     response = app.test_client().get('/resume/education')
#     assert response.json[item_id] == example_education

# def test_skill():
#     '''Add a new skill and then get all skills.
#     Check that it returns the new skill in that list'''
#     example_skill = {
#         "name": "JavaScript",
#         "proficiency": "2-4 years",
#         "logo": "example-logo.png"
#     }
#
#     item_id = app.test_client().post('/resume/skill',
#                                      json=example_skill).json['id']
#
#     response = app.test_client().get('/resume/skill')
#     assert response.json[item_id] == example_skill
