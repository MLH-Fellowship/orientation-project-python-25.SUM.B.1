# pylint: disable=R0913
'''
Models for the Resume API. Each class is related to
'''

from dataclasses import dataclass


@dataclass
class Experience:
    '''Experience model with job history details.'''

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
    '''Education model with academic history.'''
    id: int
    course: str
    school: str
    start_date: str
    end_date: str
    grade: str
    logo: str


@dataclass
class Skill:
    '''Skill model with proficiency and logo.'''
    id: int
    name: str
    proficiency: str
    logo: str
