# pylint: disable=R0913
'''
Models for the Resume API. Each class is related to
'''

import re
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

@dataclass
class Contact:
    """Contact model with validation methods for email and phone."""
    name: str
    email: str
    phone: str
    linkedin: str
    github: str

    def validate_email(self) -> bool:
        """Validate the email format."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, self.email) is not None

    def validate_phone(self) -> bool:
        """Validate the phone number format with mandatory international country code."""
        # Require + sign followed by country code (1-3 digits) and phone number (7-12 digits)
        phone_regex = r'^\+[1-9]\d{7,14}$'  # Must start with +, then 8-15 total digits
        return re.match(phone_regex, self.phone) is not None

