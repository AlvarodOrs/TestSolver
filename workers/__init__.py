"""
Workers module for specific automation tasks
"""

from .logIn import logIn
from .course_finder import find_and_click_courses, save_course_data

__all__ = ['logIn', 'find_and_click_courses', 'save_course_data']
