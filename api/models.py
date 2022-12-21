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


class Post(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(_("description"),editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def likes_count(self):
       return self.likes.all().count()
    
    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')

    def __str__(self):
        return self.text