from django.db import models

# Create your models here.
class Email(models.Model):
    timestamp = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    from_email = models.EmailField()
    to_email = models.EmailField()
