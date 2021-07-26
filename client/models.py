from uuid import uuid4
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from client.manager import CustomUserManager


# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')


class Profile(models.Model):
    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
        (3, _('Other')),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=_("Phone number must be in format '+999999999'"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='id',
                                primary_key=True, related_name='profile',
                                verbose_name=_('User'), blank=False, null=False)
    first_name = models.CharField(max_length=64, verbose_name=_('First name'))
    last_name = models.CharField(max_length=64, verbose_name=_('Last name'))
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    verbose_name=_('Phone number'))
    address = models.CharField(max_length=300, verbose_name=_('Address'))
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=3,
                                              verbose_name=_('Gender'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Created at:'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
