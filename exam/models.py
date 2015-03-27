from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from exam_project import settings


class UserProfileManager(BaseUserManager):

    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """
    The user-profile model
    """

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # The additional attributes we wish to include.

    # The user's last name
    last_name = models.CharField(max_length=50, blank=True)
    # The user's first name
    first_name = models.CharField(max_length=50, blank=True)
    # The user's middle name
    middle_name = models.CharField(max_length=50, blank=True)
    # The user's birthday
    date_of_birth = models.DateField()
    # Gender
    gender = models.CharField(max_length=6, choices=GENDER, default=MALE)
    # The user's profile image
    picture = models.ImageField(upload_to='profile_images', blank=True)
    # Country
    country = models.CharField(max_length=100, blank=True)
    # City
    city = models.CharField(max_length=100, blank=True)
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

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # The category of the test
    category = models.ForeignKey(Category)
    # Date and time
    date_and_time = models.DateTimeField(default=datetime.datetime.now())
    # How many users complete this test.
    rating = models.IntegerField(default=0)
    # Public or not public test
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Journal(models.Model):
    """
    The result journal
    """

    # The user, who complete a test
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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
