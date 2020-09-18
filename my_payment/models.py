from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.SmallIntegerField()

    def __str__(self):
    	return self.name


class CyberSourceTransaction(models.Model):
    """
    Stores credit card transaction receipts made with CyberSource.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    return_from_cybersource = models.DateTimeField(null=True, blank=True)


class CyberSourceResponse(models.Model):
	status = models.CharField(max_length=255)



