from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, firstname, middlename, lastname, email, address, zone, date_of_birth, password=None, phone_number1=None, phone_number2=None):
        if not username:
            raise ValueError("Users must have a username")
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            email=email,
            address=address,
            zone=zone,
            date_of_birth=date_of_birth,
            phone_number1=phone_number1,
            phone_number2=phone_number2,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, firstname, middlename='', lastname='', email=None, address='', zone='1', date_of_birth=None, password=None, phone_number1=None, phone_number2=None):
        user = self.create_user(
            username,
            firstname,
            middlename,
            lastname,
            email,
            address,
            zone,
            date_of_birth,
            password,
            phone_number1=phone_number1,
            phone_number2=phone_number2,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True)
    
    zone_choices = [
        ('1', 'Zone 1'),
        ('2', 'Zone 2'),
        ('3', 'Zone 3'),
        ('4', 'Zone 4'),
        ('5', 'Zone 5'),
    ]
    zone = models.CharField(max_length=1, choices=zone_choices)
    date_of_birth = models.DateField()

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('secretary', 'Secretary'),
        ('zonal_head', 'Zonal Fellowship Head'),
        ('member', 'member')
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    phone_number1 = models.CharField(max_length=15, blank=True, null=True)  # New phone number field
    phone_number2 = models.CharField(max_length=15, blank=True, null=True)  # New phone number field

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email', 'zone', 'date_of_birth']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
