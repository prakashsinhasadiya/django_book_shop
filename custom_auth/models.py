
from datetime import datetime, timedelta
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from slugger import AutoSlugField


class UserProfile(TimeStampedModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
            regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17)
    first_name = models.CharField(
        max_length=30)
    # def clean_mobile(request):
    last_name = models.CharField(
        max_length=30)
    email = models.EmailField(
      )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    profile_image = models.ImageField(upload_to = 'picture')

class BookDetail(TimeStampedModel):

    book_name = models.CharField(max_length=30)
    auther_name = models.CharField(max_length=30)
    book_details = models.CharField(max_length=300)
    book_price = models.FloatField()
    book_image = models.ImageField(upload_to='picture')
    book_file =  models.FileField(upload_to='picture')
    slug = AutoSlugField(populate_from='book_name',unique=True,blank=True,null=True)
