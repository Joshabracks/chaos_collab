from django.db import models
from django.core.validators import validate_email
import bcrypt
from django.conf import settings

# managers

class UserManager(models.Manager):
    def validate_user(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 2:
            errors["name"] = 'Name should be at least 2 characters'
        if len(postData['alias']) < 2:
            errors["alias"] = 'Alias should be at least 2 characters'
        if len(postData['password']) < 8:
            errors['password'] = "Password name should be at least 8 characters"
        if (postData['password']) != (postData['cpassword']):
            errors['passconfirm'] = "Passwords do not match"
        if User.objects.filter(email = (postData['email'])):
            errors['inuse'] = "Email is already in use"
        try:
            validate_email(postData['email'])
        except:
            errors['invalid'] = "Invalid email"
        return errors
    def validate_login(self, postData):
        user = User.objects.get(email=postData['email'])
        errors = {}
        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors['invalid'] = 'invalid combination'
        return errors

# models

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=45, default="1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Collab(models.Model):
    title = models.CharField(max_length= 45, blank=False)
    description = models.TextField(max_length=45, blank=True)
    uploaded_by = models.ForeignKey(User, related_name="collabs", blank=True)
    encoded_img = models.TextField()
    decoded_img = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    parent = models.CharField(max_length=45, blank=True)

class Comment(models.Model):
    content = models.TextField()
    collab = models.ForeignKey(Collab, related_name="comment")
    user = models.ForeignKey(User, related_name="comment")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
