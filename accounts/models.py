from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.urls import reverse 
from django.core.validators import FileExtensionValidator,MinValueValidator, MaxValueValidator,EmailValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg


class DateManager(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class CustomUser(AbstractUser, DateManager):
    '''
    This is our main user model , contains comman detail for all user_types.

    '''
    email = models.EmailField(_("email address"), unique=True,)
    country = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=10)
    Male = "M"
    Female = "F"
    GENDER_CHOICES = [
        (Male, "Male"),
        (Female, "Female"),
    ]
    profile_pic = models.ImageField(upload_to='profile_pics/',
                validators=[
                FileExtensionValidator(
                        allowed_extensions = ["png",'jpeg', 'jpg'],
                        message = 'only jpeg and png extensions allowed'),
                        ], blank=True, null=True, default='default.jpeg')
    
    gender =  models.CharField(max_length = 1, choices=GENDER_CHOICES , blank=True ,null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'gender']

    
    def __str__(self):
        return self.email
    
    @property
    def average_rating(self):
        rating_obj = CustomUser.objects.filter(id=self.id).annotate(raiting=Avg('rating_to__star_rating',default=0))
        return rating_obj.first().raiting
    
    class Meta:
        verbose_name ='CustomUser'

class Freelancer(CustomUser):
    '''
    Profile model for freelancer user_type
    '''
    years_of_experience = models.PositiveIntegerField(null=True, default=0)
    resume = models.FileField(upload_to = 'resumes/', 
                        validators = [FileExtensionValidator(
                        allowed_extensions = ['pdf', 'txt', 'doc'],
                        message = 'only pdf , txt , doc extensions allowed')], 
                        blank=True, null=True)

    
    class Meta:
        verbose_name = 'Freelancer'
        permissions = (("is_freelancer", "freelancer user type"),)

    def __str__(self):
        return self.username
    

class SelfSkill(models.Model):

    PROFIENCY_CHOICES = [
        ('BEG', 'BEGINEER'),
        ('INT', 'INTERMIDIATE'),
        ('EXP', 'EXPERT')
    ]
    
    name = models.CharField(max_length=100)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE,null=True)
    level = models.CharField(max_length=3, choices=PROFIENCY_CHOICES)




class Education(DateManager):
    '''
    This model contains education details of freelancer and refrence freelancer model
    '''
    DEGREE_TYPE_CHOICES = [
        ("GD" , 'GRADUATION'),
        ("PG" , 'POST GRADUATION')
    ]

    type  = models.CharField(max_length=2, choices = DEGREE_TYPE_CHOICES)
    degree_name = models.CharField(max_length=40)
    course  = models.CharField(max_length=30)
    college_name = models.CharField(max_length=40) 
    start_date = models.DateField()
    end_date = models.DateField()
    freelancer= models.ForeignKey(Freelancer, on_delete=models.CASCADE)

    class Meta:
        verbose_name ='Education'

    def __str__(self):
        return self.course   


class Client(CustomUser):
    '''
    Profile model for client user_type  
    '''

    CHOICES = [
        ('Community', 'Comunity'),
        ('individual', "individual"),
    ]
    type = models.CharField(max_length=10, choices=CHOICES)
    company_name = models.CharField(max_length=30, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Client'
        permissions = (("is_client", "client user type"),)

    def __str__(self):
        return self.username


class Skill(DateManager):
    '''
    This model stores standard skills and skills created by clients(jobposters,) 
    '''
    name = models.CharField(max_length=30)
    client = models.ForeignKey(Client, on_delete=models.CASCADE , null=True)
    
    class Meta:
        verbose_name = 'Skill'

    def __str__(self):
        return self.name 
    


