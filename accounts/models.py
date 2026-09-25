from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True, editable=False)

    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name='Email Address',
        db_index=True,
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Phone Number',
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Street Address',
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='City',
    )
    postcode = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Postal Code',
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        verbose_name='Profile Picture',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.email

    def get_full_name(self):
        parts = [self.first_name, self.last_name]
        return ' '.join(part for part in parts if part).strip()
