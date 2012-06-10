from django.db import models
    
class Post(models.Model):
    title = models.CharField(max_length=1000)
    authors = models.TextField(blank=True)
    EDITION_CHOICES = (
        ('0', '[None]'),
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', '6th'),
        ('7', '7th'),
        ('8', '8th'),
        ('9', '9th'),
    )
    edition = models.CharField(max_length=2, choices=EDITION_CHOICES, blank=True)
    year = models.CharField(max_length=4, blank=True)
    isbn = models.CharField(max_length=13, blank=True) # http://djangosnippets.org/snippets/1994/
    courses = models.TextField(blank=True)
    description = models.TextField(blank=True)
    #department = models.ForeignKey(Department, blank=True)
    #photo = models.ImageField(blank=True)
    crdate = models.DateField(auto_now=True)
    mdate = models.DateField(auto_now=True)
    
    email = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    def __unicode__(self):
        return self.title

class Department(models.Model):
    title = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.title
