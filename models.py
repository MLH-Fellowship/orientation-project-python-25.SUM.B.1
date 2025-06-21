# pylint: disable=R0913

'''
Models for the Resume API. Each class is related to
'''

from dataclasses import dataclass


@dataclass
class Experience:
    def __init__(self, role, company, start, end, description, logo):
        self.role = role
        self.company = company
        self.start = start
        self.end = end
        self.description = description
        self.logo = logo

    def serialize(self):
        return {
            "role": self.role,
            "company": self.company,
            "start": self.start,
            "end": self.end,
            "description": self.description,
            "logo": self.logo
        }


@dataclass
class Education:
    '''
    Education Class
    '''
    course: str
    school: str
    start_date: str
    end_date: str
    grade: str
    logo: str


@dataclass
class Skill:
    '''
    Skill Class
    '''
    name: str
    proficiency: str
    logo: str
