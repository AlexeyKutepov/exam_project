__author__ = 'Alexey Kutepov'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_project.settings')

import django
django.setup()

from exam.models import *
from django.contrib.auth.models import User


def populate():
    """
    Populates the database.
    :return:
    """
    add_super_user()
    add_user(
        "ivanov",
        "ivanov@gmail.com",
        "ivanov_pass",
        "Ivan",
        "Ivanovich",
        "Ivanov",
        "1980-01-01",
        UserProfile.MALE,
        "Russia",
        "Moscow"
    )
    add_user(
        "petrov",
        "ipetrov@gmail.com",
        "petrov_pass",
        "Petr",
        "Petrovich",
        "Petrov",
        "1985-02-02",
        UserProfile.MALE,
        "Russia",
        "Moscow"
    )
    add_user(
        "nikolaev",
        "nikolaev@gmail.com",
        "nikolaev_pass",
        "Nikolay",
        "Nickolaevich",
        "Nickolaev",
        "1990-03-03",
        UserProfile.MALE,
        "Russia",
        "Moscow"
    )
    add_user(
        "vasileva",
        "vasileva@gmail.com",
        "vasileva_pass",
        "Mariya",
        "Petrovna",
        "Vasileva",
        "1991-04-04",
        UserProfile.FEMALE,
        "Russia",
        "Moscow"
    )
    add_user(
        "nikiforova",
        "nikiforova@gmail.com",
        "nikiforova_pass",
        "Irina",
        "Vladimirovna",
        "Nikiforova",
        "1991-04-04",
        UserProfile.FEMALE,
        "Russia",
        "Moscow"
    )


def add_super_user():
    """
    Creates a superuser
    :return:
    """
    try:
        user = User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="admin"
        )
        return user
    except:
        print("Impossible to create a superuser.")


def add_user(username, email, password, first_name, middle_name, last_name, birthday, gender, country, city):
    """
    Creates new user into database
    :param username:
    :param email:
    :param password:
    :param first_name:
    :param middle_name:
    :param last_name:
    :param birthday:
    :param gender
    :param country:
    :param city:
    :return:
    """
    user = User.objects.get_or_create(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    user_profile = UserProfile.objects.get_or_create(
        user_id=user[0].id,
        middle_name=middle_name,
        birthday=birthday,
        gender=gender,
        country=country,
        city=city
    )[0]
    return user_profile


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
    print("Complete!")