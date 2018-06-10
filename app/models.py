from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
MY_CHOICES2 = ((1, 'Item title 2.1'),
               (2, 'Item title 2.2'),
               (3, 'Item title 2.3'),
               (4, 'Item title 2.4'),
               (5, 'Item title 2.5'))
FRESHMAN = 'LK'
SOPHOMORE = 'LW'
JUNIOR = 'JR'
SENIOR = 'SR'
YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, '老街'),
        (SOPHOMORE, '羅湖'),
        (JUNIOR, '??'),
        (SENIOR, '??'),
)
class CNSSpecialField(models.Model):
    title = models.CharField(max_length=200,null=True,unique=True,blank=True)
    original_price = models.CharField(max_length=200,null=True,unique=True,blank=True)
    discount_price = models.CharField(max_length=200,null=True,unique=True,blank=True)
    period = models.IntegerField(default=1)
class CNS(models.Model):
    CHtitle = models.CharField(max_length=200,null=True,unique=True,blank=True)
    CNtitle = models.CharField(max_length=200,null=True,unique=True,blank=True)
    ENGtitle = models.CharField(max_length=200,null=True,unique=True,blank=True)
    full_address =  models.CharField(max_length=200,null=False,default=" ")
    district =models.CharField(max_length=2,choices=YEAR_IN_SCHOOL_CHOICES, default=FRESHMAN)
    telephone = models.CharField(max_length=200,null=False)
    promote_rank=models.IntegerField(null=True,blank=True,default=0)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    cnsc = models.ForeignKey(CNSSpecialField, related_name='imagess',on_delete=models.CASCADE,default=1,)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def save(self,*args,**kwargs):
            if self.CHtitle is not None:
                self.CHtitle = self.CHtitle.lower().strip() # Hopefully reduces junk to ""
            if self.CHtitle == "":
                self.CHtitle = None
                self.CNtitle = None
                self.ENGtitle = None
            super(CNS, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.id)
class CNSImage(models.Model):
    cns = models.ForeignKey(CNS, related_name='images',on_delete=models.CASCADE,)
    image = models.ImageField()
class CNSExtraField(models.Model):
    cnsx = models.ForeignKey(CNS, related_name='extra_fields',on_delete=models.CASCADE,)
    title = models.CharField(max_length=200,null=True,blank=True)
    original_price = models.IntegerField(default=1)
    discount_price = models.IntegerField(default=1)
    period = models.IntegerField(default=1)

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
    numeric = RegexValidator(r'^[0-9]*$', 'Only alphanumeric characters are allowed.')
    first_name = models.CharField(max_length=254, blank=True)
    second_name = models.CharField(max_length=254, blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True, unique= True)
    username = models.CharField(max_length=254, blank=True)
    phone_num = models.CharField(max_length=254,null=True,validators=[numeric],unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active   = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    USERNAME_FIELD='id'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()
    class Meta:
        verbose_name= _('user')
        verbose_name_plural=_('users')
    def save(self,*args,**kwargs):
            print(self.email)
            if self.email is not None:
                self.email = self.email.lower().strip() # Hopefully reduces junk to ""
            if self.email == "":
                self.email = None
            super(CustomUser, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)
    def get_full_name(self):
        full_name='%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    def get_short_name(self):
        return self.first_name
    def email_user(self,subject,message,from_email=None):
        send_mail(subject,message,from_email,[self.email])
    def __str__(self):
       return str(self.id)


# Create your models here.


# Create your models here.
