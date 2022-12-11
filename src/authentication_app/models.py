from typing import List
from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    ''' User details Model'''
    first_name:str = models.CharField(name="first_name", max_length=100, blank=False)
    last_name:str = models.CharField(name="last_name", max_length=100, blank=False)
    email:str = models.EmailField(name="email", unique=True, max_length=120)
    password:str = models.CharField(name="password",max_length=300, blank=False)
    username = None

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['first_name', 'last_name', 'password']

    def __str__(self):
        return f"Firstname: {self.first_name}, Lastname: {self.last_name}, Email_address: {self.email}"

    __repr__ = __str__
