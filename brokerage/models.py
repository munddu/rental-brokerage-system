from django.db import models
from django.contrib.auth.models import User

KAMPALA_AREAS=[
('Ntinda','Ntinda'),('Kisaasi','Kisaasi'),('Naalya','Naalya'),('Kireka','Kireka'),
('Najjera','Najjera'),('Bukoto','Bukoto'),('Kyaliwajjala','Kyaliwajjala'),
('Mukono','Mukono'),('Bweyogerere','Bweyogerere'),('Namugongo','Namugongo')]
USER_ROLES=[('Tenant','Tenant'),('Landlord','Landlord')]
PROPERTY_STATUS=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')]

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,choices=USER_ROLES,default='Tenant')
    phone=models.CharField(max_length=20,blank=True)
    def __str__(self): return f'{self.user.username} - {self.role}'

class Property(models.Model):
    landlord=models.ForeignKey(User,on_delete=models.CASCADE,related_name='properties')
    title=models.CharField(max_length=200)
    description=models.TextField()
    area=models.CharField(max_length=50,choices=KAMPALA_AREAS)
    price=models.PositiveIntegerField()
    access_road_description=models.TextField()
    facilities=models.TextField(blank=True)
    image=models.ImageField(upload_to='property_images/',blank=True,null=True)
    video=models.FileField(upload_to='property_videos/',blank=True,null=True)
    status=models.CharField(max_length=20,choices=PROPERTY_STATUS,default='Pending')
    admin_comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.title} - {self.area}'

class Inquiry(models.Model):
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name='inquiries')
    tenant=models.ForeignKey(User,on_delete=models.CASCADE,related_name='inquiries')
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'Inquiry by {self.tenant.username}'
