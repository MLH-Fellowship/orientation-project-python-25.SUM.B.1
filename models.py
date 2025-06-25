# pylint: disable=R0913
'''
Models for the Resume API. Each class is related to
'''

from dataclasses import dataclass


@dataclass
class Experience:
    '''Experience model with job history details.'''
    id: int
    title: str
    company: str
    start_date: str
    end_date: str
    description: str
    logo: str


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
