from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils import timezone

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
        MANAGER="MANAGER",'Manager'
        CLIENT="CLIENT",'Client'
    slug = models.SlugField(unique=True,blank=True)
    base_role = Role.CLIENT

    role = models.CharField(max_length=50, choices=Role.choices)
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role

        if not self.slug:
            base_slug = slugify(self.first_name)  
            unique_slug = base_slug
            counter = 1
            while User.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        return super().save(*args, **kwargs)

class Client(User):

    base_role = User.Role.CLIENT
    class Meta:
        proxy = True

class Mechanic(User):

    base_role = User.Role.MECHANIC
    
    class Meta:
        proxy = True

class Manager(User):

    base_role = User.Role.MANAGER
    
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
    make_slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.make_slug = slugify(self.make_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.make_name

class CarModel(models.Model):
    model_name = models.CharField(max_length=100,unique=True)
    make_company = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    model_Image = models.ImageField(upload_to='model_images/',blank=True, null=True)
    model_slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.model_slug = slugify(self.model_name)
        super().save(*args, **kwargs)

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
    variant_slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.variant_slug = slugify(f"{self.model.model_name}-{self.variant_name}")
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.model.model_name} - {self.variant_name}"
    class Meta:
        unique_together = ('model', 'variant_name',)

class Vehicleinfo(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    model_variant = models.ForeignKey(ModelVariant, on_delete=models.CASCADE)
    vehicle_Regno = models.CharField(max_length=20, unique=True)

class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.task_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.task_name

class ServiceList(models.Model):
    service_name = models.CharField(max_length=255,unique=True)
    service_category = models.ForeignKey('ServiceCategory', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    service_Image = models.ImageField(upload_to='service_images/',blank=True, null=True)
    tasks = models.ManyToManyField(Task)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.service_name )
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.service_name
    
class ServiceCenter(models.Model):
    place = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=15)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    manager = models.OneToOneField(Manager, on_delete=models.SET_NULL, null=True, blank=True, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.place}-{self.city}")
            unique_slug = base_slug
            counter = 1
            while ServiceCenter.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.place
    

class mechanicList(models.Model):
    mechanic = models.OneToOneField(Client, on_delete=models.CASCADE)
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mechanic)
   
class ServicesSlots(models.Model):
    slotname = models.CharField(max_length=100)
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)
    allocated_mech = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)  # Assuming Client is the correct model for the mechanic
    STATUS_CHOICES = [('ACTIVE','Active'),('INACTIVE','Inactive')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='INACTIVE')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.slotname)
            unique_slug = base_slug
            counter = 1
            while ServicesSlots.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slotname} - {self.service_center.place} - {self.allocated_mech.get_full_name()} - {self.status}"
    


class ServicePrice(models.Model):
    variant = models.ForeignKey(ModelVariant, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceList, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, max_length=255, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(f"{self.variant.model}-{self.variant.variant_name}-{self.service.service_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant.variant_name} - {self.service.service_name}"

    class Meta:
        unique_together = ('variant', 'service',)


import uuid
class Cart(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_info = models.ForeignKey(Vehicleinfo, on_delete=models.CASCADE)
    service_list = models.ForeignKey(ServiceList, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ['client', 'vehicle_info', 'service_list']

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_id = uuid.uuid4().hex[:10]
            self.slug = slugify(f"{self.service_list.service_name}-{unique_id}")
        super().save(*args, **kwargs)

class ServiceOrder(models.Model):
    STATUS_CHOICES = (
        ('on hold', 'On hold'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed'),
    )
    vehicle = models.ForeignKey(Vehicleinfo, on_delete=models.CASCADE)
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False, max_length=36)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on hold')
    service_slot = models.ForeignKey(ServicesSlots, on_delete=models.SET_NULL, null=True, blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=100, null=True,blank=True)
    razorpay_signature=models.CharField(max_length=100, null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.vehicle.vehicle_Regno} - {self.service_center.place} - {self.date} {self.time}"
    
class ServiceOrderItem(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)
    vehicle_info = models.ForeignKey(Vehicleinfo, on_delete=models.CASCADE)
    service_list = models.ForeignKey(ServiceList, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False, max_length=36)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super(ServiceOrderItem, self).save(*args, **kwargs)
    class Meta:
        unique_together = ['service_order', 'vehicle_info', 'service_list']

from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=ServiceOrderItem)
def update_service_order_status(sender, instance, **kwargs):
    service_order = instance.service_order
    if service_order.serviceorderitem_set.filter(status='completed').count() == service_order.serviceorderitem_set.count():
        service_order.status = 'completed'
        service_order.save()




class RoadsideAssistance(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]
    vehicle_info = models.ForeignKey('VehicleInfo', on_delete=models.CASCADE)
    service_center = models.ForeignKey('ServiceCenter', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES ,default='requested')
    slug = models.CharField(max_length=36, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True) 
    @property
    def created_at_in_local_timezone(self):
        return timezone.localtime(self.created_at)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        
        super(RoadsideAssistance, self).save(*args, **kwargs)

    def __str__(self):
        return f"Roadside Assistance for {self.vehicle_info.vehicle_Regno}"
    

#//////////////////////////////model For Blog //////////////////////////////////////////////////////
from tinymce.models import HTMLField
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
