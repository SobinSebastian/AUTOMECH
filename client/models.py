from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    
    email=models.EmailField(max_length=100,unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name']
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        MECHANIC="MECHANIC",'Mechanic'
        CLIENT="CLIENT",'Client'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

class Client(User):

    base_role = User.Role.CLIENT
    class Meta:
        proxy = True

class Mechanic(User):

    base_role = User.Role.MECHANIC
    
    class Meta:
        proxy = True