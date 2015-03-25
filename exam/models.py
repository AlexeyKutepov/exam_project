from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
    """
    The user-profile model
    """

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.

    # The user's middle name
    middle_name = models.CharField(max_length=50, blank=True)
    # The user's birthday
    birthday = models.DateField()
    # Gender
    gender = models.CharField(max_length=6, choices=GENDER, default=MALE)
    # The user's profile image
    picture = models.ImageField(upload_to='profile_images', blank=True)
    # Country
    country = models.CharField(max_length=100)
    # City
    city = models.CharField(max_length=100)
    # The user's full address
    address = models.CharField(max_length=500, blank=True)
    # The institution where the user works or studies
    institution = models.CharField(max_length=500, blank=True)
    # The user's job
    job = models.CharField(max_length=500, blank=True)
    # The user's registration date
    registration_date = models.DateTimeField(default=datetime.datetime.now())
    # How many tests complete this user and how many tests created this user.
    rating = models.IntegerField(default=0)

    def full_name(self):
        return self.user.last_name + " " + self.user.first_name + " " + self.middle_name

    def __str__(self):
        return self.full_name()


class Category(models.Model):
    """
    The category of the tests
    """
    name = models.CharField(max_length=128, unique=True)
    # Date and time
    date_and_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.name


class Test(models.Model):
    """
    The model of the test
    """

    # The name of the test
    name = models.CharField(max_length=500)
    # The description of test
    description = models.TextField(blank=True)
    # The file of the test
    test = models.BinaryField()
    # The author of the test
    author = models.ForeignKey(UserProfile)
    # The category of the test
    category = models.ForeignKey(Category)
    # Date and time
    date_and_time = models.DateTimeField(default=datetime.datetime.now())
    # How many users complete this test.
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Journal(models.Model):
    """
    The result journal
    """

    # The user, who complete a test
    user = models.ForeignKey(UserProfile)
    # The completed test
    test = models.ForeignKey(Test)
    # Date and time
    date_and_time = models.DateTimeField(default=datetime.datetime.now())
    # The result of test
    result = models.IntegerField(default=0)
    # The report of the test (JSON - file)'
    report = models.TextField()

    def __str__(self):
        return self.user.user.last_name + " " + self.user.user.first_name + " " + self.user.middle_name
