from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from exam_project import settings


class UserProfileManager(BaseUserManager):
    def _create_user(self, email, date_of_birth, password,
                     is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            date_of_birth=date_of_birth,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, date_of_birth, password=None, **extra_fields):
        return self._create_user(email, date_of_birth, password, False,
                                 **extra_fields)

    def create_superuser(self, email, date_of_birth, password, **extra_fields):
        return self._create_user(email, date_of_birth, password, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
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
    position = models.CharField(max_length=500, blank=True)
    # The user's registration date
    registration_date = models.DateTimeField(default=timezone.now())
    # How many tests complete this user and how many tests created this user.
    rating = models.IntegerField(default=0)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_short_name(self):
        return self.first_name + ' ' + self.last_name

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
        return self.is_superuser


class Category(models.Model):
    """
    The category of the tests
    """
    name = models.CharField(max_length=128, unique=True)
    # Date and time
    date_and_time = models.DateTimeField(default=timezone.now())

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
    # The test
    test = models.BinaryField(blank=True)
    # The author of the test
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # The category of the test
    category = models.ForeignKey(Category)
    # date and time of create test
    date_and_time = models.DateTimeField(default=timezone.now())
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

    # The user, who was complete the test
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # The completed test
    test = models.ForeignKey(Test)
    # Date and time of start test
    start_date = models.DateTimeField(default=timezone.now())
    # Date and time of end test
    end_date = models.DateTimeField(default=timezone.now())
    # Number of questions
    number_of_questions = models.IntegerField()
    # Number of correct answers
    number_of_correct_answers = models.IntegerField(default=0)
    # The result of test (%)
    result = models.IntegerField(default=0)
    # The report of the test (JSON - file)'
    report = models.BinaryField()

    def __str__(self):
        return self.user.user.last_name + " " + self.user.user.first_name + " " + self.user.middle_name


class Progress(models.Model):
    """
    The progress of the performing tests by users
    """

    # The user, who  performs the test
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Start date time
    start_date = models.DateTimeField(default=timezone.now())
    # End date time
    end_date = models.DateTimeField(blank=True, null=True)
    # The performed test by user
    test = models.ForeignKey(Test)
    # The current result
    result_list = models.BinaryField(blank=True, null=True)
    # Number of correct answers
    current_result = models.IntegerField(default=0)


class TestImage(models.Model):
    """
    There are images for tests
    """
    image = models.ImageField(upload_to='test_images', blank=True)
