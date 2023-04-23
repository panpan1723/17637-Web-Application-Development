from django.db import models
from django.contrib.auth.models import User

LEVEL_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
]

CREDIT_CHOICES = [
    ('1', '6'),
    ('2', '12')
]

# Create your models here.
class CourseExperience(models.Model):
    # required
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="oauth_entry_creators")
    creation_time  = models.DateTimeField()
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=200)
    semester = models.CharField(max_length=20)
    credit = models.CharField(max_length=1, choices=CREDIT_CHOICES, default=CREDIT_CHOICES[0][1])
    load = models.CharField(max_length=1, choices=LEVEL_CHOICES, default=LEVEL_CHOICES[0][1])
    grade_satisfication = models.CharField(max_length=1, choices=LEVEL_CHOICES, default=LEVEL_CHOICES[0][1])
    difficulty = models.CharField(max_length=1, choices=LEVEL_CHOICES, default=LEVEL_CHOICES[0][1])
    subject = models.CharField(max_length=200)
    is_anonymous = models.BooleanField()
    professor_firstname = models.CharField(max_length=20)
    professor_lastname = models.CharField(max_length=20)
    # optional
    grade = models.IntegerField()
    content = models.CharField(max_length=1000)

class Comment(models.Model):
    text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='creator')
    # post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='post')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    comments = models.ManyToManyField(Comment, blank=True, related_name='comments')

class Course(models.Model):
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=200)
    professor_lastname = models.CharField(max_length=20)