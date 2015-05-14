__author__ = 'Alexey Kutepov'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_project.settings')

import django
django.setup()

from exam.models import *
from django.contrib.auth.models import User
from exam.exam_test import exam_test


def populate():
    """
    Populates the database.
    :return:
    """
    add_cat("Произвольная тема")
    add_cat("Технические науки")
    add_cat("Гуманитарные науки")


def add_cat(name):
    """
    Creates new category into database
    :param name:
    :return:
    """
    category = Category.objects.get_or_create(name=name)[0]
    return category

if __name__ == '__main__':
    print("Starting Exam population script...")
    populate()
    print("Complete!")