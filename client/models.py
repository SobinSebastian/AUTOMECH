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

    base_role = Role.CLIENT

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

class UserInfo(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=11)
    address=models.CharField(max_length=100,null=True)
    place = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


class CarMake(models.Model):
    make_name = models.CharField(max_length=100,unique=True)
    make_Image = models.ImageField(upload_to='make_images/',blank=True, null=True)
    def __str__(self):
        return self.make_name

class CarModel(models.Model):
    model_name = models.CharField(max_length=100,unique=True)
    make_company = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    model_Image = models.ImageField(upload_to='model_images/',blank=True, null=True)
    def __str__(self):
        return self.model_name

class Fueltype(models.Model):
    fuel_name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.fuel_name

class transmissionType(models.Model):
    transmission_name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.transmission_name

class ModelVariant(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(Fueltype, on_delete=models.CASCADE)
    torque = models.CharField(max_length=50)
    bhp = models.CharField(max_length=50)
    engine = models.CharField(max_length=50)
    transmission = models.ForeignKey( transmissionType , on_delete=models.CASCADE)
    tyre_size = models.CharField(max_length=50)
    variant_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.model.model_name} - {self.variant_name}"
    class Meta:
        unique_together = ('model', 'variant_name',)

class Vehicleinfo(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    model_variant = models.ForeignKey(ModelVariant, on_delete=models.CASCADE)
    vehicle_Regno = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
