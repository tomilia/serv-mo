from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,is_staff,is_superuser, **extra_fields):
        now=timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user=self.model(email=email,is_staff=is_staff,is_active=True,is_superuser=is_superuser,last_login=now,date_joined=now,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email,password=None, **extra_fields):
        return self._create_user(email,password,False,False,**extra_fields)
    def create_superuser(self,email,password, **extra_fields):
        return self._create_user(email,password,True,True,**extra_fields)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254,unique=True)
    first_name = models.CharField(max_length=254, blank=True)
    second_name = models.CharField(max_length=254, blank=True)
    email = models.EmailField(blank=True,unique=True)
    phone_num = models.CharField(max_length=254,blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active   = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()
    class Meta:
        verbose_name= _('user')
        verbose_name_plural=_('users')
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)
    def get_full_name(self):
        full_name='%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    def get_short_name(self):
        return self.first_name
    def email_user(self,subject,message,from_email=None):
        send_mail(subject,message,from_email,[self.email])
# Create your models here.


# Create your models here.
