from django.db import models
from django.core.validators import validate_email
import bcrypt

# managers

class UserManager(models.Manager):
    def validate_user(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = 'First name should be at least 2 characters'
        if len(postData['lname']) < 2:
            errors["lname"] = 'Last name should be at least 2 characters'
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
    screen_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Collab(models.Model):
    title = models.CharField(max_length= 45, blank=False)
    description = models.TextField(max_length=45, blank=True)
    uploaded_by = models.ForeignKey(User, related_name="uploaded_collabs")
    encoded_image = models.TextField()
    decoded_image = models.ImageField(upload_to = 'thumbs')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Pkey(models.Model):
    parent = models.OneToOneField(Collab, related_name='child_key')
    child = models.ForeignKey(Collab, related_name='parent_key')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)