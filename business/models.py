from pyexpat import model
from tabnanny import verbose
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class PublishedManageer(models.Manager):
    def get_queryset(self):
        return super(PublishedManageer,self).get_queryset().filter(status='published')

class Customer(models.Model):
    STATUS_CHOICES = {
        ('draft','Draft'),
        ('published','Published'),
    }
    GENDER_CHOICES = {
        ('M','Male'),
        ('F','Female'),
        ('I','InterSex'),
    }
    title = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.PROTECT, default=1)
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManageer()
 
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name
