from django.db import models
from django.db.utils import cached_property
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.urls import reverse

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('Email is required')

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        user = self.model(
            email=self.normalize_email(email),
            is_staff=extra_fields['is_staff'],
            is_superuser=extra_fields['is_superuser']
        )

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields['is_superuser'] is not True:
            raise ValueError('is_superuser must be true for superusers')

        if extra_fields['is_staff'] is not True:
            raise ValueError('is_staff must be true for superusers')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(
        'Personal Image',
        upload_to='profiles/images/',
        blank=True,
        default='avatar-icon.png'
    )

    bio = models.TextField(blank=True)

    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)

    email = models.EmailField(unique=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def is_admin(self):
        return self.is_superuser

    @cached_property
    def get_full_name(self):

        return f'{self.first_name} {self.last_name}'.strip()

    @cached_property
    def get_channels_group(self):

        return f'group_{self.pk}'

    @cached_property
    def get_profile_url(self):
        return reverse('user_detail_view', args=[self.pk])


class Notification(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_notifications', on_delete=models.SET_NULL, null=True)
    recipients = models.ManyToManyField(
        User, related_name='received_notifications')
    verb = models.CharField(max_length=100)
    content = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
