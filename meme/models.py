from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib import messages
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Aby dokonać rejestracji musisz podać adres email")
        if not username:
            raise ValueError("Aby dokonać rejestracji musisz podać nazwę użtkownia")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user      

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(max_length=32, unique=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.username}"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



def get_image_filepath(self, filename):
    return f"static/posts/{self.owner.id}/{self.pk}.png"

class Post(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    body = models.TextField()
    image = models.ImageField(max_length=255, upload_to=get_image_filepath, null=True, blank=True)
    added = models.DateTimeField(auto_now=True)
    interactions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering = ["-added"]




class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.id}"
    
class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.id}"
    



class Coment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.CharField(max_length=1024)
    added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.id}"
    
    class Meta:
        ordering = ["-added"]
    


class Interaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}"