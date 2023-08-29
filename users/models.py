from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,UnicodeUsernameValidator
from django.db import models

# Create your models here.

class CustomUser(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(('username'), max_length=150, unique=True)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    email = models.EmailField(('email address'), unique=True)
    is_staff = models.BooleanField(('staff status'), default=False,)
    is_active = models.BooleanField(('active'), default=True,)

    user_id = models.CharField(max_length=10, unique=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        abstract = True
    def __str__(self):
        return self.username



