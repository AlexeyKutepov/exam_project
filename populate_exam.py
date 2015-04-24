import pickle
import random

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
    add_super_user()
    user1 = add_user(
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
    category1 = add_cat("category 1")
    add_test(
        "test 1",
        "test 1 description",
        user1,
        category1
    )
    user2 = add_user(
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
    category2 = add_cat("category 2")
    add_test(
        "test 2",
        "test 2 description",
        user2,
        category2
    )
    user3 = add_user(
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
    category3 = add_cat("category 3")
    add_test(
        "test 3",
        "test 3 description",
        user3,
        category3
    )
    user4 = add_user(
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
    category4 = add_cat("category 4")
    add_test(
        "test 4",
        "test 4 description",
        user4,
        category4
    )
    user5 = add_user(
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
    category5 = add_cat("category 5")
    add_test(
        "test 5",
        "test 5 description",
        user5,
        category5
    )
    add_cat("category 6")
    add_cat("category 7")
    add_cat("category 8")
    add_cat("category 9")
    add_cat("category 10")


def add_super_user():
    """
    Creates a superuser
    :return:
    """
    try:
        user = django.contrib.auth.get_user_model().objects.create_superuser(
            email="admin@gmail.com",
            date_of_birth="1990-01-01",
            password="admin"
        )
        return user
    except:
        print("Impossible to create a superuser.")


def add_user(email, password, first_name, middle_name, last_name, birthday, gender, country, city):
    """
    Creates new user into database
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
    user_profile = django.contrib.auth.get_user_model().objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        date_of_birth=birthday,
        gender=gender,
        country=country,
        city=city
    )
    return user_profile


def add_cat(name):
    """
    Creates new category into database
    :param name:
    :return:
    """
    category = Category.objects.get_or_create(name=name)[0]
    return category


def add_test(name, description, author, category):
    """
    Creates new test
    :param name: name of the test
    :param description: description of the test
    :param author:
    :param category:
    :return:
    """
    test = exam_test.ExamTest()
    number_of_questions = random.randint(1, 100)
    number_of_answers = random.randint(2, 10)
    for i in range(number_of_questions):
        question = exam_test.Question("question " + str(i))
        for j in range(number_of_answers):
            if random.randint(0, 1) == 0:
                is_correct = False
            else:
                is_correct = True
            answer = exam_test.CloseAnswer("answer " + str(j), is_correct)
            question.add_new_answer(answer)
        test.add_question(question)
    test_dump = pickle.dumps(test)
    result = Test.objects.get_or_create(
        name=name,
        description=description,
        test=test_dump,
        author=author,
        category=category
    )[0]
    return result


if __name__ == '__main__':
    print("Starting Exam population script...")
    populate()
    print("Complete!")