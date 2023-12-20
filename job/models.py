from django.db import models

# Create your models here.
from django.db import models
# Create your models here.
from accounts.models import *
from django.core.validators import FileExtensionValidator

class JobPost(DateManager):
    '''
    Client can Post multiple jobs , This Model stores info about jobs.
    '''
    JOB_STATUS = [
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED'),
    ]

    DURATION_CHOICES = [
                       ('DAY' , 'DAY'), 
                       ('WEEK' , 'WEEK'),
                       ('MONTH' , 'MONTH'),
                       
                       ] 
    CURRENCY_CHOICES = [

        ('USD','DOLLAR')
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    experience_required = models.PositiveIntegerField()
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete = models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 10, choices = JOB_STATUS,  default=JOB_STATUS[0][0])
    duration_type = models.CharField( max_length=10, choices = DURATION_CHOICES,)
    duration = models.PositiveIntegerField(null=True, help_text = 'duration must be an integer')
    currency = models.CharField(max_length=3,choices=CURRENCY_CHOICES)
    salary = models.PositiveIntegerField(help_text = 'job salary')
    skill_required = models.ManyToManyField(Skill)
    
 
    class Meta:
        verbose_name = 'Post'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
       
class JobProposal(DateManager):
    '''
    This model store data of JobProposal , User can send to client to get job
    '''
    PROPASAL_STATUS =[
        ('ACCEPTED' , 'ACCEPTED'),
        ('INPROCESS' , 'INPROCESS'),
    ]
    CURRENCY_CHOICES = [

        ('USD','DOLLAR'),
    ]
    job = models.ForeignKey(JobPost , on_delete = models.CASCADE)
    freelancer = models.ForeignKey(Freelancer , on_delete = models.CASCADE)
    status = models.CharField(max_length = 10, choices = PROPASAL_STATUS,
                                       default=PROPASAL_STATUS[1][0])
    resume = models.FileField(upload_to='certificates/',
                        validators=[FileExtensionValidator(
                        allowed_extensions = ['pdf','txt','doc'],
                        message = 'only pdf, txt, doc extensions allowed')])
    
    bid  = models.PositiveIntegerField()
    currency = models.CharField(max_length=3,choices=CURRENCY_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f" {self.job.title} > {self.status} > {self.id} > {self.freelancer.id    }"
    class Meta:
        ordering = ['-created_at']
    

class Contract(models.Model):

    '''
    Contract model stores payment details , job payment deals between 
    client and freelancer
    '''
    proposal = models.OneToOneField(JobProposal, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add = True) 
    total = models.PositiveIntegerField()
    currency = models.CharField(max_length=7)
    remaining = models.PositiveIntegerField(null=True)
    
    def __str__(self):
        return f"{self.proposal.job.user.username} - {self.proposal.user.username}" 
    
    class Meta:
        ordering = ['-created_at'] 




    
class Review(DateManager):
    """
    Clients can review Freelancer and Freelancer can review Client ,
    created and updated field can be inherited from abstract model 
    """
    rating_by = models.ForeignKey(CustomUser , on_delete = models.CASCADE, related_name='rated_by')
    rating_to = models.ForeignKey(CustomUser , on_delete = models.CASCADE, related_name='rating_to')
    star_rating = models.PositiveIntegerField(default = 0)
    review_message = models.TextField(blank=True,null=True)
    job = models.ForeignKey(JobPost,on_delete = models.CASCADE)
    

    def __str__(self) -> str:
        return str(self.star_rating) 
    


