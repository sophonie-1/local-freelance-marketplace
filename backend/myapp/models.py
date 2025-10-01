from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Profile(models.Model):
    USER_ROLES = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='client')
    bio = models.TextField(blank=True)
    skills = ArrayField(models.CharField(max_length=50), blank=True, default=list)  # E.g., ["Python", "Design"]
    location = models.CharField(max_length=100)  # Store as lat,long (e.g., "40.7128,-74.0060")
    portfolio = models.JSONField(blank=True, default=dict)  # Store file URLs or metadata

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Job(models.Model):
    client = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)  # Lat,long for geolocation
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='open')

    def __str__(self):
        return self.title

class Bid(models.Model):
    job = models.ForeignKey(Job, related_name='bids', on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.username} bid on {self.job.title}"

