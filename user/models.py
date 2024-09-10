from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# class CustomAccountManager(BaseUserManager):
#     def create_user(self, email, username=None, first_name=None, **other_fields):
#         if not email:
#             raise ValueError(_('You must provide an email address'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, first_name=first_name, **other_fields)
#         user.set_unusable_password()  # No password needed for OAuth
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, first_name, password=None, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         #other_fields.setdefault('is_active', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must be assigned to is_staff=True.')
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must be assigned to is_superuser=True.')

#         return self.create_user(email, username=username, first_name=first_name, password=password, **other_fields)
        
class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username=None, first_name=None, password=None, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        
        if password:
            user.set_password(password)  # Set the password if provided
        else:
            user.set_unusable_password()  # Use this for OAuth-based accounts
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username=username, first_name=first_name, password=password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    print('User model created')
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']

    def __str__(self):
        return self.email

class YouTubeAccount(models.Model):
    user = models.ForeignKey(User, related_name='youtube_accounts', on_delete=models.CASCADE)
    youtube_id = models.CharField(max_length=255, unique=True)
    youtube_etag = models.CharField(max_length=255, null=True, blank=True)
    youtube_title = models.CharField(max_length=255, null=True, blank=True)
    youtube_description = models.TextField(null=True, blank=True)
    youtube_custom_url = models.CharField(max_length=255, null=True, blank=True)
    youtube_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.youtube_title or "YouTube Account"
