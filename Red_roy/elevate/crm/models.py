# crm/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


User = get_user_model()
class ReservationClient(models.Model):
    event_title = models.CharField(max_length=100)
    places = models.IntegerField()
    name = models.CharField(max_length=100)
    tel= models.CharField(max_length=8, validators=[RegexValidator(r'^\d{8}$')],default='00000000')
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.CharField(max_length=100)
    def __str__(self):
        return f"Reservation by {self.name}: {self.event_title}"
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    places = models.IntegerField()
    association = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    phone = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{8}$')],default='00000000')
    ESPACE_CHOICES = [
        ('cinema', 'Cinema'),
        ('coffee', 'Coffee'),
        ('theatre', 'Theatre'),
    ]
    espace = models.CharField(max_length=10, choices=ESPACE_CHOICES,default='cinema')

    

    def __str__(self):
        return f"Reservation by {self.user}: {self.association} on {self.date} at {self.time} in {self.espace}"
class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    # Redefine groups field with a unique related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'
    )

    # Redefine user_permissions field with a unique related_name
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_places = models.PositiveIntegerField()
    image = models.ImageField(upload_to='media/',default='media/1.jpg',blank=True, null=True)
    TYPE_CHOICES = [
        ('cinema', 'Cinema'),
        ('theatre', 'Theatre'),
        ('other', 'other'),

    ]
    espace = models.CharField(max_length=10, choices=TYPE_CHOICES,default='other')
    def __str__(self):
        return f"{self.id} - {self.title}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    images= models.ImageField(upload_to='media/',blank=True, null=True)

    def __str__(self):
        return f"Image for {self.blog_post.title}"

