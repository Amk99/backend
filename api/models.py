from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


from .managers import UserManager

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    following = models.ManyToManyField(
        "self", blank=True, related_name="followers", symmetrical=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.email