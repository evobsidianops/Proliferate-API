from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female')
)

AVAILABILITY_CHOICES = (
    ('Weekdays', 'Weekdays'),
    ('Weekends', 'Weekends'),
    ('Morning', 'Morning'),
    ('Afternoons', 'Afternoons'),
    ('Evenings', 'Evenings')
)

LANGUAGE_CHOICES = (
    ('english', 'english'),
    ('french', 'french'),
    ('spanish', 'spanish') 
)

# Choices below have insufficient detail from the figma design
ATTENDANCE_CHOICES = (
    ('multiselect_tags', 'multiselect_tags'),
    ('multiselect_tags2', 'multiselect_tags2')
)
# Choices below have insufficient detail from the figma design
SUBJECT_CHOICES = (
    ('multiselect_tags', 'multiselect_tags'),
    ('multiselect_tags2', 'multiselect_tags2')
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class UserInfo(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    grade_or_year = models.CharField(max_length=30, null=True, blank=True)
    current_location = models.CharField(max_length=120, null=True, blank=True)
    subjects = models.CharField(max_length=510, choices=SUBJECT_CHOICES, null=True, blank=True)
    attendance = models.CharField(max_length=255, choices=ATTENDANCE_CHOICES, null=True, blank=True)
    availability = models.CharField(max_length=510, choices=AVAILABILITY_CHOICES)
    additional_preferences = models.TextField(null=True, blank=True)
    communication_language = models.CharField(max_length=255, choices=LANGUAGE_CHOICES)
    short_term_goals = models.TextField(null=True, blank=True)
    long_term_goals = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'