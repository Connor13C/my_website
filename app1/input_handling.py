import re

from models.db import ProjectModel


def sanitize_input(_input):
    """Removes any potentially unsafe characters from string that are sent from outside the server."""
    if isinstance(_input, dict):
        return {sanitize_input(key): sanitize_input(value) for key, value in _input.items()}
    if isinstance(_input, list):
        return [sanitize_input(item) for item in _input]
    if isinstance(_input, str):
        return re.sub('[^0-9a-zA-z \',:;?!$#@.&_()-]+', '', _input)


def valid_date(date: str) -> bool:
    """Checks to see if the date is a string in the format YYYY-MM. Returns True if valid date, False if not."""
    if date:
        if re.fullmatch(r'\d{4}-\d{2}', date):
            return True
    return False


def valid_project(project_id: int) -> ProjectModel:
    """Checks to see if a Project matching that id is in the database."""
    if project_id:
        return ProjectModel.get_by_project_id(project_id)
