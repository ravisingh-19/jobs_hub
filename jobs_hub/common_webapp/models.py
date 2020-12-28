from django.db import models
import random
from datetime import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _ 

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):

        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            email = self.normalize_email(email),
        )
        user.account_type = 'U'
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.account_type = 'S'
        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    accounttype= (
        ('S', 'Super Admin'),
        ('A', 'Admin'),
        ('U', 'User'),
    )
    email = models.EmailField(
        verbose_name = 'email address',
        max_length = 255,
        unique = True
    )
    profile_photo  = models.ImageField(upload_to='media/images/', null=True, blank=True)
    account_type = models.CharField(max_length=1, choices=accounttype, default='U')
    mobile_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=100, null=True, blank=True)
    google_id = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified_phone = models.BooleanField(default=False)
    otp_created = models.DateTimeField(null=True, blank=True)
    countrycode = models.CharField(max_length=9, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

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
        return self.is_admin
    
    def send_otp(self):
        self.otp = random.randint(100000, 999999)
        self.otp_created = datetime.now()   
    
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

    def clean(self):
        if self.name == '':
            raise ValidationError(_('INVALID FORM DATA!.'))